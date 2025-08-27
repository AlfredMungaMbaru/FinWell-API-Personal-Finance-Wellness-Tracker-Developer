from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from categories.models import Category
from transactions.models import Transaction
from budgets.models import Budget
from datetime import date, datetime
import json

class BudgetAlertsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test category
        self.category = Category.objects.create(
            name='Food',
            type='expense',
            user=self.user
        )
        
        # Create test budget for current month
        current_period = datetime.now().strftime('%Y-%m')
        self.budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            amount=1000.00,
            period=current_period
        )

    def test_budget_alert_near_limit(self):
        """Test budget alert when spending is near limit (80%)"""
        # Create transaction that brings total to 80% of budget
        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=800.00,  # 80% of 1000
            date=date.today(),
            description='Test transaction'
        )
        
        # Create another small transaction to trigger alert
        response = self.client.post('/api/transactions/', {
            'category_id': self.category.id,
            'amount': 10.00,
            'date': date.today().isoformat(),
            'description': 'Another test transaction'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        
        # Check that budget alert is present
        self.assertIsNotNone(response_data.get('budget_alert'))
        self.assertEqual(response_data['budget_alert']['type'], 'near_limit')
        self.assertIn('81.0%', response_data['budget_alert']['message'])

    def test_budget_alert_exceeded(self):
        """Test budget alert when spending exceeds budget"""
        # Create transaction that exceeds budget
        response = self.client.post('/api/transactions/', {
            'category_id': self.category.id,
            'amount': 1200.00,  # 120% of 1000
            'date': date.today().isoformat(),
            'description': 'Large transaction'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        
        # Check that budget alert is present
        self.assertIsNotNone(response_data.get('budget_alert'))
        self.assertEqual(response_data['budget_alert']['type'], 'exceeded')
        self.assertIn('20.0%', response_data['budget_alert']['message'])

    def test_no_budget_alert_under_threshold(self):
        """Test no budget alert when spending is under 80%"""
        response = self.client.post('/api/transactions/', {
            'category_id': self.category.id,
            'amount': 500.00,  # 50% of 1000
            'date': date.today().isoformat(),
            'description': 'Small transaction'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        
        # Check that no budget alert is present
        self.assertIsNone(response_data.get('budget_alert'))

    def test_no_budget_alert_no_budget(self):
        """Test no budget alert when no budget exists for category"""
        # Create another category without budget
        category2 = Category.objects.create(
            name='Entertainment',
            type='expense',
            user=self.user
        )
        
        response = self.client.post('/api/transactions/', {
            'category_id': category2.id,
            'amount': 100.00,
            'date': date.today().isoformat(),
            'description': 'No budget transaction'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        
        # Check that no budget alert is present
        self.assertIsNone(response_data.get('budget_alert'))


class CurrencyConversionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_currency_conversion_same_currency(self):
        """Test currency conversion with same source and target currency"""
        response = self.client.get('/api/convert/', {
            'amount': 100,
            'from': 'USD',
            'to': 'USD'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        
        self.assertEqual(response_data['amount'], 100)
        self.assertEqual(response_data['from'], 'USD')
        self.assertEqual(response_data['to'], 'USD')
        self.assertEqual(response_data['converted_amount'], 100)
        self.assertEqual(response_data['rate'], 1.0)

    def test_currency_conversion_missing_parameters(self):
        """Test currency conversion with missing parameters"""
        response = self.client.get('/api/convert/', {
            'amount': 100,
            'from': 'USD'
            # Missing 'to' parameter
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('Missing required parameters', response_data['error'])

    def test_currency_conversion_invalid_amount(self):
        """Test currency conversion with invalid amount"""
        response = self.client.get('/api/convert/', {
            'amount': 'invalid',
            'from': 'USD',
            'to': 'EUR'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('Amount must be a valid number', response_data['error'])

    def test_currency_conversion_negative_amount(self):
        """Test currency conversion with negative amount"""
        response = self.client.get('/api/convert/', {
            'amount': -100,
            'from': 'USD',
            'to': 'EUR'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('Amount must be positive', response_data['error'])

    def test_currency_conversion_invalid_currency_codes(self):
        """Test currency conversion with invalid currency codes"""
        response = self.client.get('/api/convert/', {
            'amount': 100,
            'from': 'US',  # Invalid - not 3 letters
            'to': 'EUR'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('Currency codes must be 3 letters', response_data['error'])


class ReportsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test categories
        self.food_category = Category.objects.create(
            name='Food',
            type='expense',
            user=self.user
        )
        self.transport_category = Category.objects.create(
            name='Transport',
            type='expense',
            user=self.user
        )
        
        # Create test budgets
        current_period = datetime.now().strftime('%Y-%m')
        Budget.objects.create(
            user=self.user,
            category=self.food_category,
            amount=500.00,
            period=current_period
        )
        Budget.objects.create(
            user=self.user,
            category=self.transport_category,
            amount=300.00,
            period=current_period
        )
        
        # Create test transactions
        Transaction.objects.create(
            user=self.user,
            category=self.food_category,
            amount=200.00,
            date=date.today(),
            description='Groceries'
        )
        Transaction.objects.create(
            user=self.user,
            category=self.transport_category,
            amount=150.00,
            date=date.today(),
            description='Bus fare'
        )

    def test_reports_summary(self):
        """Test reports summary endpoint"""
        response = self.client.get('/api/reports/summary/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        
        # Check response structure
        self.assertIn('summary', response_data)
        self.assertIn('totals', response_data)
        
        # Check totals
        totals = response_data['totals']
        self.assertEqual(totals['spent'], 350.0)  # 200 + 150
        self.assertEqual(totals['budget'], 800.0)  # 500 + 300
        self.assertEqual(totals['remaining'], 450.0)  # 800 - 350

    def test_reports_health_score(self):
        """Test financial health score endpoint"""
        response = self.client.get('/api/reports/health-score/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        
        # Check response structure
        self.assertIn('score', response_data)
        self.assertIn('message', response_data)
        
        # Check that score is between 0 and 100
        score = response_data['score']
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
