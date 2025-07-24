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
    

    class Animal(models.Model):

        class AnimalTypes(models.TextChoices):
            COW = 'COW', 'Cow'
            GOAT = 'GOAT', 'Goat'
            SHEEP = 'SHEEP', 'Sheep'
            CHICKEN = 'CHICKEN', 'Chicken'
            PIG = 'PIG', 'Pig'

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='animals_for_sale',
        limit_choices_to={'user_type': User.Types.FARMER}
    )
    name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=50, choices=AnimalTypes.choices)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField(help_text="Age in months")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='animal_images/', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_animal_type_display()}) by {self.farmer.username}"