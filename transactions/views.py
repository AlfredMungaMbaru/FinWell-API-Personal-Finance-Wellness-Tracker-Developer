from rest_framework import generics, permissions
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse

class TransactionListCreateView(generics.ListCreateAPIView):
	permission_classes = [permissions.IsAuthenticated]

	def get_serializer(self, *args, **kwargs):
		kwargs['user'] = self.request.user
		return TransactionSerializer(*args, **kwargs)

	def get_queryset(self):
		# Optimize with select_related to reduce N+1 queries
		return Transaction.objects.filter(user=self.request.user).select_related('category', 'user')

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	@extend_schema(
		summary="List user transactions",
		description="Retrieve all transactions for the authenticated user with budget alerts.",
		responses={
			200: TransactionSerializer(many=True),
			401: OpenApiResponse(description="Authentication required")
		}
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Create a new transaction",
		description="Create a new transaction for the authenticated user. Returns budget alerts if spending is nearing/exceeding budget limits.",
		request=TransactionSerializer,
		responses={
			201: TransactionSerializer,
			400: OpenApiResponse(description="Bad request - validation errors"),
			401: OpenApiResponse(description="Authentication required")
		}
	)
	def post(self, request, *args, **kwargs):
		return super().post(request, *args, **kwargs)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [permissions.IsAuthenticated]

	def get_serializer(self, *args, **kwargs):
		kwargs['user'] = self.request.user
		return TransactionSerializer(*args, **kwargs)

	def get_queryset(self):
		# Optimize with select_related to reduce N+1 queries
		return Transaction.objects.filter(user=self.request.user).select_related('category', 'user')

	@extend_schema(
		summary="Get transaction details",
		description="Retrieve details of a specific transaction with budget alerts.",
		responses={
			200: TransactionSerializer,
			401: OpenApiResponse(description="Authentication required"),
			404: OpenApiResponse(description="Transaction not found")
		}
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Update transaction",
		description="Update an existing transaction. Returns updated budget alerts if spending changes.",
		request=TransactionSerializer,
		responses={
			200: TransactionSerializer,
			400: OpenApiResponse(description="Bad request - validation errors"),
			401: OpenApiResponse(description="Authentication required"),
			404: OpenApiResponse(description="Transaction not found")
		}
	)
	def put(self, request, *args, **kwargs):
		return super().put(request, *args, **kwargs)

	@extend_schema(
		summary="Delete transaction",
		description="Delete an existing transaction.",
		responses={
			204: OpenApiResponse(description="Transaction deleted successfully"),
			401: OpenApiResponse(description="Authentication required"),
			404: OpenApiResponse(description="Transaction not found")
		}
	)
	def delete(self, request, *args, **kwargs):
		return super().delete(request, *args, **kwargs)
