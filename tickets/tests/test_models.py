from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from associates.models import Associate, UserDepartment
from tickets.models import Ticket, Category, FollowUp

User = get_user_model()


class TicketModelTest(TestCase):
    def setUp(self):
        self.organizer_user = User.objects.create_user(
            username='organizer',
            password='organizer_password',
            is_organizer=True
        )
        self.user_department, created = UserDepartment.objects.get_or_create(
            user=self.organizer_user)

        self.test_associate = Associate.objects.create(
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

        self.test_category = Category.objects.create(name='assigned')

    def test_ticket_creation(self):
        ticket = Ticket.objects.create(
            title='Test Ticket',
            type=1,
            description='Test Description',
            department=self.user_department,
            associate=self.test_associate,
            category=self.test_category
        )
        self.assertEqual(str(ticket), f'Test Ticket, id: {ticket.pk}')
        self.assertEqual(ticket.get_absolute_url(), f'/tickets/{ticket.pk}/')

    def test_category_creation(self):
        category = Category.objects.create(name='completed')
        self.assertEqual(str(category), 'Completed')
        self.assertEqual(category.get_absolute_url(),
                         f'/tickets/categories/{category.pk}/')

    def test_followup_creation(self):
        ticket = Ticket.objects.create(
            title='Test Ticket',
            type=1,
            description='Test Description',
            department=self.user_department,
            associate=self.test_associate,
            category=self.test_category
        )
        followup = FollowUp.objects.create(
            ticket=ticket,
            notes='Test FollowUp',
            file=SimpleUploadedFile("file.txt", b"file_content")
        )
        self.assertEqual(str(followup), f'Ticket id: {ticket.pk} FollowUp')
