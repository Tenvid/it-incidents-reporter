"""Class-based views for the incidents CRUD."""

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from incidents.forms import IncidentForm
from incidents.models import Incident


class HideArchivedMixin:
    """Hide archived incidents from non-staff users.

    Staff users (administrators) can still see and open archived incidents;
    everyone else gets the same result as if they had been deleted.
    """

    request: HttpRequest

    def get_queryset(self) -> QuerySet[Incident]:
        """Exclude archived incidents from the queryset for non-staff users.

        :return: The queryset, filtered to non-archived incidents unless the
            requesting user is staff.
        """
        queryset = super().get_queryset()  # type: ignore[misc]
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_archived=False)
        return queryset


class IncidentListView(HideArchivedMixin, LoginRequiredMixin, ListView):
    """List incidents, optionally filtered by status, priority and archived state."""

    model = Incident
    context_object_name = "incidents"
    paginate_by = 20

    class ArchivedFilter(models.TextChoices):
        """Values of the staff-only "archived" filter on the incident list."""

        NOT_ARCHIVED = "not_archived", "Not archived"
        ONLY_ARCHIVED = "only_archived", "Only archived"
        ALL = "all", "All"

    def get_queryset(self) -> QuerySet[Incident]:
        """Return incidents filtered by the ``status``, ``priority`` and ``archived`` query params.

        The ``archived`` filter only has an effect for staff users: non-staff
        users never see archived incidents, regardless of this param, because
        ``HideArchivedMixin`` already excludes them.

        :return: The filtered, ordered queryset of incidents.
        """
        queryset = super().get_queryset()
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if self.request.user.is_staff:
            archived_filter = self.get_archived_filter()
            if archived_filter == self.ArchivedFilter.NOT_ARCHIVED:
                queryset = queryset.filter(is_archived=False)
            elif archived_filter == self.ArchivedFilter.ONLY_ARCHIVED:
                queryset = queryset.filter(is_archived=True)
        return queryset

    def get_archived_filter(self) -> str:
        """Return the selected value of the staff-only "archived" filter.

        :return: One of :class:`ArchivedFilter`'s values, defaulting to
            ``NOT_ARCHIVED`` when missing or not a recognised value.
        """
        value = self.request.GET.get("archived", self.ArchivedFilter.NOT_ARCHIVED)
        if value not in self.ArchivedFilter.values:
            return self.ArchivedFilter.NOT_ARCHIVED
        return value

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
        if self.request.user.is_staff:
            context["archived_choices"] = self.ArchivedFilter.choices
            context["selected_archived"] = self.get_archived_filter()
        filter_params = self.request.GET.copy()
        filter_params.pop("page", None)
        context["filter_querystring"] = filter_params.urlencode()
        return context


class IncidentDetailView(HideArchivedMixin, LoginRequiredMixin, DetailView):
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


class IncidentUpdateView(HideArchivedMixin, LoginRequiredMixin, UpdateView):
    """Edit an existing incident."""

    model = Incident
    form_class = IncidentForm


class IncidentArchiveView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Archive an incident instead of deleting it, after confirmation.

    This is a soft delete: the incident row is kept, marked as archived, so
    it disappears from regular users' views while staff users can still see
    and open it.

    Staff-only: restricting who can archive an incident to staff users means
    the post-archive redirect to the incident's own detail page never 404s,
    since that page also hides archived incidents from non-staff users.
    """

    model = Incident
    context_object_name = "incident"
    template_name = "incidents/incident_confirm_archive.html"

    def test_func(self) -> bool:
        """Restrict this action to staff (administrator) users.

        :return: ``True`` if the requesting user is staff.
        """
        return bool(self.request.user.is_staff)

    def get_success_url(self) -> str:
        """Return the incident's own detail page as the post-archive redirect target.

        :return: The absolute URL of the archived incident.
        """
        return self.object.get_absolute_url()

    def form_valid(self, form: Any) -> HttpResponse:
        """Mark the incident as archived instead of deleting it.

        ``BaseDeleteView.post()`` calls this method (not ``delete()``) to
        commit the deletion, so the archiving logic has to live here.

        :param form: The (unused) confirmation form built by ``DeleteView``.
        :return: A redirect to the incident's detail page.
        """
        success_url = self.get_success_url()
        self.object.is_archived = True
        self.object.save(update_fields=["is_archived"])
        return HttpResponseRedirect(success_url)


class IncidentUnarchiveView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Restore an archived incident, after confirmation, so regular users can see it again.

    Staff-only: archived incidents are hidden from the queryset used by the
    other views, so any non-staff user would otherwise be unable to reach
    this action.
    """

    model = Incident
    context_object_name = "incident"
    template_name = "incidents/incident_confirm_unarchive.html"

    def test_func(self) -> bool:
        """Restrict this action to staff (administrator) users.

        :return: ``True`` if the requesting user is staff.
        """
        return bool(self.request.user.is_staff)

    def get_success_url(self) -> str:
        """Return the incident's own detail page as the post-unarchive redirect target.

        :return: The absolute URL of the unarchived incident.
        """
        return self.object.get_absolute_url()

    def form_valid(self, form: Any) -> HttpResponse:
        """Clear the ``is_archived`` flag on the incident instead of deleting it.

        ``BaseDeleteView.post()`` calls this method (not ``delete()``) to
        commit the deletion, so the unarchiving logic has to live here.

        :param form: The (unused) confirmation form built by ``DeleteView``.
        :return: A redirect to the incident's detail page.
        """
        success_url = self.get_success_url()
        self.object.is_archived = False
        self.object.save(update_fields=["is_archived"])
        return HttpResponseRedirect(success_url)
