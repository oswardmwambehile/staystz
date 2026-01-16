from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)

        # Set default user_type to "customer"
        extra_fields.setdefault('user_type', 'customer')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Set user_type to admin for superusers
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        return self.create_user(email, password, **extra_fields)

from django.core.exceptions import ValidationError
import datetime

def validate_nida(value):
    if not value.isdigit() or len(value) != 20:
        raise ValidationError("NIDA number must be exactly 20 digits.")
    
    # Check date validity (first 8 digits)
    try:
        year = int(value[:4])
        month = int(value[4:6])
        day = int(value[6:8])
        datetime.date(year, month, day)
    except ValueError:
        raise ValidationError("First 8 digits of NIDA must be a valid date (YYYYMMDD).")



class User(AbstractBaseUser, PermissionsMixin):
    

    REGION_CHOICES = [
        ('Arusha', 'Arusha'),
        ('Dar es Salaam', 'Dar es Salaam'),
        ('Dodoma', 'Dodoma'),
        ('Geita', 'Geita'),
        ('Iringa', 'Iringa'),
        ('Kagera', 'Kagera'),
        ('Katavi', 'Katavi'),
        ('Kigoma', 'Kigoma'),
        ('Kilimanjaro', 'Kilimanjaro'),
        ('Lindi', 'Lindi'),
        ('Manyara', 'Manyara'),
        ('Mara', 'Mara'),
        ('Mbeya', 'Mbeya'),
        ('Morogoro', 'Morogoro'),
        ('Mtwara', 'Mtwara'),
        ('Mwanza', 'Mwanza'),
        ('Njombe', 'Njombe'),
        ('Pwani', 'Pwani'),
        ('Rukwa', 'Rukwa'),
        ('Ruvuma', 'Ruvuma'),
        ('Shinyanga', 'Shinyanga'),
        ('Simiyu', 'Simiyu'),
        ('Singida', 'Singida'),
        ('Songwe', 'Songwe'),
        ('Tabora', 'Tabora'),
        ('Tanga', 'Tanga'),
        ('Zanzibar', 'Zanzibar'),
    ]

    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        
        ('property_owner', 'Property Owner'),
    ]


    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES, default='customer')
    location = models.CharField(max_length=50, choices=REGION_CHOICES, null=True, blank=True)
    user_verified = models.BooleanField(default=False)

    

    phone_number = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^(?:\+255|0)[67][0-9]\d{7}$',
                message="Enter a valid Tanzanian phone number (e.g. +255712345678 or 0712345678)"
            )
        ]
    )

    
    nida_number = models.CharField(
    max_length=20,
    null=True,
    blank=True,
    validators=[validate_nida]
)
    

    nida_card = models.ImageField(
        upload_to='nida_cards/',
        null=True,
        blank=True
    )
    
    

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.user_type})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name
