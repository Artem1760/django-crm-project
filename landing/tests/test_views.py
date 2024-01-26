from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from associates.models import UserDepartment
from tickets.models import Ticket, Category

User = get_user_model()


class LandingPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_authenticated_user_redirected(self):
        user = get_user_model().objects.create_user(username='testuser',
                                                    password='testpassword')
        self.client.force_login(user)
        response = self.client.get(reverse('landing:landing-page'))
        self.assertRedirects(response, reverse('tickets:ticket-list'))

    def test_unauthenticated_user_access(self):
        response = self.client.get(reverse('landing:landing-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/landing.html')

    def test_unauthenticated_user_gets_template(self):
        response = self.client.get(reverse('landing:landing-page'))
        self.assertTemplateUsed(response, 'landing/landing.html')


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         password='testpassword',
                                                         is_organizer=True)
        self.client.force_login(self.user)

        # Check if UserDepartment already exists for the user
        user_department, _ = UserDepartment.objects.get_or_create(
            user=self.user)

        # Create necessary objects in the database
        category_completed = Category.objects.create(name='completed')

        # Create some tickets for the user
        Ticket.objects.create(
            title='Ticket 1',
            type=1,
            description='Description 1',
            department=user_department,
            category=category_completed
        )

        # Create another ticket completed in the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        Ticket.objects.create(
            title='Ticket 2',
            type=1,
            description='Description 2',
            department=user_department,
            category=category_completed,
            completed_date=thirty_days_ago
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('landing:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/dashboard.html')

    def test_dashboard_view_context(self):
        response = self.client.get(reverse('landing:dashboard'))
        context = response.context_data
        self.assertIn('total_ticket_count', context)
        self.assertIn('total_in_past30', context)
        self.assertIn('completed_in_past30', context)

    def test_dashboard_view_ticket_count(self):
        response = self.client.get(reverse('landing:dashboard'))
        context = response.context_data
        self.assertEqual(context['total_ticket_count'], 2)

    def test_dashboard_view_new_tickets_count(self):
        response = self.client.get(reverse('landing:dashboard'))
        context = response.context_data
        self.assertEqual(context['total_in_past30'], 2)

    def test_dashboard_view_no_tickets(self):
        # Remove all tickets for the user
        Ticket.objects.filter(department__user=self.user).delete()

        response = self.client.get(reverse('landing:dashboard'))
        context = response.context_data
        self.assertEqual(context['total_ticket_count'], 0)
        self.assertEqual(context['total_in_past30'], 0)
        self.assertEqual(context['completed_in_past30'], 0)


class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_view(self):
        response = self.client.get(reverse('landing:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/signup.html')


class LogoutViewTest(TestCase):
    def test_logout_view_redirects_to_login_page(self):
        response = self.client.get(reverse('landing:logout'))
        self.assertRedirects(response, reverse('landing:landing-page'))
