from rest_framework import serializers
from .models import User, Animal, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    """Serializer for displaying user data."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'phone_number', 'location']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for creating new users. Handles password confirmation."""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'user_type', 'phone_number', 'location')
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user