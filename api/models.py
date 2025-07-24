from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class User(AbstractUser):
    """Custom User Model with Buyer/Farmer roles."""
    class Types(models.TextChoices):
        BUYER = 'BUYER', 'Buyer'
        FARMER = 'FARMER', 'Farmer'

    user_type = models.CharField(max_length=50, choices=Types.choices, default=Types.BUYER)
    
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r'^\+?1?\d{9,15}$', 
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    location = models.CharField(max_length=255)
    groups = models.ManyToManyField('auth.Group', related_name='api_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='api_user_set', blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Order(models.Model):
    """Model for customer's orders."""
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        REJECTED = 'REJECTED', 'Rejected'
        PAID = 'PAID', 'Paid'
        DELIVERED = 'DELIVERED', 'Delivered'

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        limit_choices_to={'user_type': User.Types.BUYER}
    )
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.buyer.username} - {self.get_status_display()}"