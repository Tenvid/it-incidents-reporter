"""Manager for the custom user model."""

from typing import TYPE_CHECKING, Any

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from user.models import CustomUser


class CustomUserManager(BaseUserManager["CustomUser"]):
    """Manager that creates users using the email address as the identifier."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields: Any) -> "CustomUser":
        """Create, validate and save a user with the given email and password.

        :param email: User's email address, used as the username.
        :param password: Plain-text password; it is hashed before saving.
        :param extra_fields: Remaining fields of the user model.
        :return: The user instance created and saved to the database.
        :raises ValueError: If no email address is provided.
        """
        if not email:
            raise ValueError("Users must have an email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields: Any) -> "CustomUser":
        """Create a regular user, without staff or superuser privileges.

        :param email: User's email address.
        :param password: Plain-text password.
        :param extra_fields: Remaining fields of the user model.
        :return: The created user instance.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: Any) -> "CustomUser":
        """Create a superuser with full access to the admin site.

        :param email: Superuser's email address.
        :param password: Plain-text password.
        :param extra_fields: Remaining fields of the user model.
        :return: The created superuser instance.
        :raises ValueError: If ``is_staff`` or ``is_superuser`` are forced to False.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
