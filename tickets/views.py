import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.forms import ValidationError
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from associates.mixins import OrganizerAndLoginRequiredMixin
from .forms import (TicketForm, AssignAssociateForm, TicketCategoryUpdateForm,
                    FollowUpForm, CategoryForm)
from .mixins import TicketFormAndUrlMixin, TicketQuerysetMixin, FollowUpMixin
from .models import Ticket, Category


class TicketCreateView(TicketFormAndUrlMixin, OrganizerAndLoginRequiredMixin,
                       generic.CreateView):
    """ View for creating a new ticket. """
    template_name = 'tickets/ticket/ticket_create.html'
    form_class = TicketForm

    def form_valid(self, form):
        ticket = form.save(commit=False)

        # Set the ticket department
        ticket.department = self.request.user.userdepartment
        ticket.save()
        send_mail(
            subject='A ticket has been created.',
            message='Go to the site to see the new ticket.',
            from_email='test@test.com',
            recipient_list=['associate@test.com']
        )
        messages.success(self.request,
                         'You have successfully created a ticket.')
        return super().form_valid(form)


class TicketListView(LoginRequiredMixin, generic.ListView):
    """ 
    View for displaying a list of tickets. 
    
    For organizer display all tickets assigned and unassigned to associates
    regarding the user's department.
    For associate display only tickets assigned to the specific user.
    """
    template_name = 'tickets/ticket/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            # Show tickets assigned to associates within their department
            queryset = Ticket.objects.filter(
                department=user.userdepartment,
                associate__isnull=False
            )
        else:
            # Show only tickets assigned to the specific associate
            queryset = Ticket.objects.filter(
                department=user.associate.department,
                associate__isnull=False
            )
            # Filter tickets regarding the specific associate           
            queryset = queryset.filter(associate__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            # For organizers, include a list of unassigned tickets
            queryset = Ticket.objects.filter(
                department=user.userdepartment,
                associate__isnull=True
            )
            context.update({'unassigned_tickets': queryset})
        return context


class TicketDetailView(TicketQuerysetMixin, LoginRequiredMixin,
                       generic.DetailView):
    """ View for ticket details. """
    template_name = 'tickets/ticket/ticket_detail.html'
    context_object_name = 'ticket'


class TicketUpdateView(TicketFormAndUrlMixin, OrganizerAndLoginRequiredMixin,
                       generic.UpdateView):
    """
    View for updating a ticket.

    Organizer can update tickets for the entire department.
    Associate is forbidden to update tickets.
    """
    template_name = 'tickets/ticket/ticket_update.html'
    form_class = TicketForm
    context_object_name = 'ticket'

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            # For organizers, show all tickets in the user's department
            queryset = Ticket.objects.filter(department=user.userdepartment)
        else:
            # For associates, forbid ticket updates by providing an empty queryset
            queryset = Ticket.objects.none()
        return queryset

    def form_valid(self, form):
        """
        If the ticket category is set to 'completed', update the completion date.
        """
        ticket_before_update = self.get_object()
        ticket = form.save(commit=False)
        completed_category = Category.objects.get(name='completed')

        if form.cleaned_data['category'] == completed_category:
            # Update the date at which this ticket was completed
            if ticket_before_update.category != completed_category:
                # This ticket has now been completed
                ticket.completed_date = datetime.datetime.now()
        ticket.save()
        messages.info(self.request,
                      'You have successfully updated this ticket')
        return super().form_valid(form)


class TicketDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    """
    View for deleting a ticket.
    
    Organizer can delete tickets for the entire department.
    Associate is forbidden to delete tickets.
    """
    template_name = 'tickets/ticket/ticket_delete.html'

    def get_success_url(self):
        return reverse('tickets:ticket-list')

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            # For organizers, show all tickets in the user's department
            queryset = Ticket.objects.filter(department=user.userdepartment)
        else:
            # For associates, forbid ticket deletion by providing an empty queryset
            queryset = Ticket.objects.none()
        return queryset


class TicketCategoryUpdateView(TicketQuerysetMixin, LoginRequiredMixin,
                               generic.UpdateView):
    """
    View for updating the category of a ticket.

    Organizer can update the category for tickets in their department.
    Associate can only update the category for their own assigned tickets.
    """
    template_name = 'tickets/ticket/ticket_category_update.html'
    form_class = TicketCategoryUpdateForm
    context_object_name = 'ticket'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """ 
        If the ticket category is set to 'completed', update the completion date.
        If the associate is not selected before assigning the category, raise
        a validation error and redirect with an error message.
        """
        ticket_before_update = self.get_object()
        instance = form.save(commit=False)
        completed_category = Category.objects.get(name='completed')

        # Check if the associate is selected
        try:
            if instance.associate is None:
                raise ValidationError(
                    'Associate must be selected before assigning a category.')
        except ValidationError as e:
            # Handle the validation error by redirecting back to the form
            # with an error message
            messages.error(self.request, str(*e))
            return redirect(reverse_lazy('tickets:ticket-category-update',
                                         kwargs={'pk': self.get_object().id}))

        if form.cleaned_data['category'] == completed_category:
            # Update the date at which this ticket was completed
            if ticket_before_update.category != completed_category:
                # This ticket has now been completed
                instance.completed_date = datetime.datetime.now()
        instance.save()
        messages.info(self.request,
                      'You have successfully updated this ticket')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tickets:ticket-detail',
                       kwargs={'pk': self.get_object().id})


class AssignAssociateView(TicketFormAndUrlMixin,
                          OrganizerAndLoginRequiredMixin, generic.FormView):
    """ View for assigning an associate to a ticket. """
    template_name = 'tickets/ticket/assign_associate.html'
    form_class = AssignAssociateForm

    def form_valid(self, form):
        # Retrieve the existing ticket
        ticket = Ticket.objects.get(id=self.kwargs['pk'])

        # Update the ticket with the selected associate
        ticket.associate = form.cleaned_data['associate']

        # Check if the 'assigned' category exists, create it if not
        assigned_category, created = Category.objects.get_or_create(name='assigned')
        
        if ticket.associate:
            # If an associate is selected, set the ticket category to 'assigned'
            ticket.category = assigned_category

        ticket.save()

        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    """ 
    View for displaying a list of ticket categories.

    For organizer display categories for their department.
    For associate display categories for their assigned tickets.
    """
    template_name = 'tickets/category/category_list.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Filter tickets based on the user's role and department
        if user.is_organizer:
            tickets = Ticket.objects.filter(department=user.userdepartment)
        else:
            tickets = Ticket.objects.filter(
                department=user.associate.department, associate=user.associate)

        # Count how many tickets are in each category based on the organizer 
        categories = self.get_queryset()
        category_counts = categories.annotate(count=Count('categories',
                            filter=Q(categories__in=tickets))).order_by('id')

        # Count how many tickets are unassigned        
        unassigned_ticket_count = tickets.filter(category__isnull=True).count()

        context.update({
            'unassigned_ticket_count': unassigned_ticket_count,
            'category_counts': category_counts,
        })

        return context


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    """
    View for displaying details of a specific ticket category.

    For organizer display all tickets in the category for their department.
    For associate display only their assigned tickets in the category.
    """
    template_name = 'tickets/category/category_detail.html'
    context_object_name = 'category'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Filter tickets based on the user's role and department
        if user.is_organizer:
            tickets = Ticket.objects.filter(department=user.userdepartment,
                                            category=self.object)
        else:
            tickets = Ticket.objects.filter(
                department=user.associate.department, associate=user.associate,
                category=self.object)

        context['tickets'] = tickets
        return context


class CategoryCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    """ View for creating a new ticket category only by organizers. """
    template_name = 'tickets/category/category_create.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('tickets:category-list')

    def form_valid(self, form):
        category_name = form.cleaned_data['name']
        # Check if the category name already exists
        if Category.objects.filter(name=category_name).exists():
            messages.error(self.request,
                           f'The category "{category_name}" already exists.')
            return self.form_invalid(form)

        messages.success(self.request,
                 f'The category "{category_name}" was created successfully.')
        return super().form_valid(form)


class FollowUpCreateView(LoginRequiredMixin, generic.CreateView):
    """ View for creating a new follow-up for a ticket. """
    template_name = 'tickets/followup/followup_create.html'
    form_class = FollowUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'ticket': Ticket.objects.get(pk=self.kwargs['pk'])})
        return context

    def form_valid(self, form):
        ticket = Ticket.objects.get(pk=self.kwargs['pk'])
        followup = form.save(commit=False)
        followup.ticket = ticket
        followup.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tickets:ticket-detail', kwargs={'pk': self.kwargs['pk']})


class FollowUpUpdateView(FollowUpMixin, generic.UpdateView):
    """ View for updating a ticket follow-up. """
    template_name = 'tickets/followup/followup_update.html'
    form_class = FollowUpForm


class FollowUpDeleteView(FollowUpMixin, generic.DeleteView):
    """ View for deleting a ticket follow-up. """
    template_name = 'tickets/followup/followup_delete.html'


class TicketJsonView(generic.View):
    """ View for retrieving ticket data as JSON from the database. """

    def get(self, request, *args, **kwargs):
        try:
            qs = Ticket.objects.all().values('title', 'description', 'type', 
                                             'category', 'department', 'associate')
            return JsonResponse({'qs': list(qs)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

