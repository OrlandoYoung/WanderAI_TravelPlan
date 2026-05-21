from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from trip.models import Trip

class GenerateTripViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_generate_trip_success(self):
        data = {
            "origin": "北京",
            "destination": "上海",
            "startDate": "2024-10-01",
            "endDate": "2024-10-05",
            "numPeople": 2
        }
        response = self.client.post('/api/generate-trip/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(Trip.objects.count(), 1)

    def test_generate_trip_missing_parameters(self):
        data = {
            "origin": "北京",
            "destination": "上海"
        }
        response = self.client.post('/api/generate-trip/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["success"], False)