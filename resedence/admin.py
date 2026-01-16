from django.contrib import admin
from .models import (
    ResidenceProperty,
    ResidencePropertySetup,
    ResidencePropertyPhoto,
    ResidencePropertyPricing,
    ResidencePropertyLegal
)

# ---------------------------
# Inline for Residence Photos
# ---------------------------
class ResidencePropertyPhotoInline(admin.TabularInline):
    model = ResidencePropertyPhoto
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
# Inline for Property Setup
# ---------------------------
class ResidencePropertySetupInline(admin.StackedInline):
    model = ResidencePropertySetup
    can_delete = False
    verbose_name_plural = 'Property Setup'
    readonly_fields = ('total_beds',)
    fieldsets = (
        (None, {
            'fields': (
                ('number_of_rooms', 'beds_per_room', 'max_guests_per_room', 'total_beds'),
                'number_of_bathrooms',
                'bathroom_types',
                ('has_kitchen', 'kitchen_type', 'has_living_room', 'living_room_size_sqm'),
                'room_types',
                'amenities',
                'accessibility_features',
                ('has_balcony', 'has_storage_room', 'has_laundry_room'),
            )
        }),
    )

# ---------------------------
# Inline for Pricing
# ---------------------------
class ResidencePropertyPricingInline(admin.StackedInline):
    model = ResidencePropertyPricing
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                'base_price',
                'weekly_discount',
                'monthly_discount',
                'cleaning_fee',
                'tax_percentage',
                'currency',
            )
        }),
    )

# ---------------------------
# Inline for Legal
# ---------------------------
class ResidencePropertyLegalInline(admin.StackedInline):
    model = ResidencePropertyLegal
    extra = 0
    fieldsets = (
        ('Legal & Policies', {
            'classes': ('collapse',),
            'fields': (
                'terms_and_conditions',
                'house_rules',
                'cancellation_policy',
                'deposit_policy',
                'refund_rules',
                'insurance_details',
            )
        }),
    )

# ---------------------------
# Main Residence Property Admin
# ---------------------------
@admin.register(ResidenceProperty)
class ResidencePropertyAdmin(admin.ModelAdmin):
    list_display = (
        'property_name',
        'property_type',
        'owner',
        'district',
        'region',
        'country',
        'status',
        'created_at',
    )
    search_fields = (
        'property_name',
        'owner__email',
        'district',
        'region',
    )
    list_filter = (
        'property_type',
        'country',
        'region',
        'status',
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'owner',
                'property_name',
                'property_type',
                'property_description',
                'address',
                ('district', 'region', 'country', 'postal_code'),
                'phone_number',
                'property_size_sqm',
                'year_built',
                'floors',
                'furnished',
                ('parking_available', 'parking_spaces'),
                ('electricity_type', 'water_supply', 'internet_available'),
                ('has_cctv', 'has_security_guard', 'fenced_compound'),
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [
        ResidencePropertySetupInline,
        ResidencePropertyPhotoInline,
        ResidencePropertyPricingInline,
        ResidencePropertyLegalInline,
    ]
