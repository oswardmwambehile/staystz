from django import forms
from .models import (
    BookingProperty,
    BookingPropertySetup,
    BookingPropertyPricing,
    BookingPropertyLegal,
    BookingPropertyPhoto
)
from .widgets import MultipleFileInput

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
class BookingPropertyForm(forms.ModelForm):
    languages_spoken = forms.MultipleChoiceField(
        choices=[
            ("English", "English"),
            ("French", "French"),
            ("Kiswahili", "Kiswahili"),
            ("German", "German"),
            ("Spanish", "Spanish"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = BookingProperty
        fields = [
            "property_name", "property_type", "property_description",
            "address", "district", "region", "country",
            "postal_code", "phone_number",
            "property_size_sqm", "languages_spoken"
        ]
        widgets = {
            "property_description": forms.Textarea(attrs={"rows": 3}),
            "property_type": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)

# ------------------------------------------------------------------
# STEP 2 – PROPERTY SETUP
# ------------------------------------------------------------------
class BookingPropertySetupForm(forms.ModelForm):
    amenities = forms.MultipleChoiceField(
        choices=[
            ("WiFi", "WiFi"),
            ("Parking", "Parking"),
            ("AC", "AC"),
            ("TV", "TV"),
            ("Pool", "Pool"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    room_types = forms.MultipleChoiceField(
        choices=[
            ("Single", "Single"),
            ("Double", "Double"),
            ("Suite", "Suite"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    accessibility_features = forms.MultipleChoiceField(
        choices=[
            ("Wheelchair accessible", "Wheelchair accessible"),
            ("Elevator", "Elevator"),
            ("Ramp", "Ramp"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = BookingPropertySetup
        fields = [
            "number_of_rooms", "beds_per_room",
            "max_guests_per_room", "number_of_bathrooms",
            "has_kitchen", "has_living_room",
            "amenities", "room_types",
            "accessibility_features"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)

# ------------------------------------------------------------------
# STEP 3 – MULTIPLE IMAGES
# ------------------------------------------------------------------
class BookingPropertyPhotoForm(forms.ModelForm):
    image = forms.FileField(
        widget=MultipleFileInput(attrs={"multiple": True}),
        required=False
    )

    class Meta:
        model = BookingPropertyPhoto
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)

# ------------------------------------------------------------------
# STEP 4 – PRICING & CALENDAR
# ------------------------------------------------------------------
class BookingPropertyPricingForm(forms.ModelForm):
    class Meta:
        model = BookingPropertyPricing
        fields = [
            "base_price_per_night",
            "available_from", "available_to",
    
            "minimum_stay_nights",
            "maximum_stay_nights"
        ]
        widgets = {
            "available_from": forms.DateInput(attrs={"type": "date"}),
            "available_to": forms.DateInput(attrs={"type": "date"}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)

# ------------------------------------------------------------------
# STEP 5 – LEGAL INFORMATION
# ------------------------------------------------------------------
class BookingPropertyLegalForm(forms.ModelForm):
    class Meta:
        model = BookingPropertyLegal
        fields = [
            "terms_and_conditions",
            "house_rules",
            "cancellation_policy",
            "check_in_policy",
            "smoking_policy",
            "pet_policy",
        ]
        widgets = {
            "terms_and_conditions": forms.Textarea(attrs={"rows": 3}),
            "house_rules": forms.Textarea(attrs={"rows": 3}),
            "cancellation_policy": forms.Textarea(attrs={"rows": 3}),
            "check_in_policy": forms.Textarea(attrs={"rows": 3}),
            "smoking_policy": forms.Textarea(attrs={"rows": 3}),
            "pet_policy": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_fields(self.fields)



from django import forms
from .models import Booking, BookingProperty, BookingPropertySetup

from django import forms


class BookingForm(forms.Form):
    room_type = forms.ChoiceField(
        choices=[],
        required=True
    )

    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    guests = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.property_obj = kwargs.pop('property', None)
        super().__init__(*args, **kwargs)

        if self.property_obj:
            setup = getattr(self.property_obj, 'bookingpropertysetup', None)
            if setup and setup.room_types:
                self.fields['room_type'].choices = [
                    (rt, rt) for rt in setup.room_types
                ]
            else:
                self.fields['room_type'].choices = []

    def clean(self):
        cleaned_data = super().clean()

        if not self.fields['room_type'].choices:
            raise forms.ValidationError("No room types available for this property.")

        return cleaned_data
