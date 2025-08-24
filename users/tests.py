from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class UserAuthTests(APITestCase):
    def test_register(self):
        url = reverse('register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login(self):
        User.objects.create_user(username='testuser', password='testpass123')
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_profile_get_and_update(self):
        user = User.objects.create_user(username='testuser', password='testpass123', email='test@example.com')
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(url, data)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # GET profile
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
        # PUT profile
        response = self.client.put(url, {'first_name': 'Test', 'last_name': 'User'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')
