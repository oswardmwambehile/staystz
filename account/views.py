
from django.shortcuts import render, redirect
from django.contrib import messages



from django.contrib.auth import login,logout

def home(request):
    regions = [
        "Arusha","Dar es Salaam","Dodoma","Geita","Iringa","Kagera","Katavi",
        "Kigoma","Kilimanjaro","Lindi","Manyara","Mara","Mbeya","Morogoro",
        "Mtwara","Mwanza","Njombe","Pemba North","Pemba South","Pwani",
        "Rukwa","Ruvuma","Shinyanga","Simiyu","Singida","Songwe","Tabora",
        "Tanga","Zanzibar Central/South","Zanzibar North","Zanzibar Urban/West"
    ]
    return render(request, 'customers/home.html', {"regions": regions})


def about(request):
    return render(request, 'customer/about.html')





from resedence.models import ResidenceProperty
from booking.models import BookingProperty
from carrental.models import CarRental

def dashboard(request):
    user = request.user  # get logged-in user

    # Counts for this user only
    booking_count = BookingProperty.objects.filter(owner=user).count()
    residence_count = ResidenceProperty.objects.filter(owner=user).count()
    car_rental_count = CarRental.objects.filter(owner=user).count()

    # Residence property statuses (for this user)
    available_count = ResidenceProperty.objects.filter(owner=user, status='open').count()
    hold_count = ResidenceProperty.objects.filter(owner=user, status='hold').count()
    closed_count = ResidenceProperty.objects.filter(owner=user, status='closed').count()

    # Latest 3 Residence Properties for this user
    residence_properties = ResidenceProperty.objects.filter(owner=user).order_by('-created_at')[:3]

    context = {
        'booking_count': booking_count,
        'residence_count': residence_count,
        'car_rental_count': car_rental_count,
        'available_count': available_count,
        'hold_count': hold_count,
        'closed_count': closed_count,
        'residence_properties': residence_properties,
    }

    return render(request, 'property/dashboard.html', context)


from .forms import RegisterForm
from .models import OtpToken
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout


# Create your views here.





from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .forms import RegisterForm
from .models import OtpToken
from django.conf import settings

def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # user inactive until verified
            user.save()

            # create OTP
            otp = OtpToken.objects.create(
                user=user,
                otp_expires_at=timezone.now() + timedelta(minutes=5)
            )

            # send email
            try:
                send_mail(
                    subject="Email Verification",
                    message=f"Hi {user.username},\n\nYour OTP is: {otp.otp_code}\nIt expires in 5 minutes.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False
                )
            except Exception as e:
                messages.warning(request, f"Account created but failed to send OTP email: {e}")
                return redirect("verify-email", username=user.username)

            messages.success(request, "Account created successfully! An OTP has been sent to your email.")
            return redirect("verify-email", username=user.username)

    return render(request, "customer/signup.html", {"form": form})


def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST.get("otp_email")
        User = get_user_model()

        if not user_email or not User.objects.filter(email=user_email).exists():
            messages.warning(request, "This email doesn't exist")
            return redirect("resend-otp")

        user = User.objects.get(email=user_email)

        # cooldown check
        last_otp = OtpToken.objects.filter(user=user).order_by('-otp_created_at').first()
        if last_otp and timezone.now() - last_otp.otp_created_at < timedelta(seconds=60):
            messages.warning(request, "Wait 1 min before requesting another OTP")
            return redirect("resend-otp")

        # daily limit check
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if OtpToken.objects.filter(user=user, otp_created_at__gte=today_start).count() >= 5:
            messages.warning(request, "Reached daily OTP limit")
            return redirect("resend-otp")

        # create OTP
        otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timedelta(minutes=5))

        # send email safely
        try:
            send_mail(
                subject="Email Verification",
                message=f"Hi {user.username},\n\nYour OTP is: {otp.otp_code}\nIt expires in 5 minutes.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False
            )
        except Exception as e:
            messages.error(request, f"Failed to send OTP email: {e}")
            return redirect("resend-otp")

        messages.success(request, "A new OTP has been sent to your email")
        return redirect("verify-email", username=user.username)

    return render(request, "customer/resend_otp.html")


def verify_email(request, username):
    # Get user or return 404 if not found
    user = get_user_model().objects.get(username=username)

    # Get the latest OTP for this user
    user_otp = OtpToken.objects.filter(user=user).last()

    if request.method == 'POST':
        otp_input = request.POST.get('otp_code', '').strip()  # Get OTP from form safely

        if not user_otp:
            messages.warning(request, "No OTP found. Please request a new one!")
            return redirect("resend-otp")  # Or redirect back to verification page

        if user_otp.otp_code == otp_input:
            # Check if OTP is expired
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account activated successfully! You can now login.")
                return redirect("signin")
            else:
                messages.warning(request, "The OTP has expired, please request a new OTP!")
                return redirect("verify-email", username=user.username)
        else:
            messages.warning(request, "Invalid OTP entered! Please enter a valid OTP.")
            return redirect("verify-email", username=user.username)

    # GET request, just render form
    return render(request, "customer/verify_token.html", {"username": username})






def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {request.user.username}, you are now logged-in")
            return redirect("index")

        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")

    return render(request, "customer/login.html")




def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')


from django.contrib.auth.decorators import login_required

from .forms import SecurePasswordChangeForm
from django.contrib import messages

@login_required
def change_password(request):
    if request.method == "POST":
        form = SecurePasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed successfully!")
            return redirect("change_password")  # or any page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SecurePasswordChangeForm(request.user)

    return render(request, "customer/change_password.html", {"form": form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def user_profile(request):
    return render(request, 'customer/profile.html', {
        'user': request.user
    })



@login_required
def property_change_password(request):
    if request.method == "POST":
        form = SecurePasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed successfully!")
            return redirect("change_password")  # or any page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SecurePasswordChangeForm(request.user)

    return render(request, "property/change_password.html", {"form": form})



from django.db.models import Q

from booking.models import BookingProperty
from resedence.models import ResidenceProperty
from carrental.models import CarRental


def global_search(request):
    region = request.GET.get("region", "").strip()
    property_type = request.GET.get("property_type", "").strip()

    booking_results = BookingProperty.objects.none()
    residence_results = ResidenceProperty.objects.none()
    car_results = CarRental.objects.none()

    # ----------------------------
    # Booking properties search
    # ----------------------------
    if region:
        booking_results = BookingProperty.objects.filter(
            Q(region__iexact=region)
        )

        if property_type:
            booking_results = booking_results.filter(
                property_type__iexact=property_type
            )

    # ----------------------------
    # Residence properties search
    # ----------------------------
    if region:
        residence_results = ResidenceProperty.objects.filter(
            Q(region__iexact=region),
            status="open"
        )

        if property_type:
            residence_results = residence_results.filter(
                property_type__iexact=property_type
            )

    # ----------------------------
    # OPTIONAL: Car search (disabled unless you want it)
    # ----------------------------
    # if region:
    #     car_results = CarRental.objects.filter(
    #         available_region__iexact=region
    #     )

    context = {
        "region": region,
        "property_type": property_type,
        "booking_results": booking_results,
        "residence_results": residence_results,
        "car_results": car_results,
    }

    return render(request, "customer/search_results.html", context)





from django.db.models import Q
from booking.models import BookingProperty
from carrental.models import CarRental
from resedence.models import ResidenceProperty

def city_search(request, city):
    city = city.strip()  # remove extra spaces if any

    # Query Booking Properties
    booking_results = BookingProperty.objects.filter(
        Q(district__icontains=city) |
        Q(region__icontains=city) |
        Q(country__icontains=city)
    )

    # Query Residence Properties
    residence_results = ResidenceProperty.objects.filter(
        Q(district__icontains=city) |
        Q(region__icontains=city) |
        Q(country__icontains=city),
        status="open"
    )

    # Query Car Rentals
    car_results = CarRental.objects.filter(
        Q(car_name__icontains=city) |
        Q(car_description__icontains=city)
    )

    context = {
        "property_type": city,  # for template header
        "booking_results": booking_results,
        "residence_results": residence_results,
        "car_results": car_results,
    }

    return render(request, "customer/city_results.html", context)
