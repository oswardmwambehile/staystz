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





def terms(request):
    return render(request, 'customers/terms.html')


def privacy(request):
    return render(request, 'customers/privacy.html')

def cookies(request):
    return render(request, 'customers/cookies.html')


def security_policy(request):
    return render(request, "customers/security_policy.html")