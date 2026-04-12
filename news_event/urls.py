from django.urls import path
from . import views

urlpatterns = [
    path('terms-of-services/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('cookies/', views.cookies, name='cookies'),
    path('careers/', views.careers, name='careers'),
    path('sustainability/', views.sustainability, name='sustainability'),
     path('how-we-work/', views.how_we_work, name='how_we_work'),
    path('events-news/', views.news_event_list, name='events-list'),
    path('security-policy/', views.security_policy, name='security_policy'),# list view
    path('events_news/<slug:slug>/', views.news_event_detail, name='event_detail'), # detail view,
    
    path('contact/', views.contact, name='contact'),
]