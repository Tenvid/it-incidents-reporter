"""Integration tests for the OperabilityCheckView."""

from django.conf import settings
from django.test import Client
from django.urls import reverse

from user.models import CustomUser


def test_operability_check_view_redirects_anonymous_user_to_login(client: Client) -> None:
    response = client.get(reverse("incidents:operability"))
    assert response.status_code == 302
    assert response["Location"].startswith("/admin/login/")


def test_operability_check_view_returns_api_base_url_for_authenticated_user(
    client: Client, user: CustomUser
) -> None:
    client.force_login(user)
    response = client.get(reverse("incidents:operability"))
    assert response.status_code == 200
    assert response.context["api_base_url"] == settings.INCIDENT_API_URL
