"""Integration tests for the ``seed_incidents`` management command."""

from datetime import timedelta
from io import StringIO

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone

from incidents.models import Incident
from user.models import CustomUser


def test_seed_command_creates_requested_number_of_incidents(user: CustomUser) -> None:
    out = StringIO()
    call_command("seed_incidents", count=20, seed=1, stdout=out)

    assert Incident.objects.count() == 20
    assert "Created 20 sample incidents." in out.getvalue()


def test_seed_command_assigns_incidents_to_existing_users(
    user: CustomUser, other_user: CustomUser
) -> None:
    call_command("seed_incidents", count=50, seed=1, stdout=StringIO())

    reporters = set(Incident.objects.values_list("user_id", flat=True))
    assert reporters <= {user.pk, other_user.pk}
    assert len(reporters) == 2


def test_seed_command_backdates_incidents_within_the_given_days(
    user: CustomUser,
) -> None:
    before = timezone.now()
    call_command("seed_incidents", count=30, seed=1, days=10, stdout=StringIO())

    dates = list(Incident.objects.values_list("date", flat=True))
    assert all(before - timedelta(days=10) <= date <= timezone.now() for date in dates)
    assert len(set(dates)) > 1


def test_seed_command_is_reproducible_with_a_seed(user: CustomUser) -> None:
    call_command("seed_incidents", count=15, seed=42, stdout=StringIO())
    first_run = list(
        Incident.objects.order_by("pk").values_list("title", "description", "equipment")
    )
    Incident.objects.all().delete()

    call_command("seed_incidents", count=15, seed=42, stdout=StringIO())
    second_run = list(
        Incident.objects.order_by("pk").values_list("title", "description", "equipment")
    )

    assert first_run == second_run


@pytest.mark.django_db
def test_seed_command_fails_when_there_are_no_users() -> None:
    with pytest.raises(CommandError, match="Create at least one user"):
        call_command("seed_incidents", count=5, stdout=StringIO())

    assert Incident.objects.count() == 0
