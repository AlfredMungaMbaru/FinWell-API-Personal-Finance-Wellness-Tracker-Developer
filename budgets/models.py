from django.db import models
from django.contrib.auth.models import User
from categories.models import Category

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    period = models.CharField(max_length=7)  # YYYY-MM format
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'category', 'period')

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.period}: {self.amount}"
