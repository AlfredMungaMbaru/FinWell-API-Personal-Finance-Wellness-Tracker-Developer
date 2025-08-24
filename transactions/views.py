from rest_framework import generics, permissions
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer

class TransactionListCreateView(generics.ListCreateAPIView):
	permission_classes = [permissions.IsAuthenticated]

	def get_serializer(self, *args, **kwargs):
		kwargs['user'] = self.request.user
		return TransactionSerializer(*args, **kwargs)

	def get_queryset(self):
		return Transaction.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [permissions.IsAuthenticated]

	def get_serializer(self, *args, **kwargs):
		kwargs['user'] = self.request.user
		return TransactionSerializer(*args, **kwargs)

	def get_queryset(self):
		return Transaction.objects.filter(user=self.request.user)
