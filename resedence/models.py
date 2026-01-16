from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class ResidenceProperty(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('frame', 'Frame'),
    ]

    RESEDENCE_STATUS_CHOICES = [
        ('open', 'Open'),
        ('hold', 'Hold'),
        ('closed', 'Closed'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    property_description = models.TextField(blank=True, null=True)

    
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default='Tanzania')
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    # Contact
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Property specifications
    property_size_sqm = models.PositiveIntegerField(blank=True, null=True)
    year_built = models.PositiveIntegerField(blank=True, null=True)
    floors = models.PositiveIntegerField(blank=True, null=True)
    furnished = models.BooleanField(default=False)
    parking_available = models.BooleanField(default=False)
    parking_spaces = models.PositiveIntegerField(blank=True, null=True)

    # Utilities
    electricity_type = models.CharField(max_length=50, blank=True, null=True)
    water_supply = models.CharField(max_length=50, blank=True, null=True)
    internet_available = models.BooleanField(default=False)

    # Security
    has_cctv = models.BooleanField(default=False)
    has_security_guard = models.BooleanField(default=False)
    fenced_compound = models.BooleanField(default=False)

    # System
    status = models.CharField(max_length=20, choices=RESEDENCE_STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResidencePropertySetup(models.Model):
    property = models.OneToOneField(ResidenceProperty, on_delete=models.CASCADE)

    # Rooms & beds
    number_of_rooms = models.IntegerField(default=1)
    beds_per_room = models.IntegerField(default=1)
    max_guests_per_room = models.IntegerField(default=1)
    total_beds = models.IntegerField(blank=True, null=True)

    # Bathroom details
    number_of_bathrooms = models.IntegerField(default=1)
    bathroom_types = models.JSONField(
        default=list,
        blank=True
    )  # e.g. ["Shared", "Private", "Ensuite"]

    # Kitchen & living
    has_kitchen = models.BooleanField(default=False)
    kitchen_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[
            ('private', 'Private Kitchen'),
            ('shared', 'Shared Kitchen'),
            ('none', 'No Kitchen'),
        ]
    )
    has_living_room = models.BooleanField(default=False)
    living_room_size_sqm = models.PositiveIntegerField(blank=True, null=True)

    # Room types (Bedrooms)
    room_types = models.JSONField(
        default=list,
        blank=True
    )  # e.g. ["Single Room", "Double Room", "Master Bedroom"]

    # Amenities
    amenities = models.JSONField(
        default=list,
        blank=True
    )  # e.g. ["WiFi", "Parking", "TV", "AC", "Fridge"]

    # Accessibility features
    accessibility_features = models.JSONField(
        default=list,
        blank=True
    )  # e.g ["Wheelchair Ramp", "Wide Doors"]

    # Extra features
    has_balcony = models.BooleanField(default=False)
    has_storage_room = models.BooleanField(default=False)
    has_laundry_room = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.total_beds:
            self.total_beds = self.number_of_rooms * self.beds_per_room
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Setup for {self.property.property_name}"


class ResidencePropertyPhoto(models.Model):
    property = models.ForeignKey(
        ResidenceProperty,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    image = models.ImageField(upload_to='residence_property_photos/')
    
    def __str__(self):
        return f"Photo of {self.property.property_name}"


class ResidencePropertyPricing(models.Model):
    property = models.OneToOneField(ResidenceProperty, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=15, decimal_places=2)
    weekly_discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    monthly_discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    cleaning_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    currency = models.CharField(max_length=10, default="TZS")

    def __str__(self):
        return f"Pricing for {self.property.property_name}"


class ResidencePropertyLegal(models.Model):
    property = models.OneToOneField(ResidenceProperty, on_delete=models.CASCADE)

    terms_and_conditions = models.TextField(blank=True, null=True)
    house_rules = models.TextField(blank=True, null=True)
    cancellation_policy = models.TextField(blank=True, null=True)

    # Additional legal items
    deposit_policy = models.TextField(blank=True, null=True)
    refund_rules = models.TextField(blank=True, null=True)
    insurance_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Legal Info for {self.property.property_name}"
