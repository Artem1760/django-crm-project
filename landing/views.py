from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from associates.mixins import OrganizerAndLoginRequiredMixin
from tickets.models import Ticket, Category
from .forms import CustomUserCreationForm


class LandingPageView(generic.TemplateView):
    template_name = 'landing/landing.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('tickets:ticket-list')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(OrganizerAndLoginRequiredMixin, generic.TemplateView):
    template_name = 'landing/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # How many tickets we have in total
        total_ticket_count = Ticket.objects.filter(
            department=user.userdepartment).count()

        # How many new tickets in the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)

        total_in_past30 = Ticket.objects.filter(
            department=user.userdepartment,
            created_date__gte=thirty_days_ago
        ).count()

        # How many completed tickets in the last 30 days       
        completed_category = get_object_or_404(Category, name='completed')
        completed_in_past30 = Ticket.objects.filter(
            department=user.userdepartment,
            category=completed_category,
            completed_date__gte=thirty_days_ago
        ).count()

        context.update({
            'total_ticket_count': total_ticket_count,
            'total_in_past30': total_in_past30,
            'completed_in_past30': completed_in_past30
        })
        return context


class SignupView(generic.CreateView):
    """View for user registration."""
    template_name = 'landing/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('tickets:ticket-list')

    def form_valid(self, form):
        """
        If the form is valid, log in the user and redirect to the success URL.
        """
        response = super().form_valid(form)
        user = authenticate(
            self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return response


def logout_view(request):
    logout(request)
    return redirect('landing:landing-page')
