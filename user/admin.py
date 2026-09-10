"""Admin site configuration for the user model."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin site panel for :class:`~user.models.CustomUser`."""

    model = CustomUser
    ordering = ["email"]
    list_display = [
        "email",
        "first_name",
        "first_surname",
        "second_surname",
        "dni",
        "is_staff",
        "is_active",
    ]
    list_filter = ["is_staff", "is_active"]
    search_fields = ["email", "first_name", "first_surname", "second_surname", "dni"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal information",
            {
                "fields": (
                    "first_name",
                    "first_surname",
                    "second_surname",
                    "address",
                    "city",
                    "dni",
                    "date_of_birth",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
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
                ),
            },
        ),
    )
