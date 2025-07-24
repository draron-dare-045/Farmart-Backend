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

class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Orders."""
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        """Use different serializers for reading vs. writing data."""
        if self.action in ['create', 'update', 'partial_update']:
            return OrderWriteSerializer
        return OrderReadSerializer

    def get_queryset(self):
        """
        Filter orders based on the user's role.
        """
        user = self.request.user
        queryset = super().get_queryset().prefetch_related('items__animal')

        if user.is_staff:
            return queryset
        if user.user_type == User.Types.FARMER:
            return queryset.filter(items__animal__farmer=user).distinct()
        return queryset.filter(buyer=user)

    def perform_create(self, serializer):
        """
        Set the buyer to the currently logged-in user when creating an order.
        """
        if self.request.user.user_type != User.Types.BUYER:
            raise permissions.PermissionDenied("Only Buyers can create orders.")
        serializer.save(buyer=self.request.user, status=Order.OrderStatus.CONFIRMED)