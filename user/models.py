"""Custom user model for the application."""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from user.managers import CustomUserManager
from user.validators import validate_dni


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Application user, authenticated with an email address and a password.

    Replaces Django's default user model (there is no username): the email
    address is the unique identifier used to log in, and the password is
    always stored hashed, handled by
    :class:`~django.contrib.auth.base_user.AbstractBaseUser`.
    """

    email = models.EmailField("email address", unique=True)
    first_name = models.CharField("first name", max_length=150)
    first_surname = models.CharField("first surname", max_length=150)
    second_surname = models.CharField("second surname", max_length=150)
    address = models.CharField("address", max_length=255)
    city = models.CharField("city", max_length=150)
    dni = models.CharField(
        "DNI",
        max_length=9,
        unique=True,
        validators=[validate_dni],
        help_text="Spanish national ID: 8 digits followed by a letter (e.g. 12345678Z).",
    )
    date_of_birth = models.DateField("date of birth")

    is_active = models.BooleanField("active", default=True)
    is_staff = models.BooleanField("staff status", default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "first_surname",
        "second_surname",
        "address",
        "city",
        "dni",
        "date_of_birth",
    ]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(dni__regex=r"^[0-9]{8}[A-Za-z]$"),
                name="user_dni_valid_format",
            ),
        ]

    def __str__(self) -> str:
        """Return a human-readable representation of the user.

        :return: The user's email address.
        """
        return self.email

    def clean(self) -> None:
        """Validate model rules that do not depend on a single field.

        :raises ValidationError: If the date of birth is in the future.
        """
        super().clean()
        if self.date_of_birth and self.date_of_birth > timezone.localdate():
            raise ValidationError(
                {"date_of_birth": "The date of birth cannot be in the future."}
            )

    def get_full_name(self) -> str:
        """Return the user's full name.

        :return: The first name and both surnames separated by spaces.
        """
        parts = [self.first_name, self.first_surname, self.second_surname]
        return " ".join(part for part in parts if part)

    def get_short_name(self) -> str:
        """Return the user's short name.

        :return: The user's first name.
        """
        return self.first_name
