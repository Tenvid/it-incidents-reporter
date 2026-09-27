"""Integration tests for the admin-only DashboardView."""

from django.test import Client
from django.urls import reverse

from incidents.models import Incident
from user.models import CustomUser


def test_dashboard_view_redirects_anonymous_user_to_login(client: Client) -> None:
    response = client.get(reverse("incidents:dashboard"))
    assert response.status_code == 302
    assert response["Location"].startswith("/accounts/login/")


def test_dashboard_view_forbidden_for_non_staff_user(
    client: Client, user: CustomUser, incident: Incident
) -> None:
    client.force_login(user)
    response = client.get(reverse("incidents:dashboard"))
    assert response.status_code == 403


def test_dashboard_view_returns_200_for_staff_user(
    client: Client, staff_user: CustomUser, incident: Incident
) -> None:
    client.force_login(staff_user)
    response = client.get(reverse("incidents:dashboard"))
    assert response.status_code == 200


def test_dashboard_view_kpi_counts(
    client: Client, staff_user: CustomUser, incident: Incident, archived_incident: Incident
) -> None:
    # incident: priority=high, status=open, is_archived=False
    # archived_incident: priority=low, status=closed, is_archived=True
    client.force_login(staff_user)
    response = client.get(reverse("incidents:dashboard"))
    assert response.context["total_incidents"] == 2
    assert response.context["open_incidents"] == 1
    assert response.context["closed_incidents"] == 1
    assert response.context["high_priority_incidents"] == 1


def test_dashboard_view_priority_chart_data_ordered_and_counted(
    client: Client, staff_user: CustomUser, user: CustomUser
) -> None:
    Incident.objects.create(
        title="Low prio",
        description="d",
        equipment="Server-A",
        priority=Incident.Priority.LOW,
        status=Incident.Status.OPEN,
        user=user,
    )
    Incident.objects.create(
        title="High prio 1",
        description="d",
        equipment="Server-A",
        priority=Incident.Priority.HIGH,
        status=Incident.Status.OPEN,
        user=user,
    )
    Incident.objects.create(
        title="High prio 2",
        description="d",
        equipment="Server-A",
        priority=Incident.Priority.HIGH,
        status=Incident.Status.OPEN,
        user=user,
    )
    client.force_login(staff_user)
    response = client.get(reverse("incidents:dashboard"))
    data = response.context["priority_chart_data"]
    assert data["labels"] == [label for _, label in Incident.Priority.choices]
    assert data["series"] == [1, 0, 2]  # low, medium, high


def test_dashboard_view_status_chart_data_ordered_and_counted(
    client: Client, staff_user: CustomUser, user: CustomUser
) -> None:
    Incident.objects.create(
        title="Open incident",
        description="d",
        equipment="Server-A",
        priority=Incident.Priority.MEDIUM,
        status=Incident.Status.OPEN,
        user=user,
    )
    Incident.objects.create(
        title="Closed incident",
        description="d",
        equipment="Server-A",
        priority=Incident.Priority.MEDIUM,
        status=Incident.Status.CLOSED,
        user=user,
    )
    client.force_login(staff_user)
    response = client.get(reverse("incidents:dashboard"))
    data = response.context["status_chart_data"]
    assert data["labels"] == [label for _, label in Incident.Status.choices]
    assert data["series"] == [1, 0, 1]  # open, in_progress, closed


def test_dashboard_view_equipment_chart_data_counted(
    client: Client, staff_user: CustomUser, incident: Incident
) -> None:
    client.force_login(staff_user)
    response = client.get(reverse("incidents:dashboard"))
    data = response.context["equipment_chart_data"]
    assert data["labels"] == ["Server-01"]
    assert data["series"] == [1]


def test_dashboard_view_evolution_chart_data_has_all_granularities(
    client: Client, staff_user: CustomUser, incident: Incident
) -> None:
    client.force_login(staff_user)
    response = client.get(reverse("incidents:dashboard"))
    data = response.context["evolution_chart_data"]
    assert set(data.keys()) == {"day", "week", "month", "year"}
    for granularity, points in data.items():
        total = sum(point["y"] for point in points)
        assert total == 1, f"unexpected total for {granularity}"
