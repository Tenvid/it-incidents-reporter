"""Shared fixtures for the incidents test suite."""

from datetime import date

import pytest
from sklearn.feature_extraction.text import TfidfVectorizer

from incidents.models import Incident
from ml import similarity
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
def staff_user(db: None) -> CustomUser:
    """Return a valid, staff (administrator) CustomUser.

    :param db: Enables database access for this fixture.
    :return: A saved, staff CustomUser instance.
    """
    return CustomUser.objects.create_user(
        email="admin@example.com",
        password="Str0ngPassw0rd!",
        first_name="Marta",
        first_surname="Fernandez",
        second_surname="Diaz",
        address="Calle Real 3",
        city="Valencia",
        dni="11223344B",
        date_of_birth=date(1980, 3, 20),
        is_staff=True,
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


@pytest.fixture
def archived_incident(db: None, user: CustomUser) -> Incident:
    """Return a saved, archived Incident reported by ``user``.

    :param db: Enables database access for this fixture.
    :param user: The reporter of the incident.
    :return: A saved Incident instance with ``is_archived=True``.
    """
    return Incident.objects.create(
        title="Archived incident",
        description="Already archived.",
        equipment="Server-02",
        priority=Incident.Priority.LOW,
        status=Incident.Status.CLOSED,
        user=user,
        is_archived=True,
    )


@pytest.fixture
def fitted_vectorizer(monkeypatch: pytest.MonkeyPatch) -> TfidfVectorizer:
    """Swap ``ml.similarity``'s loaded vectorizer for one fit on a small, fixed corpus.

    Keeps duplicate-detection tests independent of any local
    artifact.

    :param monkeypatch: Pytest's monkeypatch fixture.
    :return: The vectorizer now in effect for ``ml.similarity.find_similar``.
    """
    corpus = [
        "printer paper jam display shows error printer room",
        "server down network outage no connectivity server room",
        "coffee machine leaking water kitchen floor",
    ]
    vectorizer = TfidfVectorizer().fit(corpus)
    monkeypatch.setattr(similarity, "VECTORIZER", vectorizer)
    return vectorizer
