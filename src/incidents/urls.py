"""URL routes for the incidents app."""

from django.urls import path

from incidents import views

app_name = "incidents"

urlpatterns = [
    path("", views.IncidentListView.as_view(), name="list"),
    path("new/", views.IncidentCreateView.as_view(), name="create"),
    path(
        "check-duplicates/",
        views.IncidentDuplicateCheckView.as_view(),
        name="check_duplicates",
    ),
    path("operability/", views.OperabilityCheckView.as_view(), name="operability"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("<int:pk>/", views.IncidentDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.IncidentUpdateView.as_view(), name="update"),
    path("<int:pk>/archive/", views.IncidentArchiveView.as_view(), name="archive"),
    path(
        "<int:pk>/unarchive/",
        views.IncidentUnarchiveView.as_view(),
        name="unarchive",
    ),
]
