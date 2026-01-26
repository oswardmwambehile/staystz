
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
    return render(request, 'customer/home.html', {"regions": regions})


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





def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
    context = {"form": form}
    return render(request, "customer/signup.html", context)




def verify_email(request, username):
    user = get_user_model().objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    
    if request.method == 'POST':
        # valid token
        if user_otp.otp_code == request.POST['otp_code']:
            
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():
                user.is_active=True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("signin")
            
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=user.username)
        
        
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)
        
    context = {}
    return render(request, "customer/verify_token.html", context)




def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
            # email variables
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{user.username}
                                
                                """
            sender = "clintonmatics@gmail.com"
            receiver = [user.email, ]
        
        
            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")
        
           
    context = {}
    return render(request, "customer/resend_otp.html", context)




def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
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
