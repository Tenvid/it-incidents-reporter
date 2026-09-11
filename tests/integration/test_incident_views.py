"""Integration tests for the incidents views."""

from django.test import Client
from django.urls import reverse

from incidents.models import Incident
from user.models import CustomUser

VALID_FORM_DATA = {
    "title": "Network outage",
    "description": "No connectivity in building B.",
    "equipment": "Switch-12",
    "priority": "high",
    "status": "open",
}


# --- Anonymous access ---


def test_list_view_redirects_anonymous_user_to_login(client: Client) -> None:
    response = client.get(reverse("incidents:list"))
    assert response.status_code == 302
    assert response["Location"].startswith("/admin/login/")


def test_detail_view_redirects_anonymous_user_to_login(client: Client, incident: Incident) -> None:
    response = client.get(reverse("incidents:detail", kwargs={"pk": incident.pk}))
    assert response.status_code == 302
    assert response["Location"].startswith("/admin/login/")


def test_create_view_redirects_anonymous_user_to_login(client: Client) -> None:
    response = client.get(reverse("incidents:create"))
    assert response.status_code == 302
    assert response["Location"].startswith("/admin/login/")


def test_update_view_redirects_anonymous_user_to_login(client: Client, incident: Incident) -> None:
    response = client.get(reverse("incidents:update", kwargs={"pk": incident.pk}))
    assert response.status_code == 302
    assert response["Location"].startswith("/admin/login/")


def test_delete_view_redirects_anonymous_user_to_login(client: Client, incident: Incident) -> None:
    response = client.get(reverse("incidents:delete", kwargs={"pk": incident.pk}))
    assert response.status_code == 302
    assert response["Location"].startswith("/admin/login/")


# --- List view ---


def test_list_view_returns_incidents_for_logged_in_user(
    client: Client, user: CustomUser, other_user: CustomUser, incident: Incident
) -> None:
    other_incident = Incident.objects.create(
        title="Other user's incident",
        description="Reported by another user.",
        equipment="Laptop-05",
        user=other_user,
    )
    client.force_login(user)
    response = client.get(reverse("incidents:list"))
    assert response.status_code == 200
    incidents = list(response.context["incidents"])
    assert incident in incidents
    assert other_incident in incidents


def test_list_view_filters_by_status(client: Client, user: CustomUser) -> None:
    open_incident = Incident.objects.create(
        title="Open incident",
        description="Still open.",
        equipment="Server-01",
        status=Incident.Status.OPEN,
        user=user,
    )
    closed_incident = Incident.objects.create(
        title="Closed incident",
        description="Already closed.",
        equipment="Server-02",
        status=Incident.Status.CLOSED,
        user=user,
    )
    client.force_login(user)
    response = client.get(reverse("incidents:list"), {"status": "closed"})
    incidents = list(response.context["incidents"])
    assert closed_incident in incidents
    assert open_incident not in incidents
    assert response.context["selected_status"] == "closed"


def test_list_view_filters_by_priority(client: Client, user: CustomUser) -> None:
    high_incident = Incident.objects.create(
        title="High priority incident",
        description="Urgent.",
        equipment="Server-01",
        priority=Incident.Priority.HIGH,
        user=user,
    )
    low_incident = Incident.objects.create(
        title="Low priority incident",
        description="Not urgent.",
        equipment="Server-02",
        priority=Incident.Priority.LOW,
        user=user,
    )
    client.force_login(user)
    response = client.get(reverse("incidents:list"), {"priority": "high"})
    incidents = list(response.context["incidents"])
    assert high_incident in incidents
    assert low_incident not in incidents
    assert response.context["selected_priority"] == "high"


def test_list_view_filters_by_status_and_priority_combined(client: Client, user: CustomUser) -> None:
    matching = Incident.objects.create(
        title="Matching incident",
        description="Open and high priority.",
        equipment="Server-01",
        status=Incident.Status.OPEN,
        priority=Incident.Priority.HIGH,
        user=user,
    )
    other_status = Incident.objects.create(
        title="Other status incident",
        description="Closed and high priority.",
        equipment="Server-02",
        status=Incident.Status.CLOSED,
        priority=Incident.Priority.HIGH,
        user=user,
    )
    other_priority = Incident.objects.create(
        title="Other priority incident",
        description="Open and low priority.",
        equipment="Server-03",
        status=Incident.Status.OPEN,
        priority=Incident.Priority.LOW,
        user=user,
    )
    client.force_login(user)
    response = client.get(reverse("incidents:list"), {"status": "open", "priority": "high"})
    incidents = list(response.context["incidents"])
    assert incidents == [matching]
    assert other_status not in incidents
    assert other_priority not in incidents


def test_list_view_empty_filter_params_return_unfiltered_queryset(
    client: Client, user: CustomUser, incident: Incident
) -> None:
    client.force_login(user)
    response = client.get(reverse("incidents:list"), {"status": "", "priority": ""})
    assert response.status_code == 200
    assert incident in list(response.context["incidents"])
    assert response.context["selected_status"] == ""
    assert response.context["selected_priority"] == ""


def test_list_view_context_includes_choice_lists(client: Client, user: CustomUser) -> None:
    client.force_login(user)
    response = client.get(reverse("incidents:list"))
    assert response.context["status_choices"] == Incident.Status.choices
    assert response.context["priority_choices"] == Incident.Priority.choices


# --- Detail view ---


def test_detail_view_returns_200_for_existing_incident(client: Client, user: CustomUser, incident: Incident) -> None:
    client.force_login(user)
    response = client.get(reverse("incidents:detail", kwargs={"pk": incident.pk}))
    assert response.status_code == 200
    assert response.context["incident"] == incident


def test_detail_view_returns_404_for_nonexistent_pk(client: Client, user: CustomUser, incident: Incident) -> None:
    client.force_login(user)
    nonexistent_pk = incident.pk + 999
    response = client.get(reverse("incidents:detail", kwargs={"pk": nonexistent_pk}))
    assert response.status_code == 404


# --- Create view ---


def test_create_view_get_renders_form(client: Client, user: CustomUser) -> None:
    client.force_login(user)
    response = client.get(reverse("incidents:create"))
    assert response.status_code == 200
    assert "form" in response.context


def test_create_view_post_valid_creates_incident_with_request_user(client: Client, user: CustomUser) -> None:
    client.force_login(user)
    response = client.post(reverse("incidents:create"), VALID_FORM_DATA)
    assert response.status_code == 302
    created = Incident.objects.get(title=VALID_FORM_DATA["title"])
    assert created.user == user
    assert response["Location"] == created.get_absolute_url()


def test_create_view_post_invalid_rerenders_form_with_errors(client: Client, user: CustomUser) -> None:
    client.force_login(user)
    data = {**VALID_FORM_DATA, "title": ""}
    count_before = Incident.objects.count()
    response = client.post(reverse("incidents:create"), data)
    assert response.status_code == 200
    assert "title" in response.context["form"].errors
    assert Incident.objects.count() == count_before


# --- Update view ---


def test_update_view_get_prefills_form_with_existing_data(client: Client, user: CustomUser, incident: Incident) -> None:
    client.force_login(user)
    response = client.get(reverse("incidents:update", kwargs={"pk": incident.pk}))
    assert response.status_code == 200
    assert response.context["form"].instance == incident


def test_update_view_post_valid_updates_incident(client: Client, user: CustomUser, incident: Incident) -> None:
    client.force_login(user)
    data = {**VALID_FORM_DATA, "title": "Updated title"}
    response = client.post(reverse("incidents:update", kwargs={"pk": incident.pk}), data)
    assert response.status_code == 302
    incident.refresh_from_db()
    assert incident.title == "Updated title"
    assert response["Location"] == incident.get_absolute_url()


def test_update_view_post_by_different_user_still_succeeds(
    client: Client, other_user: CustomUser, incident: Incident
) -> None:
    client.force_login(other_user)
    data = {**VALID_FORM_DATA, "title": "Edited by another user"}
    response = client.post(reverse("incidents:update", kwargs={"pk": incident.pk}), data)
    assert response.status_code == 302
    incident.refresh_from_db()
    assert incident.title == "Edited by another user"


def test_update_view_post_invalid_rerenders_form_with_errors(client: Client, user: CustomUser, incident: Incident) -> None:
    client.force_login(user)
    original_title = incident.title
    data = {**VALID_FORM_DATA, "equipment": ""}
    response = client.post(reverse("incidents:update", kwargs={"pk": incident.pk}), data)
    assert response.status_code == 200
    assert "equipment" in response.context["form"].errors
    incident.refresh_from_db()
    assert incident.title == original_title


# --- Delete view ---


def test_delete_view_get_renders_confirmation_page(client: Client, user: CustomUser, incident: Incident) -> None:
    client.force_login(user)
    response = client.get(reverse("incidents:delete", kwargs={"pk": incident.pk}))
    assert response.status_code == 200
    assert response.context["incident"] == incident


def test_delete_view_post_deletes_and_redirects_to_list(client: Client, user: CustomUser, incident: Incident) -> None:
    client.force_login(user)
    response = client.post(reverse("incidents:delete", kwargs={"pk": incident.pk}))
    assert response.status_code == 302
    assert response["Location"] == reverse("incidents:list")
    assert not Incident.objects.filter(pk=incident.pk).exists()


def test_delete_view_post_by_different_user_still_succeeds(
    client: Client, other_user: CustomUser, incident: Incident
) -> None:
    client.force_login(other_user)
    response = client.post(reverse("incidents:delete", kwargs={"pk": incident.pk}))
    assert response.status_code == 302
    assert not Incident.objects.filter(pk=incident.pk).exists()
