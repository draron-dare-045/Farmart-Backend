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
    """Serializer for the Animal model that handles file uploads and URL generation."""
    farmer_username = serializers.CharField(source='farmer.username', read_only=True)
    image = serializers.ImageField(required=False, use_url=True)

    class Meta:
        model = Animal
        fields = [
            'id', 'farmer', 'farmer_username', 'name', 'animal_type', 'breed',
            'age', 'price', 'description', 'image', 
            'is_sold', 'quantity', 'created_at', 'updated_at'
        ]
        read_only_fields = ['farmer', 'is_sold']

    def to_representation(self, instance):
        """Formats the output to convert the image field to its full URL."""
        representation = super().to_representation(instance)
        if instance.image and hasattr(instance.image, 'url'):
            representation['image'] = instance.image.url
        else:
            representation['image'] = None
        return representation
    
class OrderItemReadSerializer(serializers.ModelSerializer):
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
        return sum(item.animal.price * item.quantity for item in order.items.all())

class OrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['animal', 'quantity']

class OrderWriteSerializer(serializers.ModelSerializer):
    items = OrderItemWriteSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items'] 

    def create(self, validated_data):
        """
        This method correctly handles the creation of an Order and its nested OrderItems.
        """

        items_data = validated_data.pop('items')
        
        buyer = self.context['request'].user
        order = Order.objects.create(buyer=buyer, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        return order
    
class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """
    A dedicated serializer specifically for updating only the status of an Order.
    """
    class Meta:
        model = Order
        fields = ['status']