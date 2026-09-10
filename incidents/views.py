"""Class-based views for the incidents CRUD."""

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from incidents.forms import IncidentForm
from incidents.models import Incident


class IncidentListView(LoginRequiredMixin, ListView):
    """List incidents, optionally filtered by status and/or priority."""

    model = Incident
    context_object_name = "incidents"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Incident]:
        """Return incidents filtered by the ``status`` and ``priority`` query params.

        :return: The filtered, ordered queryset of incidents.
        """
        queryset = super().get_queryset()
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add the filter choices and current filter values to the template context.

        :param kwargs: Extra context passed by the parent implementation.
        :return: The context dictionary rendered by the template.
        """
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Incident.Status.choices
        context["priority_choices"] = Incident.Priority.choices
        context["selected_status"] = self.request.GET.get("status", "")
        context["selected_priority"] = self.request.GET.get("priority", "")
        return context


class IncidentDetailView(LoginRequiredMixin, DetailView):
    """Show the detail of a single incident."""

    model = Incident
    context_object_name = "incident"


class IncidentCreateView(LoginRequiredMixin, CreateView):
    """Create a new incident, owned by the logged-in user."""

    model = Incident
    form_class = IncidentForm

    def form_valid(self, form: IncidentForm) -> HttpResponse:
        """Assign the logged-in user as the reporter before saving.

        :param form: The validated incident form.
        :return: The HTTP response produced by the parent implementation.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class IncidentUpdateView(LoginRequiredMixin, UpdateView):
    """Edit an existing incident."""

    model = Incident
    form_class = IncidentForm


class IncidentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an existing incident, after confirmation."""

    model = Incident
    context_object_name = "incident"
    success_url = reverse_lazy("incidents:list")
