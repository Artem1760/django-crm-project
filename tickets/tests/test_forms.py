from django.contrib.auth import get_user_model
from django.test import TestCase

from associates.models import Associate, UserDepartment
from tickets.forms import (TicketForm, AssignAssociateForm,
                           TicketCategoryUpdateForm, CategoryForm,
                           FollowUpForm)
from tickets.models import Category


class TicketFormsTest(TestCase):
    def setUp(self):
        self.organizer_user = get_user_model().objects.create_user(
            username='organizer',
            password='organizer_password',
            is_organizer=True
        )
        self.user_department, created = UserDepartment.objects.get_or_create(
            user=self.organizer_user)

        self.test_associate = Associate.objects.create(
            user=get_user_model().objects.create_user(
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

    def test_ticket_form_associate_filtering(self):
        form = TicketForm(user_department=self.user_department)
        associate_field = form.fields['associate']
        self.assertIn(self.test_associate, associate_field.queryset)

    def test_assign_associate_form_associate_filtering(self):
        form = AssignAssociateForm(user_department=self.user_department)
        associate_field = form.fields['associate']
        self.assertIn(self.test_associate, associate_field.queryset)

    def test_ticket_category_update_form_organizer_categories(self):
        form = TicketCategoryUpdateForm(user=self.organizer_user)
        category_field = form.fields['category']
        self.assertIn(self.test_category, category_field.queryset)

    def test_ticket_category_update_form_associate_categories(self):
        form = TicketCategoryUpdateForm(user=self.test_associate.user)
        category_field = form.fields['category']
        self.assertNotIn(self.test_category, category_field.queryset)

    def test_category_form(self):
        form_data = {'name': 'returned'}
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_follow_up_form(self):
        form_data = {'notes': 'Follow up notes'}
        form = FollowUpForm(data=form_data)
        self.assertTrue(form.is_valid())
