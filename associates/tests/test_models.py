from django.test import TestCase
from django.urls import reverse

from associates.models import User, Associate, UserDepartment


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        password='testpassword')

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))

    def test_user_str(self):
        self.assertEqual(self.user.__str__(), self.user.get_full_name())


class AssociateModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            is_organizer=False,
            is_associate=True
        )
        self.user_department, created = UserDepartment.objects.get_or_create(
                                            user=self.user
                                            )
        self.associate = Associate.objects.create(
                                            user=self.user,
                                            department=self.user_department
                                            )

    def test_associate_str_method(self):
        self.assertEqual(str(self.associate), 'test@example.com')

    def test_associate_get_absolute_url_method(self):
        url = reverse('associates:associate-detail',
                      kwargs={'pk': self.associate.pk})
        self.assertEqual(self.associate.get_absolute_url(), url)

    def test_associate_department(self):
        self.assertEqual(self.associate.department, self.user_department)

    def test_user_type(self):
        # Check if the user is an associate
        self.assertTrue(self.user.is_associate)
        # Ensure the user is not an organizer
        self.assertFalse(self.user.is_organizer)
