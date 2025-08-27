from rest_framework import serializers
from transactions.models import Transaction
from categories.serializers import CategorySerializer
from budgets.models import Budget
from django.db.models import Sum
from datetime import datetime
from drf_spectacular.utils import extend_schema_field

class TransactionSerializer(serializers.ModelSerializer):
	from categories.models import Category
	category = CategorySerializer(read_only=True)
	category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none(), write_only=True, source='category', required=True)
	budget_alert = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = Transaction
		fields = ['id', 'category', 'category_id', 'amount', 'date', 'description', 'budget_alert']

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)
		if user:
			self.fields['category_id'].queryset = user.categories.all()
			self.user = user

	def validate_amount(self, value):
		if value <= 0:
			raise serializers.ValidationError('Amount must be positive.')
		return value

	@extend_schema_field(serializers.JSONField(allow_null=True))
	def get_budget_alert(self, obj):
		"""Check if spending is nearing or exceeding budget for the category and month"""
		if not hasattr(self, 'user'):
			return None
		
		# Get the month/year of the transaction
		transaction_date = obj.date
		period = transaction_date.strftime('%Y-%m')
		
		# Find budget for this category and period
		try:
			budget = Budget.objects.get(
				user=self.user,
				category=obj.category,
				period=period
			)
		except Budget.DoesNotExist:
			return None
		
		# Calculate total spending for this category in this period
		total_spent = Transaction.objects.filter(
			user=self.user,
			category=obj.category,
			date__year=transaction_date.year,
			date__month=transaction_date.month
		).aggregate(total=Sum('amount'))['total'] or 0
		
		# Calculate percentage used
		budget_amount = float(budget.amount)
		spent_percentage = (float(total_spent) / budget_amount) * 100
		
		# Generate alerts based on thresholds
		if spent_percentage > 100:
			return {
				"type": "exceeded",
				"message": f"Warning: You have exceeded your {obj.category.name} budget by {spent_percentage - 100:.1f}%! Spent: {total_spent}, Budget: {budget_amount}"
			}
		elif spent_percentage >= 80:
			return {
				"type": "near_limit",
				"message": f"Caution: You have used {spent_percentage:.1f}% of your {obj.category.name} budget. Spent: {total_spent}, Budget: {budget_amount}"
			}
		
		return None
