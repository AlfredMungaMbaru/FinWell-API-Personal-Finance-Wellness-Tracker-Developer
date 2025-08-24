from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	CATEGORY_TYPES = (
		('income', 'Income'),
		('expense', 'Expense'),
	)
	name = models.CharField(max_length=100)
	type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

	def __str__(self):
		return self.name
