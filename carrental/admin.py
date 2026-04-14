from django.contrib import admin
from .models import (
    CarRental,
    CarRentalSetup,
    CarRentalPhoto,
    CarRentalPricing,
    CarRentalLegal,
)

# ---------------------------
# Inline for Car Photos
# ---------------------------
class CarRentalPhotoInline(admin.TabularInline):
    model = CarRentalPhoto
    extra = 3
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="border-radius:5px;" />'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'

# ---------------------------
# Inline for Car Setup / Features
# ---------------------------
class CarRentalSetupInline(admin.StackedInline):
    model = CarRentalSetup
    can_delete = False
    verbose_name_plural = 'Car Setup'
    fieldsets = (
        (None, {
            'fields': (
                ('has_gps', 'has_radio', 'has_music_system'),
                'safety_features',
            )
        }),
    )

# ---------------------------
# Inline for Car Pricing
# ---------------------------
class CarRentalPricingInline(admin.StackedInline):
    model = CarRentalPricing
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                ('base_price_per_day',"max_price_per_day")
                ('weekly_discount', 'monthly_discount'),
                ('cleaning_fee', 'tax_percentage'),
                'currency',
            )
        }),
    )

# ---------------------------
# Inline for Car Legal / Policies
# ---------------------------
class CarRentalLegalInline(admin.StackedInline):
    model = CarRentalLegal
    extra = 0
    fieldsets = (
        ('Legal & Policies', {
            'classes': ('collapse',),
            'fields': (
                'terms_and_conditions',
                'rental_policy',
                'cancellation_policy',
                'deposit_policy',
                'insurance_details',
            )
        }),
    )

# ---------------------------
# Main Car Rental Admin
# ---------------------------
@admin.register(CarRental)
class CarRentalAdmin(admin.ModelAdmin):
    list_display = (
        'car_name',
        'car_type',
        'owner',
        'registration_number',
        'manufacturer',
        'model_year',
        'created_at'
    )
    search_fields = (
        'car_name',
        'owner__email',
        'registration_number',
        'manufacturer',
    )
    list_filter = (
        'car_type',
        'manufacturer',
        'model_year',
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'owner',
                'car_name',
                'car_type',
                'car_description',
                ('registration_number', 'manufacturer', 'model_year', 'color'),
                'seats',
                'phone_number',
                ('has_air_conditioning', 'automatic_transmission', 'fuel_type', 'mileage_km'),
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [
        CarRentalSetupInline,
        CarRentalPhotoInline,
        CarRentalPricingInline,
        CarRentalLegalInline,
    ]

    # Optional: prettier JSONField in admin
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'safety_features':
            kwargs['widget'] = admin.widgets.AdminTextareaWidget(attrs={'rows': 2, 'cols': 40})
        return super().formfield_for_dbfield(db_field, **kwargs)






from django.contrib import admin
from .models import CarBooking


@admin.register(CarBooking)
class CarBookingAdmin(admin.ModelAdmin):

    # ✅ DISPLAY
    list_display = (
        "id",
        "car_name",
        "car_owner_name",
        "car_owner_phone",
        "customer_name",
        "customer_phone_number",
        "pickup_date",
        "pickup_time",
        "pickup_location",
        "dropoff_location",
        "status",
        "created_at",
    )

    # ✅ FILTERS
    list_filter = ("status", "pickup_date", "created_at")

    # ✅ SEARCH
    search_fields = (
        "customer_phone_number",
        "pickup_location",
        "dropoff_location",
        "car__car_name",
        "customer__email",
    )

    # ✅ ORDER
    ordering = ("-created_at",)

    # ✅ READABLE DETAIL PAGE
    fieldsets = (
        ("Booking Info", {
            "fields": ("car", "booking_type", "status")
        }),
        ("Customer Info", {
            "fields": ("customer", "customer_phone_number")
        }),
        ("Trip Details", {
            "fields": ("pickup_date", "pickup_time", "pickup_location", "dropoff_location")
        }),
        ("System", {
            "fields": ("created_at",),
        }),
    )

    readonly_fields = ("created_at",)

    # =====================================================
    # ✅ SAFE METHODS (NO CRASH GUARANTEED)
    # =====================================================

    def car_name(self, obj):
        try:
            return obj.car.car_name if obj.car else "No Car"
        except Exception:
            return "No Car"
    car_name.short_description = "Car"

    def customer_name(self, obj):
        try:
            if obj.customer:
                first = obj.customer.first_name or ""
                last = obj.customer.last_name or ""
                name = f"{first} {last}".strip()
                return name if name else obj.customer.email
            return "Guest"
        except Exception:
            return "Guest"
    customer_name.short_description = "Customer"

    def car_owner_name(self, obj):
        try:
            if obj.car and obj.car.owner:
                owner = obj.car.owner
                first = owner.first_name or ""
                last = owner.last_name or ""
                name = f"{first} {last}".strip()
                return name if name else owner.email
            return "-"
        except Exception:
            return "-"
    car_owner_name.short_description = "Car Owner"

    def car_owner_phone(self, obj):
        try:
            if obj.car and hasattr(obj.car, "phone_number"):
                return obj.car.phone_number
            return "-"
        except Exception:
            return "-"
    car_owner_phone.short_description = "Owner Phone"
