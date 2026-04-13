from django.shortcuts import render, get_object_or_404
from .models import NewsEvent

# List view: show all news and events
def news_event_list(request):
    posts = NewsEvent.objects.filter(is_active=True).order_by('-publish_date')
    context = {
        'posts': posts
    }
    return render(request, 'customer/news_event_list.html', context)


# Detail view: show single news or event
def news_event_detail(request, slug):
    post = get_object_or_404(NewsEvent, slug=slug, is_active=True)
    context = {
        'post': post
    }
    return render(request, 'customer/news_event_detail.html', context)


def help_center(request):
    return render(request, "customers/help_center.html")
def manage_trips(request):
   
    return render(request, "customers/manage_trips.html")



def terms(request):
    return render(request, 'customers/terms.html')


def privacy(request):
    return render(request, 'customers/privacy.html')

def cookies(request):
    return render(request, 'customers/cookies.html')


def security_policy(request):
    return render(request, "customers/security_policy.html")


def how_we_work(request):
    return render(request, 'customers/who.html')

def sustainability(request):
    return render(request, 'customers/sustainability.html')

def careers(request):
    return render(request, 'customers/careers.html')

def cooperate(request):
    return render(request, 'customers/cooperate.html')


from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings


def booking_support(request):
    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        booking_id = request.POST.get("booking_id")
        message = request.POST.get("message")

        full_message = f"""
Booking Support Request

Name: {name}
Email: {email}
Booking ID: {booking_id}

Message:
{message}
"""

        send_mail(
            subject="StayStz Booking Support Request",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        success = True

    return render(request, "customers/booking_support.html", {"success": success})




def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(name, email, message)  

    return render(request, 'customers/contact.html')