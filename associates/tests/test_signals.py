from django.test import TestCase

from associates.models import UserDepartment, User


class SignalTest(TestCase):
    def test_user_created(self):
        # Create a new user with is_organizer set to True
        user = User.objects.create(username='organizer', is_organizer=True)

        # Check if UserDepartment is created for the organizer user
        user_department = UserDepartment.objects.get(user=user)
        self.assertEqual(user_department.user, user)

    def test_user_created_non_organizer(self):
        # Create a new user with is_organizer set to False
        user = User.objects.create(username='associate', is_organizer=False)

        # Ensure no UserDepartment is created for non-organizer user
        with self.assertRaises(UserDepartment.DoesNotExist):
            UserDepartment.objects.get(user=user)
