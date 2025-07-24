from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import transaction
from . import mpesa_api

from .models import Animal, Order, OrderItem
from .serializers import (
    AnimalSerializer,
    OrderReadSerializer, OrderWriteSerializer,
    UserSerializer,
    UserRegistrationSerializer
)
from .permissions import IsFarmerOrReadOnly, IsOwnerOrAdmin
from . import mpesa_api

User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    class AnimalViewSet(viewsets.ModelViewSet):
        queryset = Animal.objects.filter(is_sold=False).order_by('-created_at')
        serializer_class = AnimalSerializer
        permission_classes = [permissions.IsAuthenticated, IsFarmerOrReadOnly]

    def perform_create(self, serializer): 
        serializer.save(farmer=self.request.user)