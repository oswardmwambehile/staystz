from django.shortcuts import render
from .models import ResidenceProperty, ResidencePropertyPhoto
from django.shortcuts import render, redirect
from .models import ResidenceProperty, ResidencePropertyPhoto
from .forms import (
    ResidencePropertyForm,
    ResidencePropertySetupForm,
    OfficePropertySetupForm,
    ResidencePropertyPricingForm,
    ResidencePropertyLegalForm,
)

from django.shortcuts import render, redirect
from .models import ResidenceProperty, ResidencePropertyPhoto
from .forms import (
    ResidencePropertyForm,
    ResidencePropertySetupForm,
    OfficePropertySetupForm,
    ResidencePropertyPricingForm,
    ResidencePropertyLegalForm,
)


def add_residence_property_all_in_one(request):
    success = False

    if request.method == "POST":

        if request.session.get("residence_lock"):
          return redirect("my_residence_properties")

        request.session["residence_lock"] = True

        # -------------------------
        # STEP 1: PROPERTY FORM
        # -------------------------
        property_form = ResidencePropertyForm(request.POST)

        if property_form.is_valid():
            prop = property_form.save(commit=False)
            prop.owner = request.user
            prop.save()

            property_type = prop.property_type
            is_office = (property_type == "office_space")

            # -------------------------
            # STEP 2: SETUP FORM
            # -------------------------
            if is_office:
                setup_form = OfficePropertySetupForm(request.POST)
            else:
                setup_form = ResidencePropertySetupForm(request.POST)

            # -------------------------
            # STEP 3: PRICING FORM
            # -------------------------
            pricing_form = ResidencePropertyPricingForm(
                request.POST,
                property_obj=prop
            )

            # -------------------------
            # STEP 4: LEGAL FORM
            # -------------------------
            legal_form = ResidencePropertyLegalForm(request.POST)

            # -------------------------
            # VALIDATION
            # -------------------------
            setup_valid = setup_form.is_valid()
            pricing_valid = pricing_form.is_valid()
            legal_valid = legal_form.is_valid()

            if setup_valid and pricing_valid and legal_valid:

                # SAVE SETUP
                setup_obj = setup_form.save(commit=False)
                setup_obj.property = prop
                setup_obj.save()

                # SAVE PRICING
                pricing_obj = pricing_form.save(commit=False)
                pricing_obj.property = prop
                pricing_obj.save()

                # SAVE LEGAL
                legal_obj = legal_form.save(commit=False)
                legal_obj.property = prop
                legal_obj.save()

                # ======================================================
                # FIXED IMAGE UPLOAD (SAFE FOR 100 IMAGES)
                # ======================================================

                images = request.FILES.getlist("image")

                # limit number of images
                if len(images) > 100:
                    return render(request, "property/add_residence_property.html", {
                        "property_form": property_form,
                        "residence_setup_form": setup_form,
                        "office_setup_form": office_setup_form,
                        "pricing_form": pricing_form,
                        "legal_form": legal_form,
                        "success": False,
                        "error": "Maximum 100 images allowed"
                    })

                # batch processing to avoid server crash
                batch_size = 10

                for i in range(0, len(images), batch_size):
                    batch = images[i:i + batch_size]

                    for img in batch:
                        ResidencePropertyPhoto.objects.create(
                            property=prop,
                            image=img
                        )

                success = True
                return redirect("my_residence_properties")

        else:
            # if property form fails
            setup_form = ResidencePropertySetupForm(request.POST)
            office_setup_form = OfficePropertySetupForm(request.POST)
            pricing_form = ResidencePropertyPricingForm(request.POST)
            legal_form = ResidencePropertyLegalForm(request.POST)

    else:
        property_form = ResidencePropertyForm()
        setup_form = ResidencePropertySetupForm()
        office_setup_form = OfficePropertySetupForm()
        pricing_form = ResidencePropertyPricingForm()
        legal_form = ResidencePropertyLegalForm()

    return render(request, "property/add_residence_property.html", {
        "property_form": property_form,
        "residence_setup_form": setup_form,
        "office_setup_form": office_setup_form,
        "pricing_form": pricing_form,
        "legal_form": legal_form,
        "success": success,
    })








from django.shortcuts import render
from .models import ResidenceProperty

def my_residence_properties(request):
    # Only show residences added by the logged-in user
    properties = ResidenceProperty.objects.filter(owner=request.user)
    return render(request, "property/residence_properties.html", {
        "properties": properties
    })


from django.shortcuts import render, get_object_or_404
from .models import (
    ResidenceProperty,
    ResidencePropertySetup,
    ResidencePropertyPhoto,
    ResidencePropertyPricing,
    ResidencePropertyLegal,
)

def residence_property_detail(request, pk):
    # Fetch the property for the logged-in user
    property_obj = get_object_or_404(ResidenceProperty, pk=pk, owner=request.user)
    office_setup = getattr(property_obj, 'office_setup', None)

    # Related objects
    setup = getattr(property_obj, 'residencepropertysetup', None)
    pricing = getattr(property_obj, 'residencepropertypricing', None)
    legal = getattr(property_obj, 'residencepropertylegal', None)
    photos = property_obj.photos.all()

    return render(request, "property/residence_property_detail.html", {
        "property": property_obj,
        "setup": setup,
        "pricing": pricing,
        "legal": legal,
        "photos": photos,
        "office_setup": office_setup,
    })


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import ResidenceProperty

def residence_property_delete(request, pk):
    # Only allow POST requests for deletion
    if request.method == "POST":
        property_obj = get_object_or_404(ResidenceProperty, pk=pk, owner=request.user)
        property_name = property_obj.property_name
        property_obj.delete()
        messages.success(request, f"Residence property '{property_name}' has been deleted successfully.")
        return redirect('my_residence_properties')  # Replace with the name of your "My Properties" page
    else:
        messages.error(request, "Invalid request method.")
        return redirect('my_residence_properties')


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import ResidenceProperty
from .forms import ResidencePropertyStatusForm

def update_residence_status(request, pk):
    property_obj = get_object_or_404(ResidenceProperty, pk=pk, owner=request.user)

    if request.method == "POST":
        form = ResidencePropertyStatusForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Status of '{property_obj.property_name}' updated to {property_obj.status}.")
        else:
            messages.error(request, "Failed to update status.")

    return redirect('my_residence_properties')

from django.shortcuts import render
from django.db.models import Q
from .models import ResidenceProperty


TANZANIA_REGIONS = [
    'Arusha', 'Dar es Salaam', 'Dodoma', 'Geita', 'Iringa', 'Kagera', 'Katavi',
    'Kigoma', 'Kilimanjaro', 'Lindi', 'Manyara', 'Mara', 'Mbeya', 'Morogoro',
    'Mtwara', 'Mwanza', 'Njombe', 'Pwani', 'Rukwa', 'Ruvuma', 'Shinyanga',
    'Simiyu', 'Singida', 'Tabora', 'Tanga', 'Zanzibar North', 'Zanzibar South',
    'Zanzibar West', 'Zanzibar Central/South', 'Zanzibar Urban/West'
]

def residence_properties(request, property_type):
    # Filter by selected property_type (e.g., "apartment", "house", "frame")
    properties = ResidenceProperty.objects.filter(
        property_type=property_type,
        owner__attachments__is_verified=True
    )

    keyword = request.GET.get("keyword", "")
    region = request.GET.get("region", "")
    type_filter = request.GET.get("property_type_filter", "")

    # Keyword search
    if keyword:
        properties = properties.filter(
            Q(property_name__icontains=keyword) |
            Q(property_description__icontains=keyword) |
            Q(address__icontains=keyword) |
            Q(district__icontains=keyword) |
            Q(region__icontains=keyword)
        )

    # Region filter
    if region:
        properties = properties.filter(region=region)

    # Filter by property_type_choices
    if type_filter:
        properties = properties.filter(property_type=type_filter)

    context = {
        "properties": properties,
        "property_type": property_type.replace("_", " ").title(),
        "tanzania_regions": TANZANIA_REGIONS,
        "property_type_choices": ResidenceProperty.PROPERTY_TYPE_CHOICES,
    }

    return render(request, "customer/residence_property_lists.html", context)


from django.shortcuts import render, get_object_or_404
from .models import ResidenceProperty

def residence_property_details(request, pk):
    # Public access – no owner restriction
    property_obj = get_object_or_404(ResidenceProperty, pk=pk)

    # Related objects
    setup = getattr(property_obj, 'residencepropertysetup', None)
    office_setup = getattr(property_obj, 'office_setup', None)  # ✅ fetch office setup
    pricing = getattr(property_obj, 'residencepropertypricing', None)
    legal = getattr(property_obj, 'residencepropertylegal', None)
    photos = property_obj.photos.all()

    return render(request, "customer/residence_property_detail.html", {
        "property": property_obj,
        "setup": setup,
        "office_setup": office_setup,  # ✅ pass to template
        "pricing": pricing,
        "legal": legal,
        "photos": photos,
    })




def resedence(request, booking_id=None):

    return render(request, 'customer/resedence.html')

