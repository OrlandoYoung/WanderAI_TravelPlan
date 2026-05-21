from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from auth_app.models import User
import bcrypt

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        password = "testpassword".encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        self.user = User.objects.create(
            name="test_user",
            email="test@example.com",
            password_hash=hashed.decode('utf-8')
        )

    def test_successful_login(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)

    def test_failed_login_wrong_email(self):
        data = {
            "email": "wrong@example.com",
            "password": "testpassword"
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["success"], False)

    def test_failed_login_wrong_password(self):
        data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["success"], False)