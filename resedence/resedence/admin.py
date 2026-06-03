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
# PHOTOS INLINE (WITH IMAGE PREVIEW)
# =========================================================
class ResidencePropertyPhotoInline(admin.TabularInline):
    model = ResidencePropertyPhoto
    extra = 1
    readonly_fields = ("preview",)
    fields = ("image", "preview")

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:70px;width:110px;object-fit:cover;border-radius:10px;border:1px solid #ddd;" />',
                obj.image.url
            )
        return "No Image"

    preview.short_description = "Preview"


# =========================================================
# ONE-TO-ONE INLINES
# =========================================================
class ResidencePropertySetupInline(admin.StackedInline):
    model = ResidencePropertySetup
    extra = 0
    can_delete = False


class OfficePropertySetupInline(admin.StackedInline):
    model = OfficePropertySetup
    extra = 0
    can_delete = False


class ResidencePropertyPricingInline(admin.StackedInline):
    model = ResidencePropertyPricing
    extra = 0
    can_delete = False


class ResidencePropertyLegalInline(admin.StackedInline):
    model = ResidencePropertyLegal
    extra = 0
    can_delete = False


# =========================================================
# MAIN PROPERTY ADMIN
# =========================================================
@admin.register(ResidenceProperty)
class ResidencePropertyAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "property_name",
        "property_type",
        "owner",
        "region",
        "district",
        "status",
        "airbnb_available",
        "created_at",
    )

    list_filter = (
        "property_type",
        "status",
        "region",
        "district",
        "airbnb_available",
        "furnished",
        "parking_available",
        "internet_available",
        "has_cctv",
        "has_security_guard",
        "fenced_compound",
        "created_at",
    )

    search_fields = (
        "property_name",
        "owner__username",
        "owner__email",
        "region",
        "district",
        "address",
        "phone_number",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Owner & Property Info", {
            "fields": (
                "owner",
                "property_name",
                "property_type",
                "airbnb_available",
                "property_description",
            )
        }),

        ("Location", {
            "fields": (
                "address",
                "region",
                "district",
                "country",
                "postal_code",
            )
        }),

        ("Contact", {
            "fields": ("phone_number",)
        }),

        ("Property Specifications", {
            "fields": (
                "property_size_sqm",
                "year_built",
                "building_level",
                "floors",
                "furnished",
                "parking_available",
                "parking_spaces",
            )
        }),

        ("Utilities", {
            "fields": (
                "electricity_type",
                "water_supply",
                "internet_available",
            )
        }),

        ("Security", {
            "fields": (
                "has_cctv",
                "has_security_guard",
                "fenced_compound",
            )
        }),

        ("System", {
            "fields": (
                "status",
                "created_at",
                "updated_at",
            )
        }),
    )

    # ✅ SHOW INLINES DEPENDING ON PROPERTY TYPE
    def get_inlines(self, request, obj=None):

        # When creating new property (obj is None)
        if obj is None:
            return [
                ResidencePropertyPricingInline,
                ResidencePropertyLegalInline,
                ResidencePropertyPhotoInline,
            ]

        # Office Space
        if obj.property_type == "office_space":
            return [
                OfficePropertySetupInline,
                ResidencePropertyPricingInline,
                ResidencePropertyLegalInline,
                ResidencePropertyPhotoInline,
            ]

        # Apartment / Homes
        return [
            ResidencePropertySetupInline,
            ResidencePropertyPricingInline,
            ResidencePropertyLegalInline,
            ResidencePropertyPhotoInline,
        ]


# =========================================================
# REGISTER OTHER MODELS (OPTIONAL)
# =========================================================
@admin.register(ResidencePropertyPhoto)
class ResidencePropertyPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "image")
    search_fields = ("property__property_name",)


@admin.register(ResidencePropertySetup)
class ResidencePropertySetupAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "number_of_rooms", "total_beds")
    search_fields = ("property__property_name",)


@admin.register(OfficePropertySetup)
class OfficePropertySetupAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "office_size_sqm", "number_of_tenants", "road_type")
    search_fields = ("property__property_name",)


@admin.register(ResidencePropertyPricing)
class ResidencePropertyPricingAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "base_price", "currency", "rent_duration")
    search_fields = ("property__property_name",)


@admin.register(ResidencePropertyLegal)
class ResidencePropertyLegalAdmin(admin.ModelAdmin):
    list_display = ("id", "property")
    search_fields = ("property__property_name",)
