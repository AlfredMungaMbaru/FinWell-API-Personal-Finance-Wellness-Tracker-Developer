from rest_framework import generics, permissions
from budgets.models import Budget
from budgets.serializers import BudgetSerializer

class BudgetListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        kwargs['user'] = self.request.user
        kwargs['context'] = {'request': self.request}
        return BudgetSerializer(*args, **kwargs)

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        kwargs['user'] = self.request.user
        kwargs['context'] = {'request': self.request}
        return BudgetSerializer(*args, **kwargs)

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
