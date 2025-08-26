from rest_framework import generics, permissions
from budgets.models import Budget
from budgets.serializers import BudgetSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse

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

    @extend_schema(
        summary="List user budgets",
        description="Retrieve all budgets for the authenticated user with spending calculations.",
        responses={
            200: BudgetSerializer(many=True),
            401: OpenApiResponse(description="Authentication required")
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new budget",
        description="Create a new budget for a specific category and period. Only one budget per category per month is allowed.",
        request=BudgetSerializer,
        responses={
            201: BudgetSerializer,
            400: OpenApiResponse(description="Bad request - validation errors or duplicate budget"),
            401: OpenApiResponse(description="Authentication required")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        kwargs['user'] = self.request.user
        kwargs['context'] = {'request': self.request}
        return BudgetSerializer(*args, **kwargs)

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Get budget details",
        description="Retrieve details of a specific budget including spending calculations.",
        responses={
            200: BudgetSerializer,
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Budget not found")
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update budget",
        description="Update an existing budget's amount, category, or period.",
        request=BudgetSerializer,
        responses={
            200: BudgetSerializer,
            400: OpenApiResponse(description="Bad request - validation errors"),
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Budget not found")
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete budget",
        description="Delete an existing budget.",
        responses={
            204: OpenApiResponse(description="Budget deleted successfully"),
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Budget not found")
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
