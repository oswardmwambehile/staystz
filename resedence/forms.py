from django import forms

from .models import (
    ResidenceProperty,
    ResidencePropertySetup,
    OfficePropertySetup,
    ResidencePropertyPhoto,
    ResidencePropertyPricing,
    ResidencePropertyLegal,
)

from booking.widgets import MultipleFileInput


# ------------------------------------------------------------------
# UNIVERSAL BOOTSTRAP HELPER
# ------------------------------------------------------------------
def bootstrap_fields(fields):
    """Apply Bootstrap styles + placeholders to all fields."""
    for name, field in fields.items():
        widget = field.widget
        input_type = getattr(widget, "input_type", None)

        # Mark checkboxes for template safety
        if isinstance(widget, forms.CheckboxSelectMultiple):
            field.is_checkbox = True
        else:
            field.is_checkbox = False

        # Add placeholder for text-like inputs
        if input_type == "file":
            widget.attrs.update({"class": "form-control"})
        elif input_type == "checkbox":
            widget.attrs.update({"class": "form-check-input"})
        elif isinstance(widget, forms.Select):
            widget.attrs.update({"class": "form-select"})
        elif isinstance(widget, forms.Textarea):
            widget.attrs.update({
                "class": "form-control",
                "placeholder": f"Enter {field.label}"
            })
        else:
            widget.attrs.update({
                "class": "form-control",
                "placeholder": f"Enter {field.label}"
            })

    return fields


# ------------------------------------------------------------------
# STEP 1 – BASIC INFORMATION (COMMON)
# ------------------------------------------------------------------
class ResidencePropertyForm(forms.ModelForm):

    class Meta:
        model = ResidenceProperty
        fields = [
            "property_name", "property_type", "property_description", "bnb_available",
            "address", "district", "region", "country",
            "postal_code", "phone_number",
            "property_size_sqm", "year_built","building_level", "floors",
            "furnished", "parking_available", "parking_spaces",

            # Utilities + security
            "electricity_type", "water_supply", "internet_available",
            "has_cctv", "has_security_guard", "fenced_compound",
        ]
        widgets = {
            "property_description": forms.Textarea(attrs={"rows": 3}),
            "property_type": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)


# ------------------------------------------------------------------
# STEP 2A – SETUP FOR APARTMENT / HOUSE
# ------------------------------------------------------------------
class ResidencePropertySetupForm(forms.ModelForm):

    amenities = forms.MultipleChoiceField(
        choices=[
            ("WiFi", "WiFi"),
            ("Parking", "Parking"),
            ("AC", "Air Conditioning"),
            ("TV", "Television"),
            ("Fridge", "Fridge"),
            ("Pool", "Swimming Pool"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    room_types = forms.MultipleChoiceField(
        choices=[
            ("Single Room", "Single Room"),
            ("Double Room", "Double Room"),
            ("Master Bedroom", "Master Bedroom"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    accessibility_features = forms.MultipleChoiceField(
        choices=[
            ("Wheelchair Ramp", "Wheelchair Ramp"),
            ("Wide Doors", "Wide Doors"),
            ("Elevator", "Elevator"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    bathroom_types = forms.MultipleChoiceField(
        choices=[
            ("Shared", "Shared"),
            ("Private", "Private"),
            ("Ensuite", "Ensuite"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = ResidencePropertySetup
        exclude = ["property", "total_beds"]  # property assigned in view

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)


# ------------------------------------------------------------------
# STEP 2B – SETUP FOR OFFICE SPACE
# ------------------------------------------------------------------
class OfficePropertySetupForm(forms.ModelForm):

    class Meta:
        model = OfficePropertySetup
        exclude = ["property"]  # property assigned in view

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)


# ------------------------------------------------------------------
# STEP 3 – MULTIPLE IMAGES
# ------------------------------------------------------------------
class ResidencePropertyPhotoForm(forms.ModelForm):

    image = forms.FileField(
        widget=MultipleFileInput(attrs={"multiple": True}),
        required=False
    )

    class Meta:
        model = ResidencePropertyPhoto
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)


# ------------------------------------------------------------------
# STEP 4 – PRICING (DIFFERENT FOR OFFICE VS RESIDENCE)
class ResidencePropertyPricingForm(forms.ModelForm):

    class Meta:
        model = ResidencePropertyPricing
        fields = [
            "base_price",
            "base_price_per_day",
            "weekly_discount_percent",
            "monthly_discount_percent",
            "cleaning_fee",
            "rent_duration",
            "min_months",
            "max_months",
            "currency",
        ]
        widgets = {
            "currency": forms.Select(choices=[("TZS", "TZS"), ("USD", "USD")]),
        }

    def __init__(self, *args, **kwargs):
        self.property_obj = kwargs.pop("property_obj", None)
        super().__init__(*args, **kwargs)

        if self.property_obj:
            is_apartment = self.property_obj.property_type == "apartment"
            is_bnb = self.property_obj.bnb_available == "yes"

            if is_apartment and is_bnb:
                # BNB MODE → DAILY PRICING ONLY
                allowed_fields = {
                    "base_price_per_day",
                    "weekly_discount_percent",
                    "monthly_discount_percent",
                    "cleaning_fee",
                    "currency",
                }

            else:
                # NORMAL RENT MODE → MONTHLY / LONG TERM
                allowed_fields = {
                    "base_price",
                    "rent_duration",
                    "min_months",
                    "max_months",
                    "cleaning_fee",
                    "currency",
                }

            # remove everything not allowed
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)

        bootstrap_fields(self.fields)


# ------------------------------------------------------------------
# STEP 5 – LEGAL
# ------------------------------------------------------------------
class ResidencePropertyLegalForm(forms.ModelForm):

    class Meta:
        model = ResidencePropertyLegal
        exclude = ["property"]  # property assigned in view
        widgets = {
            "terms_and_conditions": forms.Textarea(attrs={"rows": 3}),
            "house_rules": forms.Textarea(attrs={"rows": 3}),
            "cancellation_policy": forms.Textarea(attrs={"rows": 3}),
            "deposit_policy": forms.Textarea(attrs={"rows": 3}),
            "refund_rules": forms.Textarea(attrs={"rows": 3}),
            "insurance_details": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)


# ------------------------------------------------------------------
# STATUS UPDATE FORM
# ------------------------------------------------------------------
class ResidencePropertyStatusForm(forms.ModelForm):
    class Meta:
        model = ResidenceProperty
        fields = ["status"]
