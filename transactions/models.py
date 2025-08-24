from django.db import models
from django.contrib.auth.models import User
from categories.models import Category

class Transaction(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	date = models.DateField()
	description = models.TextField(blank=True)

	def __str__(self):
		return f"{self.category.name}: {self.amount}"
