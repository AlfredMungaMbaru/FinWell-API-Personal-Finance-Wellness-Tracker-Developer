from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from categories.models import Category
from transactions.models import Transaction

class TransactionAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='txnuser', password='txnpass')
        self.client.login(username='txnuser', password='txnpass')
        self.token = self.client.post(reverse('token_obtain_pair'), {'username': 'txnuser', 'password': 'txnpass'}).data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.category = Category.objects.create(name='Groceries', type='expense', user=self.user)

    def test_create_transaction(self):
        url = reverse('transaction-list-create')
        data = {'category_id': self.category.id, 'amount': 50, 'date': '2025-08-24', 'description': 'Supermarket'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_list_transactions(self):
        Transaction.objects.create(user=self.user, category=self.category, amount=20, date='2025-08-24')
        url = reverse('transaction-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_transaction(self):
        txn = Transaction.objects.create(user=self.user, category=self.category, amount=10, date='2025-08-24')
        url = reverse('transaction-detail', args=[txn.id])
        data = {'category_id': self.category.id, 'amount': 30, 'date': '2025-08-24', 'description': 'Updated'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        txn.refresh_from_db()
        self.assertEqual(txn.amount, 30)

    def test_delete_transaction(self):
        txn = Transaction.objects.create(user=self.user, category=self.category, amount=5, date='2025-08-24')
        url = reverse('transaction-detail', args=[txn.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_amount_positive_validation(self):
        url = reverse('transaction-list-create')
        data = {'category_id': self.category.id, 'amount': -10, 'date': '2025-08-24'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
