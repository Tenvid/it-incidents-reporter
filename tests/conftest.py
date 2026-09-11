"""Shared fixtures for the incidents test suite."""

from datetime import date

import pytest

from incidents.models import Incident
from user.models import CustomUser


@pytest.fixture
def user(db: None) -> CustomUser:
    """Return a valid CustomUser to act as the reporter of incidents.

    :param db: Enables database access for this fixture.
    :return: A saved CustomUser instance.
    """
    return CustomUser.objects.create_user(
        email="reporter@example.com",
        password="Str0ngPassw0rd!",
        first_name="Ana",
        first_surname="Garcia",
        second_surname="Lopez",
        address="Calle Mayor 1",
        city="Madrid",
        dni="12345678Z",
        date_of_birth=date(1990, 1, 1),
    )


@pytest.fixture
def other_user(db: None) -> CustomUser:
    """Return a second valid CustomUser, distinct from ``user``.

    :param db: Enables database access for this fixture.
    :return: A saved CustomUser instance.
    """
    return CustomUser.objects.create_user(
        email="other@example.com",
        password="Str0ngPassw0rd!",
        first_name="Carlos",
        first_surname="Ruiz",
        second_surname="Sanchez",
        address="Calle Menor 2",
        city="Barcelona",
        dni="87654321X",
        date_of_birth=date(1985, 6, 15),
    )


@pytest.fixture
def incident(db: None, user: CustomUser) -> Incident:
    """Return a saved Incident reported by ``user``.

    :param db: Enables database access for this fixture.
    :param user: The reporter of the incident.
    :return: A saved Incident instance.
    """
    return Incident.objects.create(
        title="Server down",
        description="Main server is unreachable.",
        equipment="Server-01",
        priority=Incident.Priority.HIGH,
        status=Incident.Status.OPEN,
        user=user,
    )
