from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class BillingTests(TestCase):
    def setUp(self):
        self.u=User.objects.create_user('x','x@x.com','p')
        self.client=APIClient(); self.client.login(username='x',password='p')

    def test_usage_list(self):
        resp=self.client.get('/billing/api/usage/')
        self.assertEqual(resp.status_code,200)

    def test_invoice_generate(self):
        url='/billing/api/invoice/generate/'
        data={'start':'2025-01-01','end':'2025-01-31'}
        resp=self.client.post(url,data,format='json')
        self.assertEqual(resp.status_code,201)
        self.assertIn('invoice_id',resp.json())
