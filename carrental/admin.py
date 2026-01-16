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
                'base_price_per_day',
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
