from django.test import TestCase
from django.contrib.auth import get_user_model
from associates.forms import AssociateForm

User = get_user_model()


class AssociateFormTest(TestCase):
    def test_associate_form_valid_data(self):
        form_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
        }

        form = AssociateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_associate_form_missing_required_field(self):
        form_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            # 'last_name' is missing
        }

        form = AssociateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_associate_form_invalid_email(self):
        form_data = {
            'email': 'invalid_email',  # Invalid email format
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
        }

        form = AssociateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

   