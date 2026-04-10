from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ResidenceProperty,
    ResidencePropertySetup,
    ResidencePropertyPhoto,
    ResidencePropertyPricing,
    OfficePropertySetup,
    ResidencePropertyLegal
)

# =========================================================
# 📸 PHOTO INLINE (WITH PREVIEW)
# =========================================================
class ResidencePropertyPhotoInline(admin.TabularInline):
    model = ResidencePropertyPhoto
    extra = 3
    fields = ("image", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" style="border-radius:8px;" />',
                obj.image.url
            )
        return "-"
    preview.short_description = "Preview"


# =========================================================
# 🏠 RESIDENCE SETUP INLINE
# =========================================================
class ResidencePropertySetupInline(admin.StackedInline):
    model = ResidencePropertySetup
    can_delete = False
    extra = 0
    readonly_fields = ("total_beds",)

    fieldsets = (
        ("Room Configuration", {
            "fields": (
                ("number_of_rooms", "beds_per_room", "max_guests_per_room", "total_beds"),
                "number_of_bathrooms",
            )
        }),
        ("Living Features", {
            "fields": (
                ("has_kitchen", "kitchen_type"),
                ("has_living_room", "living_room_size_sqm"),
            )
        }),
        ("Amenities & Features", {
            "classes": ("collapse",),
            "fields": (
                "amenities",
                "room_types",
                "accessibility_features",
                ("has_balcony", "has_storage_room", "has_laundry_room"),
            )
        }),
    )


# =========================================================
# 🏢 OFFICE SETUP INLINE
# =========================================================
class OfficePropertySetupInline(admin.StackedInline):
    model = OfficePropertySetup
    can_delete = False
    extra = 0

    fieldsets = (
        ("Office Details", {
            "fields": (
                ("office_size_sqm", "number_of_offices"),
                ("number_of_tenants", "road_type"),
                ("building_condition", "floor_finish"),
                ("door_type", "door_lock_condition"),
            )
        }),
        ("Facilities", {
            "fields": (
                ("has_water", "has_electricity"),
                ("fan_or_ac", "ceiling_type"),
                "window_type",
            )
        }),
        ("Environment", {
            "classes": ("collapse",),
            "fields": (
                "environment",
                "location_category",
            )
        }),
    )


# =========================================================
# 💰 PRICING INLINE
# =========================================================
class ResidencePropertyPricingInline(admin.StackedInline):
    model = ResidencePropertyPricing
    extra = 0

    fieldsets = (
        ("Pricing", {
            "fields": (
                "base_price",
                "cleaning_fee",
                ("currency", "rent_duration"),
                ("min_months", "max_months"),
            )
        }),
    )


# =========================================================
# ⚖️ LEGAL INLINE
# =========================================================
class ResidencePropertyLegalInline(admin.StackedInline):
    model = ResidencePropertyLegal
    extra = 0

    fieldsets = (
        ("Legal & Policies", {
            "classes": ("collapse",),
            "fields": (
                "terms_and_conditions",
                "house_rules",
                "cancellation_policy",
                "deposit_policy",
                "refund_rules",
                "insurance_details",
            )
        }),
    )


# =========================================================
# 🏠 MAIN ADMIN
# =========================================================
@admin.register(ResidenceProperty)
class ResidencePropertyAdmin(admin.ModelAdmin):

    # =========================
    # LIST VIEW
    # =========================
    list_display = (
        "id",
        "property_name",
        "property_type",
        "owner",
        "region",
        "district",
        "colored_status",
        "airbnb_available",
        "created_at",
    )

    list_display_links = ("id", "property_name")

    list_filter = (
        "property_type",
        "status",
        "region",
        "airbnb_available",
        "furnished",
        "parking_available",
    )

    search_fields = (
        "property_name",
        "owner__username",
        "region",
        "district",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at", "updated_at")

    # =========================
    # FORM LAYOUT
    # =========================
    fieldsets = (
        ("🏠 Basic Information", {
            "fields": (
                "owner",
                "property_name",
                "property_type",
                "airbnb_available",
                "property_description",
            )
        }),

        ("📍 Location", {
            "fields": (
                "address",
                ("region", "district"),
                ("country", "postal_code"),
            )
        }),

        ("📞 Contact", {
            "fields": ("phone_number",)
        }),

        ("📐 Property Details", {
            "fields": (
                ("property_size_sqm", "year_built"),
                ("building_level", "floors"),
                ("furnished", "parking_available", "parking_spaces"),
            )
        }),

        ("⚡ Utilities", {
            "fields": (
                ("electricity_type", "water_supply"),
                "internet_available",
            )
        }),

        ("🛡 Security", {
            "fields": (
                "has_cctv",
                "has_security_guard",
                "fenced_compound",
            )
        }),

        ("🕒 System", {
            "classes": ("collapse",),
            "fields": ("status", "created_at", "updated_at"),
        }),
    )

    # =========================
    # DYNAMIC INLINE SWITCH
    # =========================
    def get_inlines(self, request, obj=None):
        if obj is None:
            return [
                ResidencePropertyPricingInline,
                ResidencePropertyLegalInline,
                ResidencePropertyPhotoInline,
            ]

        if obj.property_type == "office_space":
            return [
                OfficePropertySetupInline,
                ResidencePropertyPricingInline,
                ResidencePropertyLegalInline,
                ResidencePropertyPhotoInline,
            ]

        return [
            ResidencePropertySetupInline,
            ResidencePropertyPricingInline,
            ResidencePropertyLegalInline,
            ResidencePropertyPhotoInline,
        ]

    # =========================
    # STATUS COLOR
    # =========================
    def colored_status(self, obj):
        colors = {
            "open": "green",
            "hold": "orange",
            "closed": "red",
        }
        return format_html(
            '<b style="color:{};">{}</b>',
            colors.get(obj.status, "black"),
            obj.status.upper()
        )
    colored_status.short_description = "Status"