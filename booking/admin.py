from django.contrib import admin
from .models import (
    BookingProperty,
    BookingPropertySetup,
    BookingPropertyPhoto,
    BookingPropertyPricing,
    BookingPropertyLegal
)

# ---------------------------
# Inline for Property Photos
# ---------------------------
class BookingPropertyPhotoInline(admin.TabularInline):
    model = BookingPropertyPhoto
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
class BookingPropertySetupInline(admin.StackedInline):
    model = BookingPropertySetup
    can_delete = False
    verbose_name_plural = 'Property Setup'
    readonly_fields = ('total_beds',)
    fieldsets = (
        (None, {
            'fields': (
                ('number_of_rooms', 'beds_per_room', 'max_guests_per_room', 'total_beds'),
                'number_of_bathrooms',
                ('has_kitchen', 'has_living_room'),
                'amenities',
                'room_types',
                'accessibility_features',
            )
        }),
    )
    # For JSONField multi-selection look nicer, use horizontal filter if ManyToManyField
    # filter_horizontal = ('amenities', 'room_types', 'accessibility_features')


# ---------------------------
# Inline for Pricing
# ---------------------------
class BookingPropertyPricingInline(admin.StackedInline):
    model = BookingPropertyPricing
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                'base_price_per_night',
                ('available_from', 'available_to'),
                ('minimum_stay_nights', 'maximum_stay_nights'),
            )
        }),
    )


# ---------------------------
# Inline for Legal
# ---------------------------
class BookingPropertyLegalInline(admin.StackedInline):
    model = BookingPropertyLegal
    extra = 0
    fieldsets = (
        ('Legal & Policies', {
            'classes': ('collapse',),
            'fields': (
                'terms_and_conditions',
                'house_rules',
                'cancellation_policy',
                'check_in_policy',
                'smoking_policy',
                'pet_policy',
            )
        }),
    )


# ---------------------------
# Main Property Admin
# ---------------------------
@admin.register(BookingProperty)
class BookingPropertyAdmin(admin.ModelAdmin):
    list_display = (
        'property_name',
        'property_type',
        'owner',
        'district',
        'region',
        'country',
        'created_at'
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
                'languages_spoken',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [
        BookingPropertySetupInline,
        BookingPropertyPhotoInline,
        BookingPropertyPricingInline,
        BookingPropertyLegalInline,
    ]

    # Optional: make JSONField prettier in admin
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'languages_spoken':
            kwargs['widget'] = admin.widgets.AdminTextareaWidget(attrs={'rows': 2, 'cols': 40})
        return super().formfield_for_dbfield(db_field, **kwargs)
    


from django.contrib import admin
from django.utils.html import format_html
from .models import Booking


from django.contrib import admin
from django.utils.html import format_html
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    # =========================
    # LIST PAGE (TABLE VIEW)
    # =========================
    list_display = (
        "id",
        "user_full_name",  # <- custom method
        "property",
        "room_type",
        "check_in",
        "check_out",
        "guests",
        "colored_status",
        "total_price",
        "created_at",
    )

    # Columns you can click to go to detail page
    list_display_links = ("id", "user_full_name", "property")

    list_filter = (
        "status",
        "room_type",
        "check_in",
        "created_at",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "property__property_name",
        "room_type",
    )

    date_hierarchy = "created_at"

    ordering = ("-created_at",)

    list_per_page = 25

    list_select_related = ("user", "property")

    # =========================
    # READ-ONLY FIELDS
    # =========================
    readonly_fields = (
        "nights",
        "total_price",
        "created_at",
    )

    # =========================
    # FORM LAYOUT (DETAIL VIEW)
    # =========================
    fieldsets = (
        ("👤 Customer Information", {
            "fields": ("user",)
        }),
        ("🏠 Property Information", {
            "fields": ("property", "room_type")
        }),
        ("📅 Booking Dates", {
            "fields": ("check_in", "check_out", "nights")
        }),
        ("👥 Guests", {
            "fields": ("guests",)
        }),
        ("💰 Pricing", {
            "fields": ("price_per_night", "total_price")
        }),
        ("📌 Booking Status", {
            "fields": ("status",)
        }),
        ("🕒 System Info", {
            "fields": ("created_at",)
        }),
    )

    # =========================
    # CUSTOM STATUS COLOR
    # =========================
    def colored_status(self, obj):
        color_map = {
            "pending": "orange",
            "confirmed": "green",
            "cancelled": "red",
            "completed": "blue",
        }
        color = color_map.get(obj.status, "black")
        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            obj.status.upper()
        )

    colored_status.short_description = "Status"

    # =========================
    # CUSTOM METHOD FOR FULL NAME
    # =========================
    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    user_full_name.short_description = "Customer"
    user_full_name.admin_order_field = "user__first_name"

    # =========================
    # ADMIN ACTIONS (BULK UPDATE)
    # =========================
    actions = (
        "mark_confirmed",
        "mark_cancelled",
        "mark_completed",
    )

    @admin.action(description="✅ Mark selected bookings as CONFIRMED")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="confirmed")

    @admin.action(description="❌ Mark selected bookings as CANCELLED")
    def mark_cancelled(self, request, queryset):
        queryset.update(status="cancelled")

    @admin.action(description="🏁 Mark selected bookings as COMPLETED")
    def mark_completed(self, request, queryset):
        queryset.update(status="completed")
