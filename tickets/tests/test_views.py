from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from associates.models import Associate, UserDepartment
from tickets.models import Ticket, Category, FollowUp

User = get_user_model()


class BaseTicketViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create an organizer user
        self.organizer_user = User.objects.create_user(
            username='organizer',
            password='organizer_password',
            is_organizer=True
        )

        # Create or get a user department for the organizer
        self.user_department, created = UserDepartment.objects.get_or_create(
            user=self.organizer_user)

        # Create an Associate user
        self.associate_user = Associate.objects.create(
            user=User.objects.create_user(
                username='test_associate',
                email='associate@test.com',
                first_name='Test',
                last_name='Associate',
                password='test_associate_password',
                is_associate=True,
                is_organizer=False
            ),
            department=self.user_department
        )

        # Login as the organizer user
        self.client.force_login(self.organizer_user)

        # Create a ticket
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            type=1,
            description='Test Description',
            department=self.user_department
        )

        # Create a category
        self.category = Category.objects.create(name='assigned')


class TicketViewsTest(BaseTicketViewsTest):
    def setUp(self):
        super().setUp()

    def test_ticket_create_view(self):
        response = self.client.get(reverse('tickets:ticket-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket/ticket_create.html')

    def test_ticket_list_view(self):
        response = self.client.get(reverse('tickets:ticket-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket/ticket_list.html')

    def test_ticket_detail_view(self):
        response = self.client.get(
            reverse('tickets:ticket-detail', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket/ticket_detail.html')

    def test_ticket_update_view(self):
        response = self.client.get(
            reverse('tickets:ticket-update', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket/ticket_update.html')

    def test_ticket_delete_view(self):
        response = self.client.get(
            reverse('tickets:ticket-delete', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket/ticket_delete.html')

    def test_ticket_category_update_view(self):
        response = self.client.get(
            reverse('tickets:ticket-category-update', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'tickets/ticket/ticket_category_update.html')

    def test_assign_associate_view(self):
        response = self.client.get(
            reverse('tickets:assign-associate', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'tickets/ticket/assign_associate.html')


class CategoryViewsTest(BaseTicketViewsTest):
    def setUp(self):
        super().setUp()

    def test_category_list_view(self):
        response = self.client.get(reverse('tickets:category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'tickets/category/category_list.html')

    def test_category_detail_view(self):
        response = self.client.get(
            reverse('tickets:category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'tickets/category/category_detail.html')

    def test_category_create_view(self):
        response = self.client.get(reverse('tickets:category-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'tickets/category/category_create.html')

        # Test for creating a category with a unique name
        response = self.client.post(reverse('tickets:category-create'),
                                    {'name': 'processed'})

        self.assertEqual(response.status_code, 302)

        # Verify that the category is in the database
        category = Category.objects.get(name='processed')
        category.refresh_from_db()

        self.assertEqual(category.name, 'processed')


class FollowUpViewsTest(BaseTicketViewsTest):
    def setUp(self):
        super().setUp()

    def test_followup_create_view(self):
        response = self.client.get(
            reverse('tickets:ticket-followup-create', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'tickets/followup/followup_create.html')

    def test_followup_update_view(self):
        # Create a follow-up for the ticket
        followup = FollowUp.objects.create(ticket=self.ticket,
                                           notes='Original Notes')
        response = self.client.get(
            reverse('tickets:ticket-followup-update', args=[followup.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'tickets/followup/followup_update.html')

        # Test updating a follow-up
        response = self.client.post(
            reverse('tickets:ticket-followup-update', args=[followup.id]),
            {'notes': 'Updated Notes'})

        self.assertEqual(response.status_code, 302)

        # Verify that the follow-up is updated in the database
        followup.refresh_from_db()
        self.assertEqual(followup.notes, 'Updated Notes')

    def test_followup_delete_view(self):
        # Create a follow-up for the ticket
        followup = FollowUp.objects.create(ticket=self.ticket,
                                           notes='Test Follow-Up')

        response = self.client.get(
            reverse('tickets:ticket-followup-delete', args=[followup.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'tickets/followup/followup_delete.html')

        # Test deleting a follow-up
        response = self.client.post(
            reverse('tickets:ticket-followup-delete', args=[followup.id]))
        self.assertEqual(response.status_code, 302)

        # Verify that the follow-up is deleted from the database
        with self.assertRaises(FollowUp.DoesNotExist):
            FollowUp.objects.get(pk=followup.id)
