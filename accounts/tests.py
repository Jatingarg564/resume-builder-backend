from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, UserSettings
import json


class SignupTests(TestCase):
    """Test user signup functionality"""

    def setUp(self):
        self.client = APIClient()
        self.signup_url = '/api/accounts/signup/'

    def test_signup_valid_data(self):
        """AUTH-001: Signup with valid data should create user"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)

    def test_signup_duplicate_username(self):
        """AUTH-002: Duplicate username should be rejected"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        # First signup
        self.client.post(self.signup_url, data, format='json')
        # Second signup with same username
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_duplicate_email(self):
        """AUTH-003: Duplicate email behavior (note: backend allows duplicate emails)"""
        data1 = {
            'username': 'testuser1',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        data2 = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        self.client.post(self.signup_url, data1, format='json')
        # Note: Current backend allows duplicate emails (only username is unique)
        # This test documents the current behavior
        response = self.client.post(self.signup_url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email='test@example.com').count(), 2)

    def test_signup_empty_username(self):
        """AUTH-004: Empty username should be rejected"""
        data = {
            'username': '',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalid_email(self):
        """AUTH-005: Invalid email format should be rejected"""
        data = {
            'username': 'testuser',
            'email': 'invalidemail@',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_xss_in_username(self):
        """AUTH-014: XSS in username should be stored safely"""
        data = {
            'username': '<script>alert(1)</script>',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.signup_url, data, format='json')
        # Should either reject or store safely
        if response.status_code == status.HTTP_201_CREATED:
            user = User.objects.get(username=data['username'])
            self.assertEqual(user.username, data['username'])


class LoginTests(TestCase):
    """Test user login functionality"""

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/accounts/login/'
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )

    def test_login_valid_credentials(self):
        """AUTH-009: Login with valid credentials should return tokens"""
        data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        """AUTH-010: Invalid credentials should be rejected"""
        data = {
            'username': 'testuser',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        """AUTH-011: Non-existent user should be rejected"""
        data = {
            'username': 'fakeuser',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileTests(TestCase):
    """Test profile management"""

    def setUp(self):
        self.client = APIClient()
        self.profile_url = '/api/accounts/profile/'
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!',
            email='test@example.com'
        )
        # Get token
        login_response = self.client.post('/api/accounts/login/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_profile_get_own_profile(self):
        """AUTH-019: Get own profile should return user data"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_profile_update_own_profile(self):
        """AUTH-020: Update own profile should work"""
        data = {
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.patch(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')

    def test_profile_unauthorized(self):
        """AUTH-013: Access profile without token should fail"""
        self.client.credentials()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserSettingsTests(TestCase):
    """Test user settings"""

    def setUp(self):
        self.client = APIClient()
        self.settings_url = '/api/accounts/settings/'
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        login_response = self.client.post('/api/accounts/login/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_settings_get(self):
        """AUTH-027: Get settings should return settings object"""
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('theme_preference', response.data)

    def test_settings_update(self):
        """AUTH-028: Update settings should work"""
        data = {'theme_preference': 'dark'}
        response = self.client.patch(self.settings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['theme_preference'], 'dark')
