from django.shortcuts import render,get_object_or_404
from django.forms import formset_factory
from .models import BookingProperty, BookingPropertyPhoto
from .forms import (
    BookingPropertyForm,
    BookingPropertySetupForm,
    BookingPropertyPricingForm,
    BookingPropertyLegalForm,
    BookingPropertyPhotoForm,
)

def add_property_all_in_one(request):
    success = False

    if request.method == "POST":
        property_form = BookingPropertyForm(request.POST)
        setup_form = BookingPropertySetupForm(request.POST)
        pricing_form = BookingPropertyPricingForm(request.POST)
        legal_form = BookingPropertyLegalForm(request.POST)

        if (property_form.is_valid() and setup_form.is_valid() and
            pricing_form.is_valid() and legal_form.is_valid()):

            # Save main property
            property_obj = property_form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()

            # Save setup
            setup_obj = setup_form.save(commit=False)
            setup_obj.property = property_obj
            setup_obj.save()

            # Save pricing
            pricing_obj = pricing_form.save(commit=False)
            pricing_obj.property = property_obj
            pricing_obj.save()

            # Save legal
            legal_obj = legal_form.save(commit=False)
            legal_obj.property = property_obj
            legal_obj.save()

            # Save multiple images
            images = request.FILES.getlist("image")  # <-- get all uploaded files
            for image in images:
                BookingPropertyPhoto.objects.create(
                    property=property_obj,
                    image=image
                )

            success = True

    else:
        property_form = BookingPropertyForm()
        setup_form = BookingPropertySetupForm()
        pricing_form = BookingPropertyPricingForm()
        legal_form = BookingPropertyLegalForm()

    return render(request, "property/add_property_all_in_one.html", {
        "property_form": property_form,
        "setup_form": setup_form,
        "pricing_form": pricing_form,
        "legal_form": legal_form,
        "success": success,
    })




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

    # ✅ ONLY show properties whose OWNER has VERIFIED attachment
    properties = BookingProperty.objects.filter(
        property_type=property_type,
        owner__attachments__is_verified=True
    ).distinct()

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
        "property_type_choices": BookingProperty.PROPERTY_TYPE_CHOICES
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

from .models import Booking, BookingProperty, BookingPropertyPricing
from .forms import BookingForm


@login_required(login_url='login')
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




