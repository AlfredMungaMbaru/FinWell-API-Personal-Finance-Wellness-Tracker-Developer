from rest_framework import generics, permissions
from categories.models import Category
from categories.serializers import CategorySerializer

class CategoryListCreateView(generics.ListCreateAPIView):
	serializer_class = CategorySerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Category.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = CategorySerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Category.objects.filter(user=self.request.user)
