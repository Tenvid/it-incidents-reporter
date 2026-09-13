"""Forms for creating and editing incidents."""

from django import forms

from incidents.models import Incident


class IncidentForm(forms.ModelForm):
    """Form to create or update an :class:`~incidents.models.Incident`.

    ``user`` and ``date`` are excluded: the reporting user is set from
    ``request.user`` in the view, and the registration date is filled in
    automatically by the model (``auto_now_add``).
    """

    class Meta:
        model = Incident
        fields = ["title", "description", "equipment", "priority", "status"]
