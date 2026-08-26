from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    BookingProperty,
    BookingPropertySetup,
    BookingPropertyPricing,
    BookingPropertyLegal,
    BookingPropertyPhoto,
)

from .forms import (
    BookingPropertyForm,
    BookingPropertySetupForm,
    BookingPropertyPricingForm,
    BookingPropertyLegalForm,
)


def add_property_all_in_one(request, property_id=None):

    # =====================================================
    # NEW PROPERTY
    # =====================================================

    if property_id:
        property_obj = get_object_or_404(
            BookingProperty,
            id=property_id,
            owner=request.user
        )
    else:
        property_obj = None


    # =====================================================
    # GET
    # =====================================================

    if request.method == "GET":

        if property_obj:

            property_form = BookingPropertyForm(
                instance=property_obj
            )

            setup_form = BookingPropertySetupForm(
                instance=getattr(
                    property_obj,
                    "bookingpropertysetup",
                    None
                )
            )

            pricing_form = BookingPropertyPricingForm(
                instance=getattr(
                    property_obj,
                    "bookingpropertypricing",
                    None
                )
            )

            legal_form = BookingPropertyLegalForm(
                instance=getattr(
                    property_obj,
                    "bookingpropertylegal",
                    None
                )
            )

            current_step = property_obj.current_step

        else:

            property_form = BookingPropertyForm()
            setup_form = BookingPropertySetupForm()
            pricing_form = BookingPropertyPricingForm()
            legal_form = BookingPropertyLegalForm()

            current_step = "property"


        return render(
            request,
            "property/add_property_all_in_one.html",
            {
                "property_form": property_form,
                "setup_form": setup_form,
                "pricing_form": pricing_form,
                "legal_form": legal_form,
                "property_obj": property_obj,
                "current_step": current_step,
            }
        )


    # =====================================================
    # WHICH STEP WAS SUBMITTED?
    # =====================================================

    step = request.POST.get("step")


    # =====================================================
    # STEP 1 - PROPERTY
    # =====================================================

    if step == "property":

        property_form = BookingPropertyForm(request.POST)

        if property_form.is_valid():

            property_obj = property_form.save(commit=False)

            property_obj.owner = request.user

            property_obj.current_step = "setup"

            property_obj.save()

            return redirect(
                "continue_property",
                property_id=property_obj.id
            )

        return render(
            request,
            "property/add_property_all_in_one.html",
            {
                "property_form": property_form,
                "setup_form": BookingPropertySetupForm(),
                "pricing_form": BookingPropertyPricingForm(),
                "legal_form": BookingPropertyLegalForm(),
                "current_step": "property",
                "property_obj": None,
            }
        )


    # =====================================================
    # STEP 2 - SETUP
    # =====================================================

    if step == "setup":

        if not property_obj:
            return redirect("add_property_all_in_one")

        setup_form = BookingPropertySetupForm(request.POST)

        if setup_form.is_valid():

            setup_obj, created = BookingPropertySetup.objects.get_or_create(
                property=property_obj
            )

            setup_form = BookingPropertySetupForm(
                request.POST,
                instance=setup_obj
            )

            if setup_form.is_valid():
                setup_form.save()

            property_obj.current_step = "photos"

            property_obj.save(
                update_fields=["current_step"]
            )

            return redirect(
                "continue_property",
                property_id=property_obj.id
            )

        return render(
            request,
            "property/add_property_all_in_one.html",
            {
                "property_form": BookingPropertyForm(
                    instance=property_obj
                ),
                "setup_form": setup_form,
                "pricing_form": BookingPropertyPricingForm(),
                "legal_form": BookingPropertyLegalForm(),
                "current_step": "setup",
                "property_obj": property_obj,
            }
        )


    # =====================================================
    # STEP 3 - PHOTOS
    # =====================================================

    if step == "photos":

        if not property_obj:
            return redirect("add_property_all_in_one")

        images = request.FILES.getlist("image")

        for image in images:

            BookingPropertyPhoto.objects.create(
                property=property_obj,
                image=image
            )

        property_obj.current_step = "pricing"

        property_obj.save(
            update_fields=["current_step"]
        )

        return redirect(
            "continue_property",
            property_id=property_obj.id
        )


    # =====================================================
    # STEP 4 - PRICING
    # =====================================================

    if step == "pricing":

        if not property_obj:
            return redirect("add_property_all_in_one")

        pricing_obj, created = BookingPropertyPricing.objects.get_or_create(
            property=property_obj
        )

        pricing_form = BookingPropertyPricingForm(
            request.POST,
            instance=pricing_obj
        )

        if pricing_form.is_valid():

            pricing_form.save()

            property_obj.current_step = "legal"

            property_obj.save(
                update_fields=["current_step"]
            )

            return redirect(
                "continue_property",
                property_id=property_obj.id
            )

        return render(
            request,
            "property/add_property_all_in_one.html",
            {
                "property_form": BookingPropertyForm(
                    instance=property_obj
                ),
                "setup_form": BookingPropertySetupForm(),
                "pricing_form": pricing_form,
                "legal_form": BookingPropertyLegalForm(),
                "current_step": "pricing",
                "property_obj": property_obj,
            }
        )


    # =====================================================
    # STEP 5 - LEGAL
    # =====================================================

    if step == "legal":

        if not property_obj:
            return redirect("add_property_all_in_one")

        legal_obj, created = BookingPropertyLegal.objects.get_or_create(
            property=property_obj
        )

        legal_form = BookingPropertyLegalForm(
            request.POST,
            instance=legal_obj
        )

        if legal_form.is_valid():

            legal_form.save()

            property_obj.current_step = "complete"

            property_obj.save(
                update_fields=["current_step"]
            )

            return redirect("my_properties")

        return render(
            request,
            "property/add_property_all_in_one.html",
            {
                "property_form": BookingPropertyForm(
                    instance=property_obj
                ),
                "setup_form": BookingPropertySetupForm(),
                "pricing_form": BookingPropertyPricingForm(),
                "legal_form": legal_form,
                "current_step": "legal",
                "property_obj": property_obj,
            }
        )


    return redirect("add_property_all_in_one")



def my_properties(request):
    # Only show properties added by the logged-in user
    properties = BookingProperty.objects.filter(owner=request.user)
    return render(request, "property/my_properties.html", {
        "properties": properties
    })


def property_detail(request, pk):
    property_obj = get_object_or_404(BookingProperty, pk=pk, owner=request.user)

    # Related objects
    setup = getattr(property_obj, 'bookingpropertysetup', None)
    pricing = getattr(property_obj, 'bookingpropertypricing', None)
    legal = getattr(property_obj, 'bookingpropertylegal', None)
    photos = property_obj.photos.all()

    return render(request, "property/property_detail.html", {
        "property": property_obj,
        "setup": setup,
        "pricing": pricing,
        "legal": legal,
        "photos": photos,
    })


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BookingProperty

@login_required
def property_delete(request, pk):
    prop = get_object_or_404(BookingProperty, pk=pk, owner=request.user)
    if request.method == 'POST':
        prop.delete()
        return redirect('my_properties')
    return redirect('my_properties')

from django.shortcuts import render
from django.db.models import Q
from .models import BookingProperty

TANZANIA_REGIONS = [
    'Arusha', 'Dar es Salaam', 'Dodoma', 'Geita', 'Iringa', 'Kagera', 'Katavi',
    'Kigoma', 'Kilimanjaro', 'Lindi', 'Manyara', 'Mara', 'Mbeya', 'Morogoro',
    'Mtwara', 'Mwanza', 'Njombe', 'Pwani', 'Rukwa', 'Ruvuma', 'Shinyanga',
    'Simiyu', 'Singida', 'Tabora', 'Tanga', 'Zanzibar North', 'Zanzibar South',
    'Zanzibar West', 'Zanzibar Central/South', 'Zanzibar Urban/West'
]

def booking_properties(request, property_type):

    # Only verified owners and properties that are not closed
    properties = BookingProperty.objects.filter(
        property_type=property_type,
        owner__attachments__is_verified=True,
    ).exclude(status='closed').distinct()

    keyword = request.GET.get("keyword", "")
    region = request.GET.get("region", "")
    type_filter = request.GET.get("property_type_filter", "")

    if keyword:
        properties = properties.filter(
            Q(property_name__icontains=keyword) |
            Q(property_description__icontains=keyword) |
            Q(address__icontains=keyword)
        )

    if region:
        properties = properties.filter(region=region)

    if type_filter:
        properties = properties.filter(property_type=type_filter)

    context = {
        "properties": properties,
        "property_type": property_type.replace("_", " ").title(),
        "tanzania_regions": TANZANIA_REGIONS,
        "property_type_choices": BookingProperty.PROPERTY_TYPE_CHOICES,
    }

    return render(request, "customer/booking_property_lists.html", context)



from django.shortcuts import render, get_object_or_404
from .models import BookingProperty

def booking_property_detail(request, pk):
    # Public access – removes owner=request.user
    property_obj = get_object_or_404(BookingProperty, pk=pk)

    # Related objects
    setup = getattr(property_obj, 'bookingpropertysetup', None)
    pricing = getattr(property_obj, 'bookingpropertypricing', None)
    legal = getattr(property_obj, 'bookingpropertylegal', None)
    photos = property_obj.photos.all()

    return render(request, "customer/property_detail.html", {
        "property": property_obj,
        "setup": setup,
        "pricing": pricing,
        "legal": legal,
        "photos": photos,
    })




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from .models import Booking, BookingProperty, BookingPropertyPricing
from .forms import BookingForm


@login_required(login_url='signin')
def book_property(request, pk):
    property_obj = get_object_or_404(BookingProperty, pk=pk)
    pricing = get_object_or_404(BookingPropertyPricing, property=property_obj)

    featured_properties = BookingProperty.objects.filter(
        property_type=property_obj.property_type
    ).exclude(id=property_obj.id)[:6]

    # Single form instance for GET & POST
    form = BookingForm(request.POST or None, property=property_obj)

    if request.method == "POST" and form.is_valid():

        room_type = form.cleaned_data["room_type"]
        guests = form.cleaned_data["guests"]
        check_in = form.cleaned_data["check_in"]
        check_out = form.cleaned_data["check_out"]

        nights = (check_out - check_in).days

        # Validation: only check that check-out is after check-in
        if nights <= 0:
            form.add_error("check_out", "Check-out must be after check-in.")

        else:
            # Safe price calculation
            price_per_night = pricing.base_price_per_night
            total_price = nights * price_per_night

            # Save booking
            # Save booking and assign to a variable
            new_booking = Booking.objects.create(
                user=request.user,
                property=property_obj,
                room_type=room_type,
                check_in=check_in,
                check_out=check_out,
                guests=guests,
                nights=nights,
                price_per_night=price_per_night,
                total_price=total_price,
                status="pending",
            )

            messages.success(request, "Booking submitted successfully!")
            return redirect('booking_success', booking_id=new_booking.id)


    return render(
        request,
        "customer/book_property.html",
        {
            "form": form,
            "property": property_obj,
            "featured_properties": featured_properties,
        },
    )

def booking_success(request, booking_id=None):
    booking = None
    if booking_id:
        booking = Booking.objects.filter(id=booking_id, user=request.user).first()
    return render(request, 'customer/booking_success.html', {'booking': booking})


def book(request, booking_id=None):

    return render(request, 'customer/book.html')





from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Booking

@login_required(login_url='login')
def my_bookings(request):
    # Get all bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'customer/my_bookings.html', {'bookings': bookings})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Booking, BookingProperty

@login_required(login_url='login')
def owner_bookings(request):
    # Get all properties owned by this user
    properties = BookingProperty.objects.filter(owner=request.user)

    # Get all bookings for these properties
    bookings = Booking.objects.filter(property__in=properties).order_by('-created_at')

    return render(request, 'property/owner_bookings.html', {'bookings': bookings})




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Booking, BookingProperty

@login_required(login_url='login')
def owner_booking_detail(request, booking_id):
    """
    Display detailed info for a single booking to the property owner.
    """
    # Get the booking, ensure the property belongs to the logged-in owner
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        property__owner=request.user
    )

    context = {
        'booking': booking
    }
    return render(request, 'property/owner_booking_detail.html', context)



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Booking

def update_owner_booking_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'cancelled', 'completed']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking {booking.id} status updated to {new_status.title()}.")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect(request.META.get('HTTP_REFERER', 'bookings_list'))



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import BookingProperty
from .forms import BookingPropertyStatusForm


@login_required
def update_property_booking_status(request, pk):
    property = get_object_or_404(
        BookingProperty,
        pk=pk,
        owner=request.user
    )

    if request.method == "POST":
        form = BookingPropertyStatusForm(
            request.POST,
            instance=property
        )

        if form.is_valid():
            form.save()
           
    else:
        form = BookingPropertyStatusForm(instance=property)

    return redirect("my_properties")


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import BookingProperty, Booking, PropertyReview
from .forms import PropertyReviewForm


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import BookingProperty, PropertyReview
from .forms import PropertyReviewForm


@login_required
def add_property_review(request, property_id):

    property = get_object_or_404(
        BookingProperty,
        id=property_id
    )

    if request.method == "POST":

        form = PropertyReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.property = property
            review.user = request.user

            review.save()

            return redirect(
    "booking_property_detail",
    pk=property.id
)

    else:
        form = PropertyReviewForm()

    return render(
        request,
        "customer/add_review.html",
        {
            "property": property,
            "form": form,
        }
    )


from django.shortcuts import get_object_or_404, render
from .models import BookingProperty


def property_reviews(request, property_id):

    property = get_object_or_404(
        BookingProperty,
        id=property_id
    )

    reviews = property.reviews.select_related(
        'user'
    ).all()

    return render(
        request,
        'customer/property_reviews.html',
        {
            'property': property,
            'reviews': reviews,
        }
    )