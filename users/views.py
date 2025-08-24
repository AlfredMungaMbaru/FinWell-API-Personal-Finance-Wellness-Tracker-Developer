from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
	pass

class ProfileView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		serializer = UserProfileSerializer(request.user)
		return Response(serializer.data)

	def put(self, request):
		serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
