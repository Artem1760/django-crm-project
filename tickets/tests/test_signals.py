from django.contrib.auth import get_user_model
from django.test import TestCase

from associates.models import Associate, UserDepartment
from tickets.models import Ticket, Category

User = get_user_model()


class TicketSignalsTest(TestCase):
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

        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            type=1,
            description='Test Description',
            department=self.user_department,
            associate=self.test_associate
        )

    def test_pre_save_ticket_signal_set_category(self):
        self.assertEqual(self.ticket.category, self.test_category)

    def test_pre_save_ticket_signal_unset_category(self):
        self.ticket.associate = None
        self.ticket.save()
        self.assertIsNone(self.ticket.category)
