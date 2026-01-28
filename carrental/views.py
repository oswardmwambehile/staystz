from django.shortcuts import render
from .models import CarRental, CarRentalPhoto
from .forms import (
    CarRentalForm,
    CarRentalSetupForm,
    CarRentalPricingForm,
    CarRentalLegalForm,
)

def add_car_all_in_one(request):
    success = False

    if request.method == "POST":
        car_form = CarRentalForm(request.POST)
        setup_form = CarRentalSetupForm(request.POST)
        pricing_form = CarRentalPricingForm(request.POST)
        legal_form = CarRentalLegalForm(request.POST)

        if car_form.is_valid() and setup_form.is_valid() and pricing_form.is_valid() and legal_form.is_valid():
            car_obj = car_form.save(commit=False)
            car_obj.owner = request.user
            car_obj.save()

            setup_obj = setup_form.save(commit=False)
            setup_obj.car = car_obj
            setup_obj.save()

            pricing_obj = pricing_form.save(commit=False)
            pricing_obj.car = car_obj
            pricing_obj.save()

            legal_obj = legal_form.save(commit=False)
            legal_obj.car = car_obj
            legal_obj.save()

            # Save uploaded images
            images = request.FILES.getlist("image")
            for image in images:
                CarRentalPhoto.objects.create(car=car_obj, image=image)

            success = True
        else:
            # Print errors in console
            print("CAR_FORM_ERRORS:", car_form.errors)
            print("SETUP_FORM_ERRORS:", setup_form.errors)
            print("PRICING_FORM_ERRORS:", pricing_form.errors)
            print("LEGAL_FORM_ERRORS:", legal_form.errors)

    else:
        car_form = CarRentalForm()
        setup_form = CarRentalSetupForm()
        pricing_form = CarRentalPricingForm()
        legal_form = CarRentalLegalForm()

    return render(request, "property/add_car_all_in_one.html", {
        "car_form": car_form,
        "setup_form": setup_form,
        "pricing_form": pricing_form,
        "legal_form": legal_form,
        "success": success,
    })


from django.shortcuts import render
from .models import CarRental

def my_car_rentals(request):
    # Only show car rentals added by the logged-in user
    car_rentals = CarRental.objects.filter(owner=request.user)
    
    return render(request, "property/my_car_rentals.html", {
        "car_rentals": car_rentals
    })

def car(request):
    return render(request, "customer/car.html")


from django.shortcuts import render, get_object_or_404
from .models import CarRental, CarRentalSetup, CarRentalPricing, CarRentalLegal, CarRentalPhoto

def car_rental_detail(request, pk):
    # Only allow the owner to view their car rental
    car = get_object_or_404(CarRental, pk=pk, owner=request.user)

    # Related objects
    setup = getattr(car, 'carrentalsetup', None)
    pricing = getattr(car, 'carrentalpricing', None)
    legal = getattr(car, 'carrentallegal', None)
    photos = car.photos.all()

    return render(request, "property/car_rental_detail.html", {
        "car": car,
        "setup": setup,
        "pricing": pricing,
        "legal": legal,
        "photos": photos,
    })


from django.shortcuts import render
from django.db.models import Q
from .models import CarRental

# List of all Tanzania regions
TANZANIA_REGIONS = [
    'Arusha', 'Dar es Salaam', 'Dodoma', 'Geita', 'Iringa', 'Kagera', 'Katavi',
    'Kigoma', 'Kilimanjaro', 'Lindi', 'Manyara', 'Mara', 'Mbeya', 'Morogoro',
    'Mtwara', 'Mwanza', 'Njombe', 'Pwani', 'Rukwa', 'Ruvuma', 'Shinyanga',
    'Simiyu', 'Singida', 'Tabora', 'Tanga', 'Zanzibar North', 'Zanzibar South',
    'Zanzibar West', 'Zanzibar Central/South', 'Zanzibar Urban/West'
]

def car_rental_list(request, car_type=None):
    """
    List cars optionally filtered by type, region, or keyword.
    """
    # Base queryset
    cars = CarRental.objects.filter(owner__attachments__is_verified=True)

    # Filters from URL or GET parameters
    keyword = request.GET.get("keyword", "")
    region = request.GET.get("region", "")
    car_type_filter = car_type or request.GET.get("car_type", "")

    # Keyword search
    if keyword:
        cars = cars.filter(
            Q(car_name__icontains=keyword) |
            Q(car_description__icontains=keyword) |
            Q(manufacturer__icontains=keyword) |
            Q(registration_number__icontains=keyword)
        )

    # Filter by region (optional)
    if region:
        cars = cars.filter(owner__profile__region=region)  # if owner has profile.region

    # Filter by car type
    if car_type_filter:
        cars = cars.filter(car_type=car_type_filter)

    context = {
        "cars": cars,
        "tanzania_regions": TANZANIA_REGIONS,
        "car_type_choices": CarRental.CAR_TYPE_CHOICES,
        "car_type_selected": car_type_filter,
    }

    return render(request, "customer/car_rental_list.html", context)


from django.shortcuts import render, get_object_or_404
from .models import CarRental, CarRentalSetup, CarRentalPricing, CarRentalLegal, CarRentalPhoto

def car_rental_details(request, pk):
    # Fetch car rental by ID, accessible to any user
    car = get_object_or_404(CarRental, pk=pk)

    # Related objects
    setup = getattr(car, 'carrentalsetup', None)
    pricing = getattr(car, 'carrentalpricing', None)
    legal = getattr(car, 'carrentallegal', None)
    photos = car.photos.all()

    context = {
        "car": car,
        "setup": setup,
        "pricing": pricing,
        "legal": legal,
        "photos": photos,
    }

    return render(request, "customer/car_rental_detail.html", context)
