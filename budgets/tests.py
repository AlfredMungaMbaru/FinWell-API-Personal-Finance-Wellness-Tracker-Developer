from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from categories.models import Category
from budgets.models import Budget
from transactions.models import Transaction
from decimal import Decimal

class BudgetAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='budgetuser', password='budgetpass')
        self.client.login(username='budgetuser', password='budgetpass')
        self.token = self.client.post(reverse('login'), {'username': 'budgetuser', 'password': 'budgetpass'}).data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.category = Category.objects.create(name='Food', type='expense', user=self.user)

    def test_create_budget(self):
        url = reverse('budget-list-create')
        data = {'category_id': self.category.id, 'amount': 500, 'period': '2025-08'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 1)
        budget = Budget.objects.get()
        self.assertEqual(budget.amount, Decimal('500.00'))
        self.assertEqual(budget.period, '2025-08')

    def test_list_budgets_with_spending(self):
        budget = Budget.objects.create(user=self.user, category=self.category, amount=500, period='2025-08')
        # Create a transaction in the same category and period
        Transaction.objects.create(user=self.user, category=self.category, amount=100, date='2025-08-15')
        
        url = reverse('budget-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        budget_data = response.data[0]
        self.assertEqual(budget_data['total_spent'], Decimal('100.00'))
        self.assertEqual(budget_data['remaining'], Decimal('400.00'))

    def test_update_budget(self):
        budget = Budget.objects.create(user=self.user, category=self.category, amount=300, period='2025-08')
        url = reverse('budget-detail', args=[budget.id])
        data = {'category_id': self.category.id, 'amount': 600, 'period': '2025-08'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        budget.refresh_from_db()
        self.assertEqual(budget.amount, Decimal('600.00'))

    def test_delete_budget(self):
        budget = Budget.objects.create(user=self.user, category=self.category, amount=200, period='2025-08')
        url = reverse('budget-detail', args=[budget.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Budget.objects.count(), 0)

    def test_duplicate_budget_validation(self):
        # Create first budget
        Budget.objects.create(user=self.user, category=self.category, amount=300, period='2025-08')
        
        # Try to create another budget for same user, category, and period
        url = reverse('budget-list-create')
        data = {'category_id': self.category.id, 'amount': 400, 'period': '2025-08'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_amount_positive_validation(self):
        url = reverse('budget-list-create')
        data = {'category_id': self.category.id, 'amount': -100, 'period': '2025-08'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)

    def test_period_format_validation(self):
        url = reverse('budget-list-create')
        data = {'category_id': self.category.id, 'amount': 500, 'period': 'invalid-format'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('period', response.data)
