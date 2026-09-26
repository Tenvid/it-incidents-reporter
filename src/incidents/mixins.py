"""Shared access-control mixins for incidents views."""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest


class StaffRequiredMixin(UserPassesTestMixin):
    """Restrict a view to staff (administrator) users.

    Combines ``UserPassesTestMixin`` with the staff check itself, so views
    only need ``LoginRequiredMixin, StaffRequiredMixin`` (in that order) to
    be staff-only.
    """

    request: HttpRequest

    def test_func(self) -> bool:
        """Restrict this view to staff (administrator) users.

        :return: ``True`` if the requesting user is staff.
        """
        return bool(self.request.user.is_staff)
