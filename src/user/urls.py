"""URL routes for the user app: login, logout and registration."""

from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from user import views

app_name = "user"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="user:login"), name="index"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="user/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
