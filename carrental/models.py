from django.db import models
from django.conf import settings

# ---------------------------------------------------
# Car Rental Main Model
# ---------------------------------------------------
class CarRental(models.Model):
    CAR_TYPE_CHOICES = [
        ('shuffle', 'Shuffles'),
        ('moving_logistic', 'Moving Logistic'),
        ('piki_piki_bajaji', 'Piki Piki/Bajaji'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car_name = models.CharField(max_length=255)
    car_type = models.CharField(max_length=50, choices=CAR_TYPE_CHOICES)
    car_description = models.TextField(blank=True, null=True)
    
    registration_number = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    model_year = models.PositiveIntegerField(blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    seats = models.PositiveIntegerField(default=1)

    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Car features
    has_air_conditioning = models.BooleanField(default=False)
    automatic_transmission = models.BooleanField(default=False)
    fuel_type = models.CharField(max_length=50, blank=True, null=True)
    mileage_km = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car_name} ({self.get_car_type_display()})"


# ---------------------------------------------------
# Car Rental Setup / Features
# ---------------------------------------------------
class CarRentalSetup(models.Model):
    car = models.OneToOneField(CarRental, on_delete=models.CASCADE)

    # Extra features
    has_gps = models.BooleanField(default=False)
    has_radio = models.BooleanField(default=False)
    has_music_system = models.BooleanField(default=False)
    safety_features = models.JSONField(default=list, blank=True)  # e.g. ["Airbags", "ABS"]

    def __str__(self):
        return f"Setup for {self.car.car_name}"


# ---------------------------------------------------
# Car Rental Photos
# ---------------------------------------------------
class CarRentalPhoto(models.Model):
    car = models.ForeignKey(CarRental, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='car_rental_photos/')

    def __str__(self):
        return f"Photo of {self.car.car_name}"


# ---------------------------------------------------
# Car Rental Pricing
# ---------------------------------------------------
class CarRentalPricing(models.Model):
    car = models.OneToOneField(CarRental, on_delete=models.CASCADE)
    base_price_per_day = models.DecimalField(max_digits=12, decimal_places=2)
    weekly_discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    monthly_discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    cleaning_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    currency = models.CharField(max_length=10, default='TZS')

    def __str__(self):
        return f"Pricing for {self.car.car_name}"


# ---------------------------------------------------
# Car Rental Legal / Policies
# ---------------------------------------------------
class CarRentalLegal(models.Model):
    car = models.OneToOneField(CarRental, on_delete=models.CASCADE)

    terms_and_conditions = models.TextField(blank=True, null=True)
    rental_policy = models.TextField(blank=True, null=True)
    cancellation_policy = models.TextField(blank=True, null=True)
    deposit_policy = models.TextField(blank=True, null=True)
    insurance_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Legal Info for {self.car.car_name}"
