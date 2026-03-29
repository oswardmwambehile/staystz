from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class ResidenceProperty(models.Model):
    TANZANIA_REGIONS = [
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
            ('Pwani', 'Pwani (Coast)'),
            ('Rukwa', 'Rukwa'),
            ('Ruvuma', 'Ruvuma'),
            ('Shinyanga', 'Shinyanga'),
            ('Simiyu', 'Simiyu'),
            ('Singida', 'Singida'),
            ('Songwe', 'Songwe'),
            ('Tabora', 'Tabora'),
            ('Tanga', 'Tanga'),
            ('Zanzibar North', 'Zanzibar North'),
            ('Zanzibar South', 'Zanzibar South'),
            ('Zanzibar Central/South', 'Zanzibar Central/South'),
            ('Zanzibar Urban/West', 'Zanzibar Urban/West'),

    ]
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('homes', 'Homes'),
        ('office_space', 'Office Space'),  # ✅ FIXED
    ]


    RESEDENCE_STATUS_CHOICES = [
        ('open', 'Open'),
        ('hold', 'Hold'),
        ('closed', 'Closed'),
    ]


    ELECTRICITY_USAGE_CHOICES = [
        ('private', 'Private (Only You)'),
        ('shared', 'Shared'),
    ]

    AIRBNB_CHOICES = [
    ("yes", "Yes"),
    ("no", "No"),
   ]
    BUILDING_LEVEL_CHOICES = [
        ('ground_floor', 'Ground Floor'),
        ('storey_building', 'Storey Building'),
    ]




    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    airbnb_available = models.CharField(
    max_length=3,
    choices=AIRBNB_CHOICES,
    blank=True,
    null=True
)
    property_description = models.TextField(blank=True, null=True)


    address = models.CharField(max_length=255)
    region =  models.CharField(
        max_length=50,
        choices=TANZANIA_REGIONS
    )
    district = models.CharField(max_length=100)
    country = models.CharField(max_length=50, default='Tanzania')
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    # Contact
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Property specifications
    property_size_sqm = models.PositiveIntegerField(blank=True, null=True)
    year_built = models.PositiveIntegerField(blank=True, null=True)
    # 7. Office location in building
    building_level = models.CharField(
        max_length=20,
        choices=BUILDING_LEVEL_CHOICES
    )
    floors = models.PositiveIntegerField(blank=True, null=True)

    furnished = models.BooleanField(default=False)
    parking_available = models.BooleanField(default=False)
    parking_spaces = models.PositiveIntegerField(blank=True, null=True)

    # Utilities
    electricity_type = models.CharField(
        max_length=20,
        choices=ELECTRICITY_USAGE_CHOICES,
        blank=True,
        null=True
    )
    water_supply =models.CharField(
        max_length=20,
        choices=ELECTRICITY_USAGE_CHOICES,
        blank=True,
        null=True
    )

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


    cleaning_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)


    # For office space only
    min_months = models.PositiveIntegerField(blank=True, null=True)
    max_months = models.PositiveIntegerField(blank=True, null=True)

    currency = models.CharField(max_length=10, default="TZS")

    RENT_DURATION_CHOICES = [
        (3, "3 Months"),
        (6, "6 Months"),
        (12, "12 Months"),
    ]
    rent_duration = models.IntegerField(choices=RENT_DURATION_CHOICES)

    def __str__(self):
        return f"Pricing for {self.property.property_name}"

from django.db import models

class OfficePropertySetup(models.Model):

    BUILDING_CONDITION_CHOICES = [
        ('new', 'New'),
        ('old', 'Old'),
        ('very_old', 'Very Old'),
    ]

    FLOOR_FINISH_CHOICES = [
        ('tiles', 'Tiles'),
        ('normal_floor', 'Normal Floor'),
    ]

    DOOR_TYPE_CHOICES = [
        ('glass_grill', 'Glass & Grill'),
        ('iron_grill', 'Iron Sheet & Grill'),
        ('grill_only', 'Grill Only'),
    ]

    TOILET_TYPE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    FAN_AC_CHOICES = [
        ('fan', 'Fan'),
        ('ac', 'Air Conditioner'),
        ('none', 'None'),
    ]

    CEILING_TYPE_CHOICES = [
        ('ceiling_board', 'Ceiling Board'),
        ('gypsum', 'Gypsum'),
        ('none', 'None'),
    ]

    WINDOW_TYPE_CHOICES = [
        ('glass', 'Glass Windows'),
        ('wire_mesh', 'Wire Mesh Windows'),
        ('none', 'No Windows'),
    ]

    ROAD_TYPE_CHOICES = [
        ('main_road', 'Main Road'),
        ('street_road', 'Street Road'),
    ]

    ENVIRONMENT_CHOICES = [
        ('quiet', 'Quiet'),
        ('moderate_noise', 'Moderate Noise'),
        ('normal', 'Normal'),
    ]

    LOCATION_CATEGORY_CHOICES = [
        ('city_center', 'City Center'),
        ('residential_area', 'Residential/Uswahilini'),
        ('normal', 'Normal'),
    ]

    DOOR_LOCK_CONDITION_CHOICES = [
        ('good', 'Good'),
        ('needs_repair', 'Needs Repair'),
    ]

    property = models.OneToOneField(
        "ResidenceProperty",
        on_delete=models.CASCADE,
        related_name="office_setup"
    )

    # 1. Building condition
    building_condition = models.CharField(
        max_length=20,
        choices=BUILDING_CONDITION_CHOICES
    )

    # 2. Floor finish
    floor_finish = models.CharField(
        max_length=20,
        choices=FLOOR_FINISH_CHOICES
    )

    # 3. Door type
    door_type = models.CharField(
        max_length=20,
        choices=DOOR_TYPE_CHOICES
    )

    # 4. Office size (sqm)
    office_size_sqm = models.PositiveIntegerField()

    # 5. Number of tenants
    number_of_tenants = models.PositiveIntegerField(default=1)

    # 6. Toilet type
    toilet_available = models.CharField(
        max_length=20,
        choices=TOILET_TYPE_CHOICES
    )



    # 8. Water service available
    has_water = models.BooleanField(default=True)

    # 9. Electricity service available
    has_electricity = models.BooleanField(default=True)

    # 10. Electricity usage type

    # 11. Fan / AC / None
    fan_or_ac = models.CharField(
        max_length=20,
        choices=FAN_AC_CHOICES,
        default="none"
    )

    # 12. Ceiling type
    ceiling_type = models.CharField(
        max_length=20,
        choices=CEILING_TYPE_CHOICES,
        default="none"
    )



    # 14. Window type
    window_type = models.CharField(
        max_length=20,
        choices=WINDOW_TYPE_CHOICES,
        default="none"
    )



    # 16. Door locks condition
    door_lock_condition = models.CharField(
        max_length=20,
        choices=DOOR_LOCK_CONDITION_CHOICES
    )

    # 17. Road type
    road_type = models.CharField(
        max_length=20,
        choices=ROAD_TYPE_CHOICES
    )

    # 18. Environment
    environment = models.CharField(
        max_length=20,
        choices=ENVIRONMENT_CHOICES
    )

    # 19. Office location category
    location_category = models.CharField(
        max_length=20,
        choices=LOCATION_CATEGORY_CHOICES
    )

    # Extra fields
    number_of_offices = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Office Setup for {self.property.property_name}"






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




from django.db import models
from django.conf import settings

class ResidenceBooking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey('ResidenceProperty', on_delete=models.CASCADE)

    # For residence: user chooses rent duration in months
    RENT_DURATION_CHOICES = [
        (3, "3 Months"),
        (6, "6 Months"),
        (12, "12 Months"),
    ]
    rent_duration = models.IntegerField(choices=RENT_DURATION_CHOICES)

    phone_number = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} booked {self.property.property_name} for {self.rent_duration} months"
