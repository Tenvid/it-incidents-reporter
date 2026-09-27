"""Integration tests for the user app's login, logout and registration views."""

from datetime import date

import pytest
from django.contrib.auth import get_user
from django.test import Client
from django.urls import reverse

from user.models import CustomUser

VALID_REGISTER_DATA = {
    "email": "newuser@example.com",
    "first_name": "Ana",
    "first_surname": "Garcia",
    "second_surname": "Lopez",
    "address": "Calle Mayor 1",
    "city": "Madrid",
    "dni": "12345678Z",
    "date_of_birth": date(1990, 1, 1),
    "password1": "Str0ngPassw0rd!",
    "password2": "Str0ngPassw0rd!",
}


# --- Register view ---


def test_register_view_get_renders_form(client: Client) -> None:
    response = client.get(reverse("user:register"))
    assert response.status_code == 200
    assert "form" in response.context


def test_register_view_get_redirects_authenticated_user_to_incidents_list(
    client: Client, user: CustomUser
) -> None:
    client.force_login(user)
    response = client.get(reverse("user:register"))
    assert response.status_code == 302
    assert response["Location"] == reverse("incidents:list")


@pytest.mark.django_db
def test_register_view_post_valid_creates_user_without_logging_in(client: Client) -> None:
    response = client.post(reverse("user:register"), VALID_REGISTER_DATA)
    assert response.status_code == 302
    assert response["Location"] == reverse("user:login")
    created = CustomUser.objects.get(email=VALID_REGISTER_DATA["email"])
    assert created.is_staff is False
    assert created.is_superuser is False
    assert not get_user(client).is_authenticated


@pytest.mark.django_db
def test_register_view_post_invalid_rerenders_form_with_errors(client: Client) -> None:
    data = {**VALID_REGISTER_DATA, "password2": "SomethingElse!"}
    response = client.post(reverse("user:register"), data)
    assert response.status_code == 200
    assert "password2" in response.context["form"].errors
    assert not CustomUser.objects.filter(email=VALID_REGISTER_DATA["email"]).exists()


# --- Login view ---


def test_login_view_get_renders_form(client: Client) -> None:
    response = client.get(reverse("user:login"))
    assert response.status_code == 200
    assert "form" in response.context


def test_login_view_get_redirects_authenticated_user_to_incidents_list(
    client: Client, user: CustomUser
) -> None:
    client.force_login(user)
    response = client.get(reverse("user:login"))
    assert response.status_code == 302
    assert response["Location"] == reverse("incidents:list")


def test_login_view_post_valid_credentials_logs_in_and_redirects(
    client: Client, user: CustomUser
) -> None:
    response = client.post(
        reverse("user:login"),
        {"username": user.email, "password": "Str0ngPassw0rd!"},
    )
    assert response.status_code == 302
    assert response["Location"] == reverse("incidents:list")
    assert get_user(client).is_authenticated


def test_login_view_post_wrong_password_does_not_log_in(client: Client, user: CustomUser) -> None:
    response = client.post(
        reverse("user:login"),
        {"username": user.email, "password": "wrong-password"},
    )
    assert response.status_code == 200
    assert not get_user(client).is_authenticated


# --- Logout view ---


def test_logout_view_get_is_not_allowed(client: Client, user: CustomUser) -> None:
    client.force_login(user)
    response = client.get(reverse("user:logout"))
    assert response.status_code == 405


def test_logout_view_post_logs_out_and_redirects(client: Client, user: CustomUser) -> None:
    client.force_login(user)
    response = client.post(reverse("user:logout"))
    assert response.status_code == 302
    assert response["Location"] == reverse("user:login")
    assert not get_user(client).is_authenticated


# --- Root and bare /accounts/ redirects ---


def test_root_redirects_anonymous_user_to_login(client: Client) -> None:
    response = client.get(reverse("root"))
    assert response.status_code == 302
    assert response["Location"] == reverse("user:login")


def test_root_redirects_authenticated_user_to_incidents_list(
    client: Client, user: CustomUser
) -> None:
    client.force_login(user)
    response = client.get(reverse("root"), follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[-1] == (reverse("incidents:list"), 302)


def test_bare_accounts_path_redirects_to_login(client: Client) -> None:
    response = client.get(reverse("user:index"))
    assert response.status_code == 302
    assert response["Location"] == reverse("user:login")
