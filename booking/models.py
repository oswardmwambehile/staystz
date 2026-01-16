from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class BookingProperty(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('lodge', 'Lodge'),
        ('guest_house', 'Guest House'),
        ('tent or campsite', 'Tent or campsite'),
        
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
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    property_size_sqm = models.PositiveIntegerField(blank=True, null=True)  
    languages_spoken = models.JSONField(default=list, blank=True)  # e.g., ["English", "French"]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.property_name

    class Meta:
        verbose_name = "BookingProperty"
        verbose_name_plural = "Booking Properties"


# Step 2: Property Setup
class BookingPropertySetup(models.Model):
    property = models.OneToOneField(BookingProperty, on_delete=models.CASCADE)
    number_of_rooms = models.IntegerField(default=1)
    beds_per_room = models.IntegerField(default=1)
    max_guests_per_room = models.IntegerField(default=1)
    total_beds = models.IntegerField(blank=True, null=True)
    number_of_bathrooms = models.IntegerField(default=1)
    has_kitchen = models.BooleanField(default=False)
    has_living_room = models.BooleanField(default=False)
    amenities = models.JSONField(default=list, blank=True)  # e.g., ["WiFi", "Parking", "AC"]
    room_types = models.JSONField(default=list, blank=True)  # e.g., ["Single", "Double", "Suite"]
    accessibility_features = models.JSONField(default=list, blank=True)  # e.g., ["Wheelchair accessible"]

    def save(self, *args, **kwargs):
        if not self.total_beds:
            self.total_beds = self.number_of_rooms * self.beds_per_room
        super().save(*args, **kwargs)

class BookingPropertyPhoto(models.Model):
    property = models.ForeignKey(BookingProperty, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='booking_property_photos/')
    

class BookingPropertyPricing(models.Model):
    property = models.OneToOneField(BookingProperty, on_delete=models.CASCADE)
    base_price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField()
    available_to = models.DateField()
    minimum_stay_nights = models.PositiveIntegerField(default=1)
    maximum_stay_nights = models.PositiveIntegerField(blank=True, null=True)

    

class BookingPropertyLegal(models.Model):
    property = models.OneToOneField(BookingProperty, on_delete=models.CASCADE)
    terms_and_conditions = models.TextField(blank=True, null=True)
    house_rules = models.TextField(blank=True, null=True)
    cancellation_policy = models.TextField(blank=True, null=True)
    check_in_policy = models.TextField(blank=True, null=True)
    smoking_policy = models.TextField(blank=True, null=True)
    pet_policy = models.TextField(blank=True, null=True)


from django.db import models
from django.conf import settings
from .models import BookingProperty


class Booking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(BookingProperty, on_delete=models.CASCADE)

    room_type = models.CharField(max_length=100)

    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)

    nights = models.PositiveIntegerField(default=1)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=16, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            # Handle cases where first_name/last_name might be blank
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
            if not full_name:
                full_name = self.user.email  # fallback
            return f"{full_name} booked {self.property.property_name}"

