"""Admin site configuration for the incidents app."""

from django.contrib import admin

from incidents.models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    """Admin site panel for :class:`~incidents.models.Incident`."""

    list_display = ["title", "equipment", "priority", "status", "user", "date"]
    list_filter = ["status", "priority"]
    search_fields = ["title", "equipment", "description"]
    date_hierarchy = "date"
