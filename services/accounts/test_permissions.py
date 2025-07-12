from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class RBACPermissionTests(APITestCase):
    def setUp(self):
        # Create users for each role
        self.customer = User.objects.create_user(
            username='cust', password='custpass', role=User.ROLE_CUSTOMER
        )
        self.admin = User.objects.create_user(
            username='admin', password='adminpass', role=User.ROLE_ADMIN
        )
        self.superadmin = User.objects.create_user(
            username='super', password='superpass', role=User.ROLE_SUPERADMIN
        )

    def get_token(self, username, password):
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username': username, 'password': password}, format='json')
        return resp.data['access']

    def test_customer_cannot_create_user(self):
        token = self.get_token('cust', 'custpass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('user-list')
        resp = self.client.post(url, {'username':'x','password':'x'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_users_but_not_create(self):
        token = self.get_token('admin', 'adminpass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('user-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # attempt create
        resp2 = self.client.post(url, {'username':'x','password':'x'}, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_create_and_delete_user(self):
        token = self.get_token('super', 'superpass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('user-list')
        # create
        resp = self.client.post(url, {
            'username':'newuser', 'password':'newpass', 'role': User.ROLE_CUSTOMER
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        new_id = resp.data['id']
        # delete
        delete_url = reverse('user-detail', args=[new_id])
        resp2 = self.client.delete(delete_url)
        self.assertIn(resp2.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])
