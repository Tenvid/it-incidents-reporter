"""Views for user self-registration."""

from typing import Any

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from user.forms import UserRegisterForm
from user.models import CustomUser


class RegisterView(CreateView):
    """Self-service registration, always creating a regular (non-staff) user."""

    model = CustomUser
    form_class = UserRegisterForm
    template_name = "user/register.html"
    success_url = reverse_lazy("user:login")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """Send already-authenticated users straight to the incident list.

        Mirrors ``LoginView(redirect_authenticated_user=True)``, which
        handles the same case for the login page.

        :param request: The incoming HTTP request.
        :param args: Positional URL arguments.
        :param kwargs: Keyword URL arguments.
        :return: A redirect for authenticated users, or the parent dispatch otherwise.
        """
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: UserRegisterForm) -> HttpResponse:
        """Create the user, then send them to the login page with a confirmation.

        :param form: The validated registration form.
        :return: The HTTP response produced by the parent implementation.
        """
        response = super().form_valid(form)
        messages.success(self.request, "Account created. Log in to continue.")
        return response
