import random

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import AssociateForm
from .mixins import OrganizerAndLoginRequiredMixin, AssociateMixin
from .models import Associate


class AssociateListView(OrganizerAndLoginRequiredMixin, AssociateMixin,
                        generic.ListView):
    """View for listing Associate instances."""
    template_name = 'associates/associate_list.html'
    context_object_name = 'associates'


class AssociateCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    """View for creating a new Associate instance."""
    template_name = 'associates/associate_create.html'
    form_class = AssociateForm

    def get_success_url(self):
        return reverse('associates:associate-list')

    def form_valid(self, form):
        """ Create associate and set the department regarding the organizer """
        user = form.save(commit=False)
        user.is_associate = True
        user.is_organizer = False
        user.set_password(f'{random.randint(0, 1000000)}')
        user.save()
        # Creates a new Associate instance
        associate = Associate.objects.create(
            user=user,
            department=self.request.user.userdepartment
        )
        messages.success(self.request,
                         f'Associate {associate} was created successfully.')
        return super().form_valid(form)

    def send_invitation_email(self, user):
        """ Sends an invitation email to the new Associate. """
        send_mail(
            subject='You are invited to be an associate.',
            message=f'You were added as an associate on CRM. '
                    f'Temporary password is: {user.password}.',
            from_email='django@crm.com',
            recipient_list=[user.email]
        )


class AssociateDetailView(OrganizerAndLoginRequiredMixin, AssociateMixin,
                          generic.DetailView):
    """View for displaying details of an Associate instance."""
    template_name = 'associates/associate_detail.html'
    context_object_name = 'associate'


class AssociateUpdateView(OrganizerAndLoginRequiredMixin, AssociateMixin,
                          generic.UpdateView):
    """View for updating Associate details."""
    template_name = 'associates/associate_update.html'
    form_class = AssociateForm
    context_object_name = 'associate'

    def get(self, request, *args, **kwargs):
        """
        Retrieves the Associate and populates the form with existing data.
        """
        associate = get_object_or_404(Associate, id=self.kwargs['pk'])
        form = self.form_class(instance=associate.user)
        return self.render_to_response({'form': form, 'associate': associate})

    def form_valid(self, form):
        """ Updates the User model fields and displays success messages. """
        associate = get_object_or_404(Associate, id=self.kwargs['pk'])

        user = associate.user
        user.email = form.cleaned_data['email']
        user.username = form.cleaned_data['username']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        messages.success(self.request, 'Associate data was updated successfully.')

        return super().form_valid(form)


class AssociateDeleteView(OrganizerAndLoginRequiredMixin, AssociateMixin,
                          SuccessMessageMixin, generic.DeleteView):
    """View for deleting an Associate instance."""
    template_name = 'associates/associate_delete.html'
    context_object_name = 'associate'
    success_message = 'Associate was deleted successfully.'
    