"""Unit tests for the Incident model."""

import pytest
from django.urls import reverse

from incidents.models import Incident
from user.models import CustomUser


def test_str_returns_title() -> None:
    incident = Incident(title="Printer jammed")
    assert str(incident) == "Printer jammed"


@pytest.mark.django_db
def test_get_absolute_url_returns_detail_path(incident: Incident) -> None:
    expected = reverse("incidents:detail", kwargs={"pk": incident.pk})
    assert incident.get_absolute_url() == expected


@pytest.mark.django_db
def test_default_priority_is_medium(user: CustomUser) -> None:
    incident = Incident.objects.create(
        title="Slow network",
        description="Network is slower than usual.",
        equipment="Router-01",
        user=user,
    )
    assert incident.priority == Incident.Priority.MEDIUM


@pytest.mark.django_db
def test_default_status_is_open(user: CustomUser) -> None:
    incident = Incident.objects.create(
        title="Slow network",
        description="Network is slower than usual.",
        equipment="Router-01",
        user=user,
    )
    assert incident.status == Incident.Status.OPEN


@pytest.mark.django_db
def test_date_is_set_automatically_on_create(incident: Incident) -> None:
    assert incident.date is not None


@pytest.mark.django_db
def test_ordering_by_date_descending(user: CustomUser) -> None:
    first = Incident.objects.create(
        title="First incident",
        description="Reported first.",
        equipment="Server-01",
        user=user,
    )
    second = Incident.objects.create(
        title="Second incident",
        description="Reported second.",
        equipment="Server-02",
        user=user,
    )
    assert list(Incident.objects.all()) == [second, first]


def test_priority_choices_labels() -> None:
    assert dict(Incident.Priority.choices) == {
        "low": "Low",
        "medium": "Medium",
        "high": "High",
    }


def test_status_choices_labels() -> None:
    assert dict(Incident.Status.choices) == {
        "open": "Open",
        "in_progress": "In progress",
        "closed": "Closed",
    }
