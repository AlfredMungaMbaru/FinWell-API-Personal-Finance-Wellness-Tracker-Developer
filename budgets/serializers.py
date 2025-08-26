from rest_framework import serializers
from budgets.models import Budget
from categories.serializers import CategorySerializer
from categories.models import Category
from transactions.models import Transaction
from django.db.models import Sum
from decimal import Decimal

class BudgetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.none(), 
        write_only=True, 
        source='category', 
        required=True
    )
    total_spent = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ['id', 'category', 'category_id', 'amount', 'period', 'total_spent', 'remaining']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category_id'].queryset = user.categories.all()

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be positive.')
        return value

    def validate_period(self, value):
        # Validate YYYY-MM format
        try:
            from datetime import datetime
            datetime.strptime(value, '%Y-%m')
        except ValueError:
            raise serializers.ValidationError('Period must be in YYYY-MM format.')
        return value

    def validate(self, data):
        user = self.context['request'].user
        category = data['category']
        period = data['period']
        
        # Check for duplicate budget (user, category, period) only for create operations
        if not self.instance:  # Only validate for create, not update
            if Budget.objects.filter(user=user, category=category, period=period).exists():
                raise serializers.ValidationError('A budget for this category and period already exists.')
        
        return data

    def get_total_spent(self, obj):
        # Calculate total spent in this category for this period
        year, month = obj.period.split('-')
        spent = Transaction.objects.filter(
            user=obj.user,
            category=obj.category,
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total']
        return spent or Decimal('0.00')

    def get_remaining(self, obj):
        total_spent = self.get_total_spent(obj)
        return obj.amount - total_spent
