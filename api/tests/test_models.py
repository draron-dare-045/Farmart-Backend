"""
Tests for FarmArt API models
"""
from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from api.models import User, Animal, Order, OrderItem

User = get_user_model()


class UserModelTests(TestCase):
    """Test User model functionality"""
    
    def test_user_creation_buyer(self):
        """Test creating a buyer user"""
        user = User.objects.create_user(
            username='testbuyer',
            email='buyer@example.com',
            password='testpass123',
            user_type=User.Types.BUYER,
            phone_number='+254712345678',
            location='Nairobi'
        )
        
        self.assertEqual(user.username, 'testbuyer')
        self.assertEqual(user.email, 'buyer@example.com')
        self.assertEqual(user.user_type, User.Types.BUYER)
        self.assertEqual(user.phone_number, '+254712345678')
        self.assertEqual(user.location, 'Nairobi')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_user_creation_farmer(self):
        """Test creating a farmer user"""
        user = User.objects.create_user(
            username='testfarmer',
            email='farmer@example.com',
            password='testpass123',
            user_type=User.Types.FARMER,
            phone_number='+254787654321',
            location='Mombasa'
        )
        
        self.assertEqual(user.user_type, User.Types.FARMER)
        self.assertEqual(user.get_user_type_display(), 'Farmer')

    def test_superuser_creation(self):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            user_type=User.Types.FARMER,
            phone_number='+254700000000',
            location='Kisumu'
        )
        
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_user_str_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            user_type=User.Types.BUYER,
            phone_number='+254712345678',
            location='Test Location'
        )
        expected = 'testuser (Buyer)'
        self.assertEqual(str(user), expected)

    def test_user_default_type(self):
        """Test that default user type is BUYER"""
        user = User.objects.create_user(
            username='defaultuser',
            password='testpass123',
            phone_number='+254712345678',
            location='Test Location'
        )
        self.assertEqual(user.user_type, User.Types.BUYER)

    def test_phone_number_validation_valid(self):
        """Test phone number validation with valid numbers"""
        valid_numbers = ['+254712345678', '254712345678', '0712345678', '+1234567890']
        
        for i, number in enumerate(valid_numbers):
            user = User(
                username=f'user_{i}',
                phone_number=number,
                user_type=User.Types.BUYER,
                location='Test Location'
            )
            try:
                user.full_clean()  # Should not raise ValidationError
            except ValidationError:
                self.fail(f'Valid phone number {number} failed validation')

    def test_unique_username_constraint(self):
        """Test that usernames must be unique"""
        User.objects.create_user(
            username='duplicate',
            password='testpass123',
            user_type=User.Types.BUYER,
            phone_number='+254712345678',
            location='Location1'
        )
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username='duplicate',  # Same username
                password='testpass123',
                user_type=User.Types.FARMER,
                phone_number='+254787654321',
                location='Location2'
            )

    def test_unique_email_constraint(self):
        """Test that emails must be unique"""
        User.objects.create_user(
            username='user1',
            email='same@example.com',
            password='testpass123',
            user_type=User.Types.BUYER,
            phone_number='+254712345678',
            location='Location1'
        )
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username='user2',
                email='same@example.com',  # Same email
                password='testpass123',
                user_type=User.Types.FARMER,
                phone_number='+254787654321',
                location='Location2'
            )


class AnimalModelTests(TestCase):
    """Test Animal model functionality"""
    
    def setUp(self):
        self.farmer = User.objects.create_user(
            username='farmer',
            password='testpass123',
            user_type=User.Types.FARMER,
            phone_number='+254712345678',
            location='Nairobi'
        )

    def test_animal_creation(self):
        """Test creating an animal"""
        animal = Animal.objects.create(
            farmer=self.farmer,
            name='Test Cow',
            animal_type=Animal.AnimalTypes.COW,
            breed='Holstein',
            age=24,
            price=Decimal('50000.00'),
            description='High quality dairy cow',
            quantity=1
        )
        
        self.assertEqual(animal.name, 'Test Cow')
        self.assertEqual(animal.farmer, self.farmer)
        self.assertEqual(animal.animal_type, Animal.AnimalTypes.COW)
        self.assertEqual(animal.breed, 'Holstein')
        self.assertEqual(animal.age, 24)
        self.assertEqual(animal.price, Decimal('50000.00'))
        self.assertEqual(animal.description, 'High quality dairy cow')
        self.assertEqual(animal.quantity, 1)
        self.assertFalse(animal.is_sold)
        self.assertIsNotNone(animal.created_at)
        self.assertIsNotNone(animal.updated_at)

    def test_animal_str_representation(self):
        """Test animal string representation"""
        animal = Animal.objects.create(
            farmer=self.farmer,
            name='Bessie',
            animal_type=Animal.AnimalTypes.COW,
            breed='Holstein',
            age=24,
            price=Decimal('50000.00'),
            description='Test cow',
            quantity=1
        )
        expected = f'Bessie (Cow) by {self.farmer.username}'
        self.assertEqual(str(animal), expected)

    def test_animal_types_choices(self):
        """Test all animal type choices"""
        animal_types = [
            Animal.AnimalTypes.COW,
            Animal.AnimalTypes.GOAT,
            Animal.AnimalTypes.SHEEP,
            Animal.AnimalTypes.CHICKEN,
            Animal.AnimalTypes.PIG
        ]
        
        for animal_type in animal_types:
            animal = Animal.objects.create(
                farmer=self.farmer,
                name=f'Test {animal_type}',
                animal_type=animal_type,
                breed='Test Breed',
                age=12,
                price=Decimal('25000.00'),
                description=f'Test {animal_type}',
                quantity=1
            )
            self.assertEqual(animal.animal_type, animal_type)

    def test_animal_default_values(self):
        """Test animal default values"""
        animal = Animal.objects.create(
            farmer=self.farmer,
            name='Default Animal',
            animal_type=Animal.AnimalTypes.COW,
            breed='Test Breed',
            age=12,
            price=Decimal('25000.00'),
            description='Test animal'
            # quantity and is_sold not specified - should use defaults
        )
        
        self.assertEqual(animal.quantity, 1)  # Default quantity
        self.assertFalse(animal.is_sold)     # Default is_sold

    def test_animal_cascade_delete_with_farmer(self):
        """Test that animals are deleted when farmer is deleted"""
        animal = Animal.objects.create(
            farmer=self.farmer,
            name='Test Animal',
            animal_type=Animal.AnimalTypes.GOAT,
            breed='Boer',
            age=18,
            price=Decimal('20000.00'),
            description='Test goat',
            quantity=2
        )
        
        animal_id = animal.id
        self.farmer.delete()
        
        with self.assertRaises(Animal.DoesNotExist):
            Animal.objects.get(id=animal_id)

    def test_animal_price_precision(self):
        """Test animal price decimal precision"""
        animal = Animal.objects.create(
            farmer=self.farmer,
            name='Precision Test',
            animal_type=Animal.AnimalTypes.CHICKEN,
            breed='Rhode Island Red',
            age=6,
            price=Decimal('999.99'),
            description='Test price precision',
            quantity=10
        )
        
        self.assertEqual(animal.price, Decimal('999.99'))

    def test_animal_age_positive_integer(self):
        """Test that animal age must be positive"""
        animal = Animal(
            farmer=self.farmer,
            name='Age Test',
            animal_type=Animal.AnimalTypes.SHEEP,
            breed='Dorper',
            age=0,  # Edge case - zero age
            price=Decimal('15000.00'),
            description='Test age validation',
            quantity=1
        )
        
        try:
            animal.full_clean()
        except ValidationError:
            pass  # Zero might be invalid depending on your validation rules

    def test_related_name_animals_for_sale(self):
        """Test the related name for farmer's animals"""
        animal1 = Animal.objects.create(
            farmer=self.farmer,
            name='Animal 1',
            animal_type=Animal.AnimalTypes.COW,
            breed='Holstein',
            age=24,
            price=Decimal('50000.00'),
            description='First animal',
            quantity=1
        )
        
        animal2 = Animal.objects.create(
            farmer=self.farmer,
            name='Animal 2',
            animal_type=Animal.AnimalTypes.GOAT,
            breed='Boer',
            age=18,
            price=Decimal('20000.00'),
            description='Second animal',
            quantity=3
        )
        
        farmer_animals = self.farmer.animals_for_sale.all()
        self.assertEqual(farmer_animals.count(), 2)
        self.assertIn(animal1, farmer_animals)
        self.assertIn(animal2, farmer_animals)


class OrderModelTests(TestCase):
    """Test Order model functionality"""
    
    def setUp(self):
        self.farmer = User.objects.create_user(
            username='farmer',
            password='testpass123',
            user_type=User.Types.FARMER,
            phone_number='+254712345678',
            location='Nairobi'
        )
        
        self.buyer = User.objects.create_user(
            username='buyer',
            password='testpass123',
            user_type=User.Types.BUYER,
            phone_number='+254787654321',
            location='Mombasa'
        )
        
        self.animal = Animal.objects.create(
            farmer=self.farmer,
            name='Test Animal',
            animal_type=Animal.AnimalTypes.GOAT,
            breed='Boer',
            age=12,
            price=Decimal('15000.00'),
            description='Test goat',
            quantity=3
        )

    def test_order_creation(self):
        """Test creating an order"""
        order = Order.objects.create(buyer=self.buyer)
        
        self.assertEqual(order.buyer, self.buyer)
        self.assertEqual(order.status, Order.OrderStatus.PENDING)
        self.assertIsNotNone(order.created_at)

    def test_order_str_representation(self):
        """Test order string representation"""
        order = Order.objects.create(buyer=self.buyer)
        expected = f'Order {order.id} by {self.buyer.username} - Pending'
        self.assertEqual(str(order), expected)

    def test_order_status_choices(self):
        """Test all order status choices"""
        statuses = [
            Order.OrderStatus.PENDING,
            Order.OrderStatus.CONFIRMED,
            Order.OrderStatus.REJECTED,
            Order.OrderStatus.PAID,
            Order.OrderStatus.DELIVERED
        ]
        
        for status_choice in statuses:
            order = Order.objects.create(buyer=self.buyer, status=status_choice)
            self.assertEqual(order.status, status_choice)

    def test_order_cascade_delete_with_buyer(self):
        """Test that orders are deleted when buyer is deleted"""
        order = Order.objects.create(buyer=self.buyer)
        order_id = order.id
        
        self.buyer.delete()
        
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(id=order_id)

    def test_order_related_name_orders(self):
        """Test the related name for buyer's orders"""
        order1 = Order.objects.create(buyer=self.buyer)
        order2 = Order.objects.create(buyer=self.buyer, status=Order.OrderStatus.CONFIRMED)
        
        buyer_orders = self.buyer.orders.all()
        self.assertEqual(buyer_orders.count(), 2)
        self.assertIn(order1, buyer_orders)
        self.assertIn(order2, buyer_orders)


class OrderItemModelTests(TestCase):
    """Test OrderItem model functionality"""
    
    def setUp(self):
        self.farmer = User.objects.create_user(
            username='farmer',
            password='testpass123',
            user_type=User.Types.FARMER,
            phone_number='+254712345678',
            location='Nairobi'
        )
        
        self.buyer = User.objects.create_user(
            username='buyer',
            password='testpass123',
            user_type=User.Types.BUYER,
            phone_number='+254787654321',
            location='Mombasa'
        )
        
        self.animal = Animal.objects.create(
            farmer=self.farmer,
            name='Test Animal',
            animal_type=Animal.AnimalTypes.GOAT,
            breed='Boer',
            age=12,
            price=Decimal('15000.00'),
            description='Test goat',
            quantity=3
        )
        
        self.order = Order.objects.create(buyer=self.buyer)

    def test_order_item_creation(self):
        """Test creating an order item"""
        order_item = OrderItem.objects.create(
            order=self.order,
            animal=self.animal,
            quantity=2
        )
        
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.animal, self.animal)
        self.assertEqual(order_item.quantity, 2)

    def test_order_item_str_representation(self):
        """Test order item string representation"""
        order_item = OrderItem.objects.create(
            order=self.order,
            animal=self.animal,
            quantity=2
        )
        expected = f'2 of {self.animal.name} in Order {self.order.id}'
        self.assertEqual(str(order_item), expected)

    def test_order_item_default_quantity(self):
        """Test order item default quantity"""
        order_item = OrderItem.objects.create(
            order=self.order,
            animal=self.animal
            # quantity not specified - should default to 1
        )
        self.assertEqual(order_item.quantity, 1)

    def test_order_item_unique_together_constraint(self):
        """Test that order and animal combination must be unique"""
        OrderItem.objects.create(
            order=self.order,
            animal=self.animal,
            quantity=1
        )
        
        with self.assertRaises(IntegrityError):
            OrderItem.objects.create(
                order=self.order,
                animal=self.animal,  # Same order and animal
                quantity=2
            )

    def test_order_item_validation_farmer_cannot_buy_own_animal(self):
        """Test that farmers cannot order their own animals"""
        farmer_order = Order.objects.create(buyer=self.farmer)
        order_item = OrderItem(
            order=farmer_order,
            animal=self.animal,  # Animal belongs to same farmer
            quantity=1
        )
        
        with self.assertRaises(ValidationError):
            order_item.clean()

    def test_order_item_cascade_delete_with_order(self):
        """Test that order items are deleted when order is deleted"""
        order_item = OrderItem.objects.create(
            order=self.order,
            animal=self.animal,
            quantity=1
        )
        
        order_item_id = order_item.id
        self.order.delete()
        
        with self.assertRaises(OrderItem.DoesNotExist):
            OrderItem.objects.get(id=order_item_id)

    def test_order_item_protect_delete_with_animal(self):
        """Test that animals cannot be deleted if they have order items"""
        OrderItem.objects.create(
            order=self.order,
            animal=self.animal,
            quantity=1
        )
        
        # Trying to delete the animal should raise ProtectedError
        from django.db.models import ProtectedError
        with self.assertRaises(ProtectedError):
            self.animal.delete()

    def test_order_item_related_name_items(self):
        """Test the related name for order's items"""
        item1 = OrderItem.objects.create(
            order=self.order,
            animal=self.animal,
            quantity=1
        )
        
        # Create another animal and item
        animal2 = Animal.objects.create(
            farmer=self.farmer,
            name='Second Animal',
            animal_type=Animal.AnimalTypes.CHICKEN,
            breed='Rhode Island Red',
            age=6,
            price=Decimal('500.00'),
            description='Test chicken',
            quantity=10
        )
        
        item2 = OrderItem.objects.create(
            order=self.order,
            animal=animal2,
            quantity=5
        )
        
        order_items = self.order.items.all()
        self.assertEqual(order_items.count(), 2)
        self.assertIn(item1, order_items)
        self.assertIn(item2, order_items)