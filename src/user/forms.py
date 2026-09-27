"""Forms for user self-registration."""

from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from user.models import CustomUser


class UserRegisterForm(forms.ModelForm):
    """Self-registration form that creates a regular, non-staff user.

    Written from scratch rather than subclassing
    :class:`~django.contrib.auth.forms.UserCreationForm`: Django's docs say
    that form is tied to the default ``User`` model and must be rewritten
    for a custom user model with no ``username`` field, which is exactly
    our case (``CustomUser.USERNAME_FIELD`` is ``email``). ``is_staff`` and
    ``is_superuser`` are intentionally left out of ``Meta.fields``, so a
    registered user always keeps the model's defaults (``False``/``False``).
    """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "first_surname",
            "second_surname",
            "address",
            "city",
            "dni",
            "date_of_birth",
        ]
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}

    def clean_password2(self) -> str | None:
        """Check that the two password entries match and satisfy the configured validators.

        :return: The confirmed password, or ``None`` if it wasn't provided.
        :raises ValidationError: If the two password fields don't match, or
            the password fails one of ``AUTH_PASSWORD_VALIDATORS``.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")
        if password2:
            password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit: bool = True) -> CustomUser:
        """Save the user with the hashed password.

        :param commit: Whether to persist the user to the database.
        :return: The created user instance.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
