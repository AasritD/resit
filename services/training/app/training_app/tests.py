from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch

class TrainingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_runs_empty(self):
        url = reverse('training-runs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('training_app.views.subprocess.run')
    def test_retrain_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = 'training started'
        url = reverse('training-retrain')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('training started', response.json()['output'])

    @patch('training_app.views.subprocess.run')
    def test_retrain_failure(self, mock_run):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = 'error happened'
        url = reverse('training-retrain')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error happened', response.json()['error'])
