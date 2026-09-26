"""Class-based views for the incidents CRUD."""

import json
from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Count, QuerySet
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek, TruncYear
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from incidents.forms import IncidentForm
from incidents.mixins import StaffRequiredMixin
from incidents.models import Incident
from ml.similarity import find_similar


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


class IncidentDuplicateCheckView(LoginRequiredMixin, View):
    """Score a candidate incident's text against open/in-progress incidents for duplicates.

    Used by the "Check dupes" button on the incident creation form (AJAX). Only
    gates the frontend's submit button; it is not a substitute for server-side
    validation of the created incident.
    """

    def post(self, request: HttpRequest) -> JsonResponse:
        """Return the open/in-progress incidents most similar to the posted text.

        :param request: The AJAX POST request, with a JSON body containing
            ``title``, ``description`` and ``equipment``.
        :return: A JSON response with a ``"duplicates"`` list of matches, each
            including its ``url``, ``status_display`` and similarity ``score``.
        """
        payload = json.loads(request.body)
        candidates = list(
            Incident.objects.filter(
                status__in=[Incident.Status.OPEN, Incident.Status.IN_PROGRESS],
                is_archived=False,
            ).values("id", "title", "description", "equipment", "status")
        )
        matches = find_similar(
            payload.get("title", ""),
            payload.get("description", ""),
            payload.get("equipment", ""),
            candidates,
        )
        for match in matches:
            match["url"] = reverse("incidents:detail", args=[match["id"]])
            match["status_display"] = Incident.Status(match["status"]).label
        return JsonResponse({"duplicates": matches})


class OperabilityCheckView(LoginRequiredMixin, TemplateView):
    """Page that checks the system end to end via the operability-check service.

    The page itself fetches a random incident client-side, straight from the
    standalone Flask service in ``networking/`` (see
    ``.claude/rules/conventions.md`` for why this one feature talks to a
    separate service instead of Django), so this view only needs to pass
    that service's base URL to the template.
    """

    template_name = "incidents/operability_check.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add the operability-check service's base URL to the template context.

        :param kwargs: Extra context passed by the parent implementation.
        :return: The context dictionary rendered by the template.
        """
        context = super().get_context_data(**kwargs)
        context["api_base_url"] = settings.INCIDENT_API_URL
        return context


class IncidentUpdateView(HideArchivedMixin, LoginRequiredMixin, UpdateView):
    """Edit an existing incident."""

    model = Incident
    form_class = IncidentForm


class IncidentArchiveView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
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


class IncidentUnarchiveView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Restore an archived incident, after confirmation, so regular users can see it again.

    Staff-only: archived incidents are hidden from the queryset used by the
    other views, so any non-staff user would otherwise be unable to reach
    this action.
    """

    model = Incident
    context_object_name = "incident"
    template_name = "incidents/incident_confirm_unarchive.html"

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


class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    """Admin-only dashboard with KPI counts and ApexCharts visualisations.

    Mirrors, inside the app, the metrics already computed read-only by
    ``analysis/analysis.ipynb`` and ``dashboard/dashboard.ipynb``; where a
    metric appears in both notebooks it is represented here only once.
    """

    template_name = "incidents/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Compute KPI counts and chart datasets for the dashboard template.

        :param kwargs: Extra context passed by the parent implementation.
        :return: The context dictionary rendered by the template.
        """
        context = super().get_context_data(**kwargs)
        context["total_incidents"] = Incident.objects.count()
        context["open_incidents"] = (
            Incident.objects.filter(is_archived=False)
            .exclude(status=Incident.Status.CLOSED)
            .count()
        )
        context["closed_incidents"] = Incident.objects.filter(
            status=Incident.Status.CLOSED
        ).count()
        context["high_priority_incidents"] = Incident.objects.filter(
            priority=Incident.Priority.HIGH
        ).count()
        context["priority_chart_data"] = self._priority_chart_data()
        context["status_chart_data"] = self._status_chart_data()
        context["equipment_chart_data"] = self._equipment_chart_data()
        context["evolution_chart_data"] = self._evolution_chart_data()
        return context

    def _priority_chart_data(self) -> dict[str, list[Any]]:
        """Return incident counts per priority, ordered like ``Incident.Priority``.

        :return: A dict with parallel ``labels`` and ``series`` lists.
        """
        counts = dict(
            Incident.objects.values("priority")
            .annotate(count=Count("id"))
            .values_list("priority", "count")
        )
        return {
            "labels": [label for _, label in Incident.Priority.choices],
            "series": [counts.get(value, 0) for value, _ in Incident.Priority.choices],
        }

    def _status_chart_data(self) -> dict[str, list[Any]]:
        """Return incident counts per status, ordered like ``Incident.Status``.

        :return: A dict with parallel ``labels`` and ``series`` lists.
        """
        counts = dict(
            Incident.objects.values("status")
            .annotate(count=Count("id"))
            .values_list("status", "count")
        )
        return {
            "labels": [label for _, label in Incident.Status.choices],
            "series": [counts.get(value, 0) for value, _ in Incident.Status.choices],
        }

    def _equipment_chart_data(self) -> dict[str, list[Any]]:
        """Return incident counts per affected equipment, for the top 15 equipments.

        :return: A dict with parallel ``labels`` and ``series`` lists, ordered
            by descending incident count.
        """
        rows = (
            Incident.objects.values("equipment")
            .annotate(count=Count("id"))
            .order_by("-count")[:15]
        )
        return {
            "labels": [row["equipment"] for row in rows],
            "series": [row["count"] for row in rows],
        }

    def _evolution_chart_data(self) -> dict[str, list[dict[str, Any]]]:
        """Return incident counts created per time period, at four granularities.

        :return: A dict mapping ``"day"``, ``"week"``, ``"month"`` and
            ``"year"`` to a list of ``{"x": <ISO date>, "y": <count>}`` points,
            ready to feed directly into an ApexCharts datetime series.
        """
        return {
            "day": self._evolution_series(TruncDay),
            "week": self._evolution_series(TruncWeek),
            "month": self._evolution_series(TruncMonth),
            "year": self._evolution_series(TruncYear),
        }

    def _evolution_series(self, trunc_func: type) -> list[dict[str, Any]]:
        """Return incident counts per period, truncated with the given function.

        :param trunc_func: A ``django.db.models.functions`` truncation class
            (e.g. ``TruncMonth``) applied to the incident's ``date`` field.
        :return: A list of ``{"x": <ISO date>, "y": <count>}`` points, ordered
            chronologically.
        """
        rows = (
            Incident.objects.annotate(period=trunc_func("date"))
            .values("period")
            .annotate(count=Count("id"))
            .order_by("period")
        )
        return [{"x": row["period"].strftime("%Y-%m-%d"), "y": row["count"]} for row in rows]
