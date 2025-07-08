from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

class UsersTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('u','u@u.com','p')
        self.client.force_authenticate(self.user)

    def test_list_users(self):
        resp = self.client.get(reverse('user-list'))
        self.assertEqual(resp.status_code,200)

    def test_export_data(self):
        url = reverse('user-export-data', args=[self.user.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code,200)
        self.assertIn('username',resp.json())

    def test_delete_data(self):
        url = reverse('user-delete-data', args=[self.user.id])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code,204)
