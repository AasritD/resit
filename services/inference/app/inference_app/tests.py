from django.test import TestCase, Client
from django.contrib.auth.models import User
from io import BytesIO
class InferenceTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user('u','u@u.com','p')
        self.client=Client(); self.client.login(username='u',password='p')
    def test_predict_api(self):
        f=BytesIO(b"1,2,3\n4,5,6"); f.name='data.csv'
        resp=self.client.post('/inference/api/predict/',{'file':f})
        self.assertEqual(resp.status_code,201); self.assertIn('prediction',resp.json())
    def test_upload_ui(self):
        resp=self.client.get('/inference/upload/')
        self.assertEqual(resp.status_code,200); self.assertContains(resp,'<form')
