from rest_framework import serializers
from .models import User, Animal, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'phone_number', 'location']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'user_type', 'phone_number', 'location')
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    class AnimalSerializer(serializers.ModelSerializer):
        farmer_username = serializers.CharField(source='farmer.username', read_only=True)

    class Meta:
        model = Animal
        fields = [
            'id', 'farmer', 'farmer_username', 'name', 'animal_type', 'breed',
            'age', 'price', 'description', 'image', 
            'is_sold', 'quantity', 'created_at', 'updated_at'
        ]
        read_only_fields = ['farmer', 'is_sold']

class OrderItemReadSerializer(serializers.ModelSerializer):
    """Serializer for displaying items within an order."""
    name = serializers.CharField(source='animal.name', read_only=True)
    price = serializers.DecimalField(source='animal.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'animal', 'name', 'price', 'quantity']


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'buyer_username', 'status', 'created_at', 'items', 'total_price']

    def get_total_price(self, order):
        """Calculate the total price of all items in the order."""
        return sum(item.animal.price * item.quantity for item in order.items.all())