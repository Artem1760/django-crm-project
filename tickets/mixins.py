from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from tickets.models import Ticket, FollowUp


class TicketFormAndUrlMixin:
    """
    This mixin includes methods for getting the form instance 
    and success URL for Ticket views.
    """

    def get_form_kwargs(self, **kwargs):
        """
        Get the keyword arguments to instantiate the form.

        Returns:
        dict: Keyword arguments for form instantiation, including 'user_department'.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user_department'] = self.request.user.userdepartment
        return kwargs

    def get_success_url(self):
        return reverse('tickets:ticket-list')


class TicketQuerysetMixin:
    """
    This mixin includes method for getting the queryset for Ticket views.
    """

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            # For organizers, show all tickets in the user's department
            queryset = Ticket.objects.filter(department=user.userdepartment)
        else:
            # For associates, show only their assigned tickets
            queryset = Ticket.objects.filter(
                department=user.associate.department, associate=user.associate)

        return queryset


class FollowUpMixin(LoginRequiredMixin):
    """
    This mixin includes methods for getting the queryset and
    success URL for FollowUp views.
    """

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            # Filter for the entire department
            queryset = FollowUp.objects.filter(
                ticket__department=user.userdepartment)
        else:
            queryset = FollowUp.objects.filter(
                ticket__department=user.associate.department)
            # Filter for the specific associate
            queryset = queryset.filter(ticket__associate__user=user)
        return queryset

    def get_success_url(self):
        return reverse('tickets:ticket-detail',
                       kwargs={'pk': self.get_object().ticket.id})
