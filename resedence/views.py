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

    # =========================
    # DEFAULT SAFE INITIALIZATION
    # =========================
    property_form = ResidencePropertyForm(request.POST or None)
    setup_form = None
    office_setup_form = None
    pricing_form = None
    legal_form = None

    # =========================
    # HANDLE POST
    # =========================
    if request.method == "POST":

        # -------------------------
        # LOCK CHECK
        # -------------------------
        if request.session.get("residence_lock"):
            return redirect("my_residence_properties")

        request.session["residence_lock"] = True

        # -------------------------
        # STEP 1: PROPERTY FORM
        # -------------------------
        if property_form.is_valid():
            prop = property_form.save(commit=False)
            prop.owner = request.user
            prop.save()

            property_type = prop.property_type
            is_office = property_type == "office_space"

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

                # -------------------------
                # SAVE SETUP
                # -------------------------
                setup_obj = setup_form.save(commit=False)
                setup_obj.property = prop
                setup_obj.save()

                # -------------------------
                # SAVE PRICING
                # -------------------------
                pricing_obj = pricing_form.save(commit=False)
                pricing_obj.property = prop
                pricing_obj.save()

                # -------------------------
                # SAVE LEGAL
                # -------------------------
                legal_obj = legal_form.save(commit=False)
                legal_obj.property = prop
                legal_obj.save()

                # -------------------------
                # IMAGE UPLOAD SAFE
                # -------------------------
                images = request.FILES.getlist("image")

                if len(images) > 100:
                    request.session["residence_lock"] = False
                    return render(request, "property/add_residence_property.html", {
                        "property_form": property_form,
                        "residence_setup_form": setup_form if setup_form else ResidencePropertySetupForm(),
                        "office_setup_form": office_setup_form if office_setup_form else OfficePropertySetupForm(),
                        "pricing_form": pricing_form,
                        "legal_form": legal_form,
                        "success": False,
                        "error": "Maximum 100 images allowed"
                    })

                batch_size = 10

                for i in range(0, len(images), batch_size):
                    batch = images[i:i + batch_size]
                    for img in batch:
                        ResidencePropertyPhoto.objects.create(
                            property=prop,
                            image=img
                        )

                success = True
                request.session["residence_lock"] = False
                return redirect("my_residence_properties")

        else:
            # PROPERTY FORM INVALID
            setup_form = ResidencePropertySetupForm(request.POST)
            office_setup_form = OfficePropertySetupForm(request.POST)
            pricing_form = ResidencePropertyPricingForm(request.POST)
            legal_form = ResidencePropertyLegalForm(request.POST)

            request.session["residence_lock"] = False

    # =========================
    # SAFE DEFAULT RENDER (GET OR FAIL)
    # =========================
    if setup_form is None:
        setup_form = ResidencePropertySetupForm()

    if office_setup_form is None:
        office_setup_form = OfficePropertySetupForm()

    if pricing_form is None:
        pricing_form = ResidencePropertyPricingForm()

    if legal_form is None:
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


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import ResidenceProperty, ResidenceBooking
from .forms import ResidenceBookingForm


@login_required(login_url='signin')
def book_residence(request, property_id):

    property_obj = get_object_or_404(ResidenceProperty, id=property_id)

    pricing = property_obj.residencepropertypricing

    if request.method == "POST":

        form = ResidenceBookingForm(request.POST, is_daily=bool(pricing.base_price_per_day))

        print(form.errors)

        if form.is_valid():

            booking = form.save(commit=False)

            booking.property = property_obj
            booking.user = request.user

            # =========================
            # CALCULATE TOTAL PRICE
            # =========================
            total_price = 0

            # DAILY BOOKING
            if pricing.base_price_per_day and booking.check_in_date and booking.check_out_date:

                days = (booking.check_out_date - booking.check_in_date).days

                if days <= 0:
                    days = 1

                total_price = days * pricing.base_price_per_day

            # MONTHLY BOOKING
            elif pricing.base_price and booking.rent_duration:

                total_price = booking.rent_duration * pricing.base_price

            booking.total_price = total_price

            booking.save()

            print("RESIDENCE BOOKING SAVED")

            # ==========================
            # EMAIL TO PROPERTY OWNER
            # ==========================
            try:
                subject = f"New Booking Request - {property_obj.property_name}"

                context = {
                    "booking": booking,
                    "property": property_obj,
                }

                html_content = render_to_string(
                    "emails/residence_booking_email.html",
                    context
                )

                text_content = strip_tags(html_content)

                owner_email = property_obj.owner.email

                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=f"StayTZ Bookings <{settings.EMAIL_HOST_USER}>",
                    to=[owner_email],
                )

                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)

                print("EMAIL SENT TO PROPERTY OWNER")

            except Exception as e:
                print("EMAIL ERROR:", e)

            messages.success(request, "Booking submitted successfully.")
            return redirect("residence_booking_success", booking_id=booking.id)

        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)

    else:
        form = ResidenceBookingForm(
            is_daily=bool(pricing.base_price_per_day)
        )

    return render(request, "customer/book_residence.html", {
        "form": form,
        "property": property_obj,
        "pricing": pricing,
    })


from django.shortcuts import get_object_or_404, render

def residence_booking_success(request, booking_id):
    booking = get_object_or_404(ResidenceBooking, id=booking_id)

    return render(request, "customer/residence_booking_success.html", {
        "booking": booking
    })