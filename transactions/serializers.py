from rest_framework import serializers
from transactions.models import Transaction
from categories.serializers import CategorySerializer

class TransactionSerializer(serializers.ModelSerializer):
	from categories.models import Category
	category = CategorySerializer(read_only=True)
	category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none(), write_only=True, source='category', required=True)

	class Meta:
		model = Transaction
		fields = ['id', 'category', 'category_id', 'amount', 'date', 'description']

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)
		if user:
			self.fields['category_id'].queryset = user.categories.all()

	def validate_amount(self, value):
		if value <= 0:
			raise serializers.ValidationError('Amount must be positive.')
		return value
