from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse

from associates.models import Associate


class OrganizerAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organizer."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organizer:
            return redirect('tickets:ticket-list')
        return super().dispatch(request, *args, **kwargs)


class AssociateMixin:
    """
    Provides methods for getting the queryset of Associate instances based on
    the logged-in user's department and the success URL for Associate views.
    """

    def get_queryset(self):
        department = self.request.user.userdepartment
        return Associate.objects.filter(department=department)

    def get_success_url(self):
        return reverse('associates:associate-list')
