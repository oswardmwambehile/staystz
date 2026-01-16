from django import forms
from .models import (
    CarRental,
    CarRentalSetup,
    CarRentalPhoto,
    CarRentalPricing,
    CarRentalLegal,
)
from booking.widgets import MultipleFileInput

# ------------------------------------------------------------------
# UNIVERSAL BOOTSTRAP HELPER
# ------------------------------------------------------------------
def bootstrap_fields(fields):
    """Auto-apply Bootstrap styles + placeholders to ALL fields."""
    for name, field in fields.items():
        widget = field.widget
        input_type = getattr(widget, "input_type", None)

        # Mark checkbox fields so template can safely check
        if isinstance(widget, forms.CheckboxSelectMultiple):
            field.is_checkbox = True
        else:
            field.is_checkbox = False

        # Add placeholder
        placeholder_text = f"Enter {field.label}"
        if input_type == "file":
            widget.attrs.update({"class": "form-control"})
        elif input_type == "checkbox":
            widget.attrs.update({"class": "form-check-input"})
        elif isinstance(widget, forms.Select):
            widget.attrs.update({"class": "form-select"})
            widget.attrs["placeholder"] = f"Select {field.label}"
        elif isinstance(widget, forms.Textarea):
            widget.attrs.update({"class": "form-control"})
            widget.attrs.setdefault("placeholder", f"Enter {field.label}")
        else:
            widget.attrs.update({"class": "form-control"})
            widget.attrs.setdefault("placeholder", f"Enter {field.label}")
    return fields

# ------------------------------------------------------------------
# STEP 1 – BASIC INFORMATION
# ------------------------------------------------------------------
class CarRentalForm(forms.ModelForm):

    class Meta:
        model = CarRental
        fields = [
            "car_name",
            "car_type",
            "car_description",
            "registration_number",
            "manufacturer",
            "model_year",
            "color",
            "seats",
            "phone_number",
            "has_air_conditioning",
            "automatic_transmission",
            "fuel_type",
            "mileage_km",
        ]
        widgets = {
            "car_description": forms.Textarea(attrs={"rows": 3}),
            "car_type": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)

# ------------------------------------------------------------------
# STEP 2 – CAR SETUP / FEATURES
# ------------------------------------------------------------------
class CarRentalSetupForm(forms.ModelForm):
    safety_features = forms.MultipleChoiceField(
        choices=[
            ("Airbags", "Airbags"),
            ("ABS", "ABS"),
            ("Traction Control", "Traction Control"),
            ("Parking Sensors", "Parking Sensors"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CarRentalSetup
        fields = [
            "has_gps",
            "has_radio",
            "has_music_system",
            "safety_features",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)

# ------------------------------------------------------------------
# STEP 3 – MULTIPLE IMAGES
# ------------------------------------------------------------------
class CarRentalPhotoForm(forms.ModelForm):
    image = forms.FileField(
        widget=MultipleFileInput(attrs={"multiple": True}),
        required=False
    )

    class Meta:
        model = CarRentalPhoto
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)

# ------------------------------------------------------------------
# STEP 4 – PRICING
# ------------------------------------------------------------------
class CarRentalPricingForm(forms.ModelForm):
    class Meta:
        model = CarRentalPricing
        fields = [
            "base_price_per_day",
            "weekly_discount",
            "monthly_discount",
            "cleaning_fee",
            "tax_percentage",
            "currency",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)

# ------------------------------------------------------------------
# STEP 5 – LEGAL / POLICIES
# ------------------------------------------------------------------
class CarRentalLegalForm(forms.ModelForm):
    class Meta:
        model = CarRentalLegal
        fields = [
            "terms_and_conditions",
            "rental_policy",
            "cancellation_policy",
            "deposit_policy",
            "insurance_details",
        ]
        widgets = {
            "terms_and_conditions": forms.Textarea(attrs={"rows": 3}),
            "rental_policy": forms.Textarea(attrs={"rows": 3}),
            "cancellation_policy": forms.Textarea(attrs={"rows": 3}),
            "deposit_policy": forms.Textarea(attrs={"rows": 3}),
            "insurance_details": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)
