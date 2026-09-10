"""Data model for the incidents app."""

from django.conf import settings
from django.db import models
from django.urls import reverse


class Incident(models.Model):
    """An IT incident reported for a piece of equipment or a service."""

    class Priority(models.TextChoices):
        """Priority levels an incident can be assigned."""

        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    class Status(models.TextChoices):
        """Lifecycle states an incident can be in."""

        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In progress"
        CLOSED = "closed", "Closed"

    title = models.CharField("title", max_length=200)
    description = models.TextField("description")
    equipment = models.CharField("affected equipment or service", max_length=150)
    date = models.DateTimeField("registration date", auto_now_add=True)
    priority = models.CharField(
        "priority", max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    status = models.CharField(
        "status", max_length=11, choices=Status.choices, default=Status.OPEN
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="incidents",
        verbose_name="reported by",
    )

    class Meta:
        verbose_name = "incident"
        verbose_name_plural = "incidents"
        ordering = ["-date"]

    def __str__(self) -> str:
        """Return a human-readable representation of the incident.

        :return: The incident's title.
        """
        return self.title

    def get_absolute_url(self) -> str:
        """Return the URL of this incident's detail page.

        :return: The absolute path to the incident's detail view.
        """
        return reverse("incidents:detail", kwargs={"pk": self.pk})
