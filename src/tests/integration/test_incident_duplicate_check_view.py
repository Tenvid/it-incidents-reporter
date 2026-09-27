"""Integration tests for the IncidentDuplicateCheckView (AJAX duplicate check)."""

import json

from django.test import Client
from django.urls import reverse
from sklearn.feature_extraction.text import TfidfVectorizer

from incidents.models import Incident
from user.models import CustomUser


def post_check(client: Client, title: str, description: str, equipment: str):
    return client.post(
        reverse("incidents:check_duplicates"),
        data=json.dumps({"title": title, "description": description, "equipment": equipment}),
        content_type="application/json",
    )


def test_check_duplicates_view_redirects_anonymous_user_to_login(client: Client) -> None:
    response = post_check(client, "Printer jam", "printer paper jam", "printer room")
    assert response.status_code == 302
    assert response["Location"].startswith("/accounts/login/")


def test_check_duplicates_view_returns_matching_open_incident(
    client: Client, user: CustomUser, fitted_vectorizer: TfidfVectorizer
) -> None:
    open_incident = Incident.objects.create(
        title="Printer jam",
        description="printer paper jam display shows error",
        equipment="printer room",
        status=Incident.Status.OPEN,
        user=user,
    )
    client.force_login(user)
    response = post_check(
        client, open_incident.title, open_incident.description, open_incident.equipment
    )
    assert response.status_code == 200
    data = response.json()
    matched_ids = [match["id"] for match in data["duplicates"]]
    assert open_incident.id in matched_ids
    match = next(m for m in data["duplicates"] if m["id"] == open_incident.id)
    assert match["url"] == open_incident.get_absolute_url()
    assert match["status_display"] == "Open"
    assert "score" in match


def test_check_duplicates_view_returns_matching_in_progress_incident(
    client: Client, user: CustomUser, fitted_vectorizer: TfidfVectorizer
) -> None:
    in_progress_incident = Incident.objects.create(
        title="Printer jam",
        description="printer paper jam display shows error",
        equipment="printer room",
        status=Incident.Status.IN_PROGRESS,
        user=user,
    )
    client.force_login(user)
    response = post_check(
        client,
        in_progress_incident.title,
        in_progress_incident.description,
        in_progress_incident.equipment,
    )
    matched_ids = [match["id"] for match in response.json()["duplicates"]]
    assert in_progress_incident.id in matched_ids


def test_check_duplicates_view_excludes_closed_incident(
    client: Client, user: CustomUser, fitted_vectorizer: TfidfVectorizer
) -> None:
    closed_incident = Incident.objects.create(
        title="Printer jam",
        description="printer paper jam display shows error",
        equipment="printer room",
        status=Incident.Status.CLOSED,
        user=user,
    )
    client.force_login(user)
    response = post_check(
        client, closed_incident.title, closed_incident.description, closed_incident.equipment
    )
    matched_ids = [match["id"] for match in response.json()["duplicates"]]
    assert closed_incident.id not in matched_ids


def test_check_duplicates_view_excludes_archived_incident_even_if_open(
    client: Client, user: CustomUser, fitted_vectorizer: TfidfVectorizer
) -> None:
    archived_open_incident = Incident.objects.create(
        title="Printer jam",
        description="printer paper jam display shows error",
        equipment="printer room",
        status=Incident.Status.OPEN,
        is_archived=True,
        user=user,
    )
    client.force_login(user)
    response = post_check(
        client,
        archived_open_incident.title,
        archived_open_incident.description,
        archived_open_incident.equipment,
    )
    matched_ids = [match["id"] for match in response.json()["duplicates"]]
    assert archived_open_incident.id not in matched_ids


def test_check_duplicates_view_returns_empty_list_when_no_incidents_exist(
    client: Client, user: CustomUser, fitted_vectorizer: TfidfVectorizer
) -> None:
    client.force_login(user)
    response = post_check(client, "Printer jam", "printer paper jam", "printer room")
    assert response.status_code == 200
    assert response.json() == {"duplicates": []}
