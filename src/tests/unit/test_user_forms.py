"""Unit tests for UserRegisterForm."""

from datetime import date

import pytest

from user.forms import UserRegisterForm

PASSWORD = "Str0ngPassw0rd!"

VALID_DATA = {
    "email": "newuser@example.com",
    "first_name": "Ana",
    "first_surname": "Garcia",
    "second_surname": "Lopez",
    "address": "Calle Mayor 1",
    "city": "Madrid",
    "dni": "12345678Z",
    "date_of_birth": date(1990, 1, 1),
    "password1": PASSWORD,
    "password2": PASSWORD,
}


@pytest.mark.django_db
def test_valid_data_is_valid() -> None:
    form = UserRegisterForm(data=VALID_DATA)
    assert form.is_valid()


@pytest.mark.django_db
def test_mismatched_passwords_is_invalid() -> None:
    data = {**VALID_DATA, "password2": "SomethingElse!"}
    form = UserRegisterForm(data=data)
    assert not form.is_valid()
    assert "password2" in form.errors


@pytest.mark.django_db
def test_common_password_is_invalid() -> None:
    data = {**VALID_DATA, "password1": "password", "password2": "password"}
    form = UserRegisterForm(data=data)
    assert not form.is_valid()
    assert "password2" in form.errors


def test_form_excludes_staff_and_superuser_fields() -> None:
    form = UserRegisterForm()
    assert set(form.fields) == {
        "email",
        "first_name",
        "first_surname",
        "second_surname",
        "address",
        "city",
        "dni",
        "date_of_birth",
        "password1",
        "password2",
    }


@pytest.mark.django_db
def test_save_creates_non_staff_non_superuser_with_hashed_password() -> None:
    form = UserRegisterForm(data=VALID_DATA)
    assert form.is_valid()
    user = form.save()
    assert user.pk is not None
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.password != PASSWORD
    assert user.check_password(PASSWORD)
