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


from django import forms
from .models import ResidenceBooking


from django import forms
from .models import ResidenceBooking


class ResidenceBookingForm(forms.ModelForm):

    class Meta:
        model = ResidenceBooking
        fields = [
            "need_bnb",
            "rent_duration",
            "phone_number",
            "check_in_date",
            "check_out_date",
            "adults",
            "children",
            "has_parcel",
            "parcel_details",
        ]

        widgets = {
            "need_bnb": forms.Select(attrs={
                "class": "w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-500"
            }),

            "rent_duration": forms.Select(attrs={
                "class": "w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-500"
            }),

            "phone_number": forms.TextInput(attrs={
                "class": "w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-500",
                "placeholder": "e.g. +255712345678"
            }),

            "check_in_date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-500"
            }),

            "check_out_date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-500"
            }),

            "adults": forms.NumberInput(attrs={
                "class": "w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-500",
                "min": 1
            }),

            "children": forms.NumberInput(attrs={
                "class": "w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-500",
                "min": 0
            }),

            "has_parcel": forms.Select(attrs={
                "class": "w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-500"
            }),

            "parcel_details": forms.TextInput(attrs={
                "class": "w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-500",
                "placeholder": "Enter parcel details or quantity"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optional by default (JavaScript will show/hide them)
        self.fields["rent_duration"].required = False
        self.fields["check_in_date"].required = False
        self.fields["check_out_date"].required = False
        self.fields["parcel_details"].required = False

    def clean(self):
        cleaned_data = super().clean()

        need_bnb = cleaned_data.get("need_bnb")
        rent_duration = cleaned_data.get("rent_duration")
        check_in = cleaned_data.get("check_in_date")
        check_out = cleaned_data.get("check_out_date")
        has_parcel = cleaned_data.get("has_parcel")
        parcel_details = cleaned_data.get("parcel_details")

        # If user needs BnB, require check-in and check-out
        if need_bnb == "yes":
            if not check_in:
                self.add_error(
                    "check_in_date",
                    "Check-in date is required when BnB is selected."
                )

            if not check_out:
                self.add_error(
                    "check_out_date",
                    "Check-out date is required when BnB is selected."
                )

        # If user does not need BnB, require rent duration
        else:
            if not rent_duration:
                self.add_error(
                    "rent_duration",
                    "Please select a rent duration."
                )

        # If user has parcels, require parcel details
        if has_parcel == "yes" and not parcel_details:
            self.add_error(
                "parcel_details",
                "Please provide parcel details."
            )

        return cleaned_data



from django import forms
from .models import ResidencePropertyReview


class ResidencePropertyReviewForm(forms.ModelForm):

    class Meta:
        model = ResidencePropertyReview
        fields = ["rating", "comment"]

        widgets = {
            "rating": forms.Select(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-3"
                }
            ),

            "comment": forms.Textarea(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-3",
                    "rows": 5,
                    "placeholder": "Write your review..."
                }
            ),
        }