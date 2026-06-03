from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ResidenceProperty,
    ResidencePropertySetup,
    ResidencePropertyPhoto,
    ResidencePropertyPricing,
    OfficePropertySetup,
    ResidencePropertyLegal,
)


# =========================================================
# 📸 PHOTO INLINE (SAFE FOR MISSING FILES)
# =========================================================
class ResidencePropertyPhotoInline(admin.TabularInline):
    model = ResidencePropertyPhoto
    extra = 1

    fields = ("image", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        try:
            if obj and obj.image and obj.image.name:
                return format_html(
                    '<img src="{}" width="100" style="border-radius:8px;" />',
                    obj.image.url
                )
        except Exception:
            return "Missing File"

        return "-"
    preview.short_description = "Preview"


# =========================================================
# 🏠 RESIDENCE SETUP INLINE
# =========================================================
class ResidencePropertySetupInline(admin.StackedInline):
    model = ResidencePropertySetup
    extra = 0
    can_delete = False
    readonly_fields = ("total_beds",)


# =========================================================
# 🏢 OFFICE SETUP INLINE
# =========================================================
class OfficePropertySetupInline(admin.StackedInline):
    model = OfficePropertySetup
    extra = 0
    can_delete = False


# =========================================================
# 💰 PRICING INLINE
# =========================================================
class ResidencePropertyPricingInline(admin.StackedInline):
    model = ResidencePropertyPricing
    extra = 0


# =========================================================
# ⚖️ LEGAL INLINE
# =========================================================
class ResidencePropertyLegalInline(admin.StackedInline):
    model = ResidencePropertyLegal
    extra = 0


# =========================================================
# 🏠 MAIN ADMIN
# =========================================================
@admin.register(ResidenceProperty)
class ResidencePropertyAdmin(admin.ModelAdmin):

    # ---------------- LIST VIEW ----------------
    list_display = (
        "id",
        "property_name",
        "property_type",
        "owner",
        "region",
        "district",
        "status",
        "bnb_available",
        "created_at",
    )

    list_filter = (
        "property_type",
        "status",
        "region",
        "bnb_available",
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

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    # ---------------- FORM VIEW ----------------
    fieldsets = (
        ("Basic Information", {
            "fields": (
                "owner",
                "property_name",
                "property_type",
                "bnb_available",
                "property_description",
            )
        }),

        ("Location", {
            "fields": (
                "address",
                ("region", "district"),
                ("country", "postal_code"),
            )
        }),

        ("Contact", {
            "fields": ("phone_number",)
        }),

        ("Property Details", {
            "fields": (
                ("property_size_sqm", "year_built"),
                ("building_level", "floors"),
                ("furnished", "parking_available", "parking_spaces"),
            )
        }),

        ("Utilities", {
            "fields": (
                ("electricity_type", "water_supply"),
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

    # ---------------- DYNAMIC INLINES ----------------
    def get_inlines(self, request, obj=None):

        # CREATE PAGE
        if obj is None:
            return [
                ResidencePropertyPricingInline,
                ResidencePropertyLegalInline,
                ResidencePropertyPhotoInline,
            ]

        # OFFICE PROPERTY
        if obj.property_type == "office_space":
            return [
                OfficePropertySetupInline,
                ResidencePropertyPricingInline,
                ResidencePropertyLegalInline,
                ResidencePropertyPhotoInline,
            ]

        # RESIDENTIAL PROPERTY
        return [
            ResidencePropertySetupInline,
            ResidencePropertyPricingInline,
            ResidencePropertyLegalInline,
            ResidencePropertyPhotoInline,
        ]

    # ---------------- STATUS COLOR ----------------
    def colored_status(self, obj):
        colors = {
            "open": "green",
            "hold": "orange",
            "closed": "red",
        }

        return format_html(
            '<b style="color:{};">{}</b>',
            colors.get(obj.status, "black"),
            obj.status.upper(),
        )

    colored_status.short_description = "Status"                                                              