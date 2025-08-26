from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from categories.models import Category

class CategoryAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='catuser', password='catpass')
        self.client.login(username='catuser', password='catpass')
        self.token = self.client.post(reverse('token_obtain_pair'), {'username': 'catuser', 'password': 'catpass'}).data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_category(self):
        url = reverse('category-list-create')
        data = {'name': 'Food', 'type': 'expense'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Food')

    def test_list_categories(self):
        Category.objects.create(name='Salary', type='income', user=self.user)
        url = reverse('category-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_category(self):
        cat = Category.objects.create(name='Bills', type='expense', user=self.user)
        url = reverse('category-detail', args=[cat.id])
        response = self.client.put(url, {'name': 'Utilities', 'type': 'expense'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cat.refresh_from_db()
        self.assertEqual(cat.name, 'Utilities')

    def test_delete_category(self):
        cat = Category.objects.create(name='Fun', type='expense', user=self.user)
        url = reverse('category-detail', args=[cat.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
