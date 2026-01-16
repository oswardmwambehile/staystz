from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from .forms import RegistrationForm

def home(request):
    return render(request, 'customer/home.html')


def about(request):
    return render(request, 'customer/about.html')




from django.shortcuts import render
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




def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            messages.success(request, "Account created successfully. Please wait for verification.")
            login(request, user)  # Optional: remove if you don't want auto login

            return redirect("register")  # Change to your homepage name
        else:
            # Invalid form → errors displayed in red automatically inside template
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegistrationForm()

    return render(request, "customer/register.html", {"form": form})



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm

def login_view(request):
    # Only redirect if explicitly logged in and trying to access login page
    if request.user.is_authenticated and request.method != 'POST':
        if request.user.user_type == 'customer':
            return redirect('index')
        elif request.user.user_type == 'property_owner':
            return redirect('dashboard')
        elif request.user.user_type == 'admin':
            return redirect('admin:index')

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            # Authenticate user manually in case form uses custom validation
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name()}!")

                # Redirect based on user type
                if user.user_type == 'customer':
                    return redirect('index')
                elif user.user_type == 'property_owner':
                    return redirect('dashboard')
                elif user.user_type == 'admin':
                    return redirect('admin:index')
            else:
                messages.error(request, "Login failed. Check your email and password.")
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'customer/login.html', {'form': form})



def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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

