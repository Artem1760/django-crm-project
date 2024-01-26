from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from associates.models import Associate, UserDepartment


class AssociateViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.organizer_user = get_user_model().objects.create_user(
            username='organizer',
            password='organizer_password',
            is_organizer=True
        )
        self.user_department, created = UserDepartment.objects.get_or_create(
            user=self.organizer_user)

        self.client.force_login(self.organizer_user)

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

    def test_associate_list_view(self):
        response = self.client.get(reverse('associates:associate-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'associates/associate_list.html')

    def test_associate_create_view(self):
        response = self.client.get(reverse('associates:associate-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'associates/associate_create.html')

    def test_associate_create_form_submission(self):
        data = {
            'username': 'new_associate',
            'email': 'new_associate@test.com',
            'first_name': 'New',
            'last_name': 'Associate',
            'password': 'new_associate_password',
        }
        response = self.client.post(reverse('associates:associate-create'),
                                    data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Associate.objects.filter(user__username='new_associate').exists())

    def test_associate_detail_view(self):
        response = self.client.get(reverse('associates:associate-detail',
                                           args=[self.test_associate.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'associates/associate_detail.html')

    def test_associate_update_view(self):
        response = self.client.get(reverse('associates:associate-update',
                                           args=[self.test_associate.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'associates/associate_update.html')

    def test_associate_delete_view(self):
        response = self.client.get(reverse('associates:associate-delete',
                                           args=[self.test_associate.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'associates/associate_delete.html')

    def test_associate_delete_form_submission(self):
        response = self.client.post(reverse('associates:associate-delete',
                                            args=[self.test_associate.id]))
        self.assertEqual(response.status_code, 302)  # Check for a redirect
        self.assertFalse(
            Associate.objects.filter(user__username='test_associate').exists())
