"""Field validators specific to the user application."""

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

DNI_REGEX = re.compile(r"^(?P<number>\d{8})(?P<letter>[A-Za-z])$")

_DNI_CONTROL_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"


def validate_dni(value: str) -> None:
    """Validate that ``value`` has the format of a valid Spanish DNI.

    Checks both the shape (8 digits followed by a letter) and that the
    control letter matches the number, following the official algorithm
    (number modulo 23).

    :param value: Value of the DNI field to validate.
    :raises ValidationError: If the format is invalid or the control
        letter does not match the number.
    """
    match = DNI_REGEX.match(value or "")
    if not match:
        raise ValidationError(
            _("“%(value)s” is not a valid DNI: it must have 8 digits followed by a letter."),
            code="invalid_dni_format",
            params={"value": value},
        )

    number = int(match.group("number"))
    letter = match.group("letter").upper()
    expected_letter = _DNI_CONTROL_LETTERS[number % 23]
    if letter != expected_letter:
        raise ValidationError(
            _("The control letter of DNI “%(value)s” is not correct."),
            code="invalid_dni_letter",
            params={"value": value},
        )
