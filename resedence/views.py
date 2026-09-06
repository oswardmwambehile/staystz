from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    ResidenceProperty,
    ResidencePropertySetup,
    OfficePropertySetup,
    ResidencePropertyPhoto,
    ResidencePropertyPricing,
    ResidencePropertyLegal,
)

from .forms import (
    ResidencePropertyForm,
    ResidencePropertySetupForm,
    OfficePropertySetupForm,
    ResidencePropertyPricingForm,
    ResidencePropertyLegalForm,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_setup_forms(property_obj=None):
    """
    Return the correct setup form depending on property type.

    Office Space:
        OfficePropertySetupForm

    Apartment / Homes:
        ResidencePropertySetupForm
    """

    if property_obj is None:

        return (
            ResidencePropertySetupForm(),
            OfficePropertySetupForm()
        )


    # --------------------------------------------------------
    # OFFICE SPACE
    # --------------------------------------------------------

    if property_obj.property_type == "office_space":

        office_instance = getattr(
            property_obj,
            "office_setup",
            None
        )

        office_form = OfficePropertySetupForm(
            instance=office_instance
        )

        return None, office_form


    # --------------------------------------------------------
    # APARTMENT / HOMES
    # --------------------------------------------------------

    residence_instance = getattr(
        property_obj,
        "residencepropertysetup",
        None
    )

    residence_form = ResidencePropertySetupForm(
        instance=residence_instance
    )

    return residence_form, None


# ============================================================
# MAIN VIEW
# ============================================================

def add_residence_property_all_in_one(
    request,
    property_id=None
):

    # ========================================================
    # GET EXISTING PROPERTY
    # ========================================================

    if property_id:

        property_obj = get_object_or_404(
            ResidenceProperty,
            id=property_id,
            owner=request.user
        )

    else:

        property_obj = None


    # ========================================================
    # GET REQUEST
    # ========================================================

    if request.method == "GET":

        # ====================================================
        # NEW PROPERTY
        # ====================================================

        if property_obj is None:

            property_form = ResidencePropertyForm()

            residence_setup_form = (
                ResidencePropertySetupForm()
            )

            office_setup_form = (
                OfficePropertySetupForm()
            )

            pricing_form = (
                ResidencePropertyPricingForm()
            )

            legal_form = (
                ResidencePropertyLegalForm()
            )

            current_step = "property"


        # ====================================================
        # EXISTING PROPERTY
        # ====================================================

        else:

            property_form = ResidencePropertyForm(
                instance=property_obj
            )


            # ------------------------------------------------
            # CORRECT SETUP FORM
            # ------------------------------------------------

            (
                residence_setup_form,
                office_setup_form
            ) = get_setup_forms(property_obj)


            # ------------------------------------------------
            # PRICING
            # ------------------------------------------------

            pricing_form = ResidencePropertyPricingForm(
                instance=getattr(
                    property_obj,
                    "residencepropertypricing",
                    None
                ),
                property_obj=property_obj
            )


            # ------------------------------------------------
            # LEGAL
            # ------------------------------------------------

            legal_form = ResidencePropertyLegalForm(
                instance=getattr(
                    property_obj,
                    "residencepropertylegal",
                    None
                )
            )


            current_step = property_obj.current_step


        return render(
            request,
            "property/add_residence_property.html",
            {
                "property_form": property_form,

                "residence_setup_form":
                    residence_setup_form,

                "office_setup_form":
                    office_setup_form,

                "pricing_form":
                    pricing_form,

                "legal_form":
                    legal_form,

                "property_obj":
                    property_obj,

                "current_step":
                    current_step,
            }
        )


    # ========================================================
    # POST
    # ========================================================

    step = request.POST.get("step")


    # ========================================================
    # STEP 1
    # BASIC PROPERTY INFORMATION
    # ========================================================

    if step == "property":

        property_form = ResidencePropertyForm(
            request.POST
        )


        if property_form.is_valid():

            property_obj = property_form.save(
                commit=False
            )

            property_obj.owner = request.user

            property_obj.current_step = "setup"

            property_obj.save()


            return redirect(
                "continue_residence_property",
                property_id=property_obj.id
            )


        # ----------------------------------------------------
        # FORM ERROR
        # ----------------------------------------------------

        return render(
            request,
            "property/add_residence_property.html",
            {
                "property_form":
                    property_form,

                "residence_setup_form":
                    ResidencePropertySetupForm(),

                "office_setup_form":
                    OfficePropertySetupForm(),

                "pricing_form":
                    ResidencePropertyPricingForm(),

                "legal_form":
                    ResidencePropertyLegalForm(),

                "property_obj":
                    None,

                "current_step":
                    "property",
            }
        )


    # ========================================================
    # MAKE SURE PROPERTY EXISTS FOR ALL OTHER STEPS
    # ========================================================

    if not property_obj:

        return redirect(
            "add_residence_property_all_in_one"
        )


    # ========================================================
    # STEP 2
    # PROPERTY SETUP
    # ========================================================

    if step == "setup":


        # ====================================================
        # OFFICE SPACE
        # ====================================================

        if property_obj.property_type == "office_space":

            office_setup_obj, created = (
                OfficePropertySetup.objects.get_or_create(
                    property=property_obj
                )
            )


            office_setup_form = OfficePropertySetupForm(
                request.POST,
                instance=office_setup_obj
            )


            if office_setup_form.is_valid():

                office_setup_form.save()


                property_obj.current_step = "photos"

                property_obj.save(
                    update_fields=[
                        "current_step",
                        "updated_at"
                    ]
                )


                return redirect(
                    "continue_residence_property",
                    property_id=property_obj.id
                )


            # ------------------------------------------------
            # OFFICE FORM ERROR
            # ------------------------------------------------

            return render(
                request,
                "property/add_residence_property.html",
                {
                    "property_form":
                        ResidencePropertyForm(
                            instance=property_obj
                        ),

                    "residence_setup_form":
                        None,

                    "office_setup_form":
                        office_setup_form,

                    "pricing_form":
                        ResidencePropertyPricingForm(
                            property_obj=property_obj
                        ),

                    "legal_form":
                        ResidencePropertyLegalForm(),

                    "property_obj":
                        property_obj,

                    "current_step":
                        "setup",
                }
            )


        # ====================================================
        # APARTMENT / HOMES
        # ====================================================

        residence_setup_obj, created = (
            ResidencePropertySetup.objects.get_or_create(
                property=property_obj
            )
        )


        residence_setup_form = (
            ResidencePropertySetupForm(
                request.POST,
                instance=residence_setup_obj
            )
        )


        if residence_setup_form.is_valid():

            residence_setup_form.save()


            property_obj.current_step = "photos"

            property_obj.save(
                update_fields=[
                    "current_step",
                    "updated_at"
                ]
            )


            return redirect(
                "continue_residence_property",
                property_id=property_obj.id
            )


        # ----------------------------------------------------
        # RESIDENCE FORM ERROR
        # ----------------------------------------------------

        return render(
            request,
            "property/add_residence_property.html",
            {
                "property_form":
                    ResidencePropertyForm(
                        instance=property_obj
                    ),

                "residence_setup_form":
                    residence_setup_form,

                "office_setup_form":
                    None,

                "pricing_form":
                    ResidencePropertyPricingForm(
                        property_obj=property_obj
                    ),

                "legal_form":
                    ResidencePropertyLegalForm(),

                "property_obj":
                    property_obj,

                "current_step":
                    "setup",
            }
        )


    # ========================================================
    # STEP 3
    # PHOTOS
    # ========================================================

    if step == "photos":

        images = request.FILES.getlist(
            "image"
        )


        # ====================================================
        # MAXIMUM 100 PHOTOS
        # ====================================================

        if len(images) > 100:

            (
                residence_setup_form,
                office_setup_form
            ) = get_setup_forms(property_obj)


            return render(
                request,
                "property/add_residence_property.html",
                {
                    "property_form":
                        ResidencePropertyForm(
                            instance=property_obj
                        ),

                    "residence_setup_form":
                        residence_setup_form,

                    "office_setup_form":
                        office_setup_form,

                    "pricing_form":
                        ResidencePropertyPricingForm(
                            property_obj=property_obj
                        ),

                    "legal_form":
                        ResidencePropertyLegalForm(),

                    "property_obj":
                        property_obj,

                    "current_step":
                        "photos",

                    "error":
                        "Maximum 100 images allowed.",
                }
            )


        # ====================================================
        # SAVE PHOTOS
        # ====================================================

        for image in images:

            ResidencePropertyPhoto.objects.create(
                property=property_obj,
                image=image
            )


        property_obj.current_step = "pricing"

        property_obj.save(
            update_fields=[
                "current_step",
                "updated_at"
            ]
        )


        return redirect(
            "continue_residence_property",
            property_id=property_obj.id
        )


    # ========================================================
    # STEP 4
    # PRICING
    # ========================================================

    if step == "pricing":

        pricing_obj, created = (
            ResidencePropertyPricing.objects.get_or_create(
                property=property_obj
            )
        )


        pricing_form = ResidencePropertyPricingForm(
            request.POST,
            instance=pricing_obj,
            property_obj=property_obj
        )


        if pricing_form.is_valid():

            pricing_form.save()


            property_obj.current_step = "legal"

            property_obj.save(
                update_fields=[
                    "current_step",
                    "updated_at"
                ]
            )


            return redirect(
                "continue_residence_property",
                property_id=property_obj.id
            )


        # ----------------------------------------------------
        # PRICING ERROR
        # ----------------------------------------------------

        (
            residence_setup_form,
            office_setup_form
        ) = get_setup_forms(property_obj)


        return render(
            request,
            "property/add_residence_property.html",
            {
                "property_form":
                    ResidencePropertyForm(
                        instance=property_obj
                    ),

                "residence_setup_form":
                    residence_setup_form,

                "office_setup_form":
                    office_setup_form,

                "pricing_form":
                    pricing_form,

                "legal_form":
                    ResidencePropertyLegalForm(),

                "property_obj":
                    property_obj,

                "current_step":
                    "pricing",
            }
        )


    # ========================================================
    # STEP 5
    # LEGAL
    # ========================================================

    if step == "legal":

        legal_obj, created = (
            ResidencePropertyLegal.objects.get_or_create(
                property=property_obj
            )
        )


        legal_form = ResidencePropertyLegalForm(
            request.POST,
            instance=legal_obj
        )


        if legal_form.is_valid():

            legal_form.save()


            property_obj.current_step = "complete"

            property_obj.save(
                update_fields=[
                    "current_step",
                    "updated_at"
                ]
            )


            return redirect(
                "my_residence_properties"
            )


        # ----------------------------------------------------
        # LEGAL ERROR
        # ----------------------------------------------------

        (
            residence_setup_form,
            office_setup_form
        ) = get_setup_forms(property_obj)


        return render(
            request,
            "property/add_residence_property.html",
            {
                "property_form":
                    ResidencePropertyForm(
                        instance=property_obj
                    ),

                "residence_setup_form":
                    residence_setup_form,

                "office_setup_form":
                    office_setup_form,

                "pricing_form":
                    ResidencePropertyPricingForm(
                        instance=getattr(
                            property_obj,
                            "residencepropertypricing",
                            None
                        ),
                        property_obj=property_obj
                    ),

                "legal_form":
                    legal_form,

                "property_obj":
                    property_obj,

                "current_step":
                    "legal",
            }
        )


    # ========================================================
    # UNKNOWN STEP
    # ========================================================

    return redirect(
        "add_residence_property_all_in_one"
    )







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
    ).exclude(status='closed').distinct()

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


@login_required(login_url="signin")
def book_residence(request, property_id):

    property_obj = get_object_or_404(
        ResidenceProperty,
        id=property_id
    )

    pricing = property_obj.residencepropertypricing

    if request.method == "POST":

        form = ResidenceBookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            booking.property = property_obj
            booking.user = request.user

            total_price = 0

            # -----------------------
            # BnB Booking (Daily)
            # -----------------------
            if (
                booking.need_bnb == "yes"
                and booking.check_in_date
                and booking.check_out_date
                and pricing.base_price_per_day
            ):

                days = (
                    booking.check_out_date
                    - booking.check_in_date
                ).days

                if days <= 0:
                    days = 1

                total_price = days * pricing.base_price_per_day

            # -----------------------
            # Residence Booking
            # -----------------------
            elif (
                booking.need_bnb == "no"
                and booking.rent_duration
                and pricing.base_price
            ):

                total_price = (
                    booking.rent_duration
                    * pricing.base_price
                )

            booking.total_price = total_price
            booking.save()

            try:

                subject = (
                    f"New Booking Request - "
                    f"{property_obj.property_name}"
                )

                context = {
                    "booking": booking,
                    "property": property_obj,
                }

                html_content = render_to_string(
                    "emails/residence_booking_email.html",
                    context,
                )

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=f"StayTZ Bookings <{settings.EMAIL_HOST_USER}>",
                    to=[property_obj.owner.email],
                )

                email.attach_alternative(
                    html_content,
                    "text/html"
                )

                email.send(fail_silently=False)

            except Exception as e:
                print(e)

            messages.success(
                request,
                "Booking submitted successfully."
            )

            return redirect(
                "residence_booking_success",
                booking_id=booking.id,
            )

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:

        form = ResidenceBookingForm()

    return render(
        request,
        "customer/book_residence.html",
        {
            "form": form,
            "property": property_obj,
            "pricing": pricing,
        },
    )




from django.shortcuts import get_object_or_404, render

def residence_booking_success(request, booking_id):
    booking = get_object_or_404(ResidenceBooking, id=booking_id)

    return render(request, "customer/residence_booking_success.html", {
        "booking": booking
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


from .forms import ResidencePropertyReviewForm


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


from .forms import ResidencePropertyReviewForm


@login_required(login_url="signin")
def resedence_add_property_review(request, property_id):

    property = get_object_or_404(
       ResidenceProperty,
        id=property_id
    )

    if request.method == "POST":

        form = ResidencePropertyReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.property = property
            review.user = request.user

            review.save()

            return redirect(
    "residence_property_details",
    pk=property.id
)

    else:
        form = ResidencePropertyReviewForm()

    return render(
        request,
        "customer/resedince_add_review.html",
        {
            "property": property,
            "form": form,
        }
    )


from django.shortcuts import get_object_or_404, render
from .models import ResidenceProperty


def resedence_property_reviews(request, property_id):

    property = get_object_or_404(
        ResidenceProperty,
        id=property_id
    )

    reviews = property.reviews.select_related(
        'user'
    ).all()

    return render(
        request,
        'customer/residence_property_reviews.html',
        {
            'property': property,
            'reviews': reviews,
        }
    )