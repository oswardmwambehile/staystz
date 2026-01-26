from django.urls import path
from . import views

urlpatterns = [
    path('attachments/', views.add_attachment, name='add_attachment'),
    path('owner-categories/', views.service, name='services-category'),
]
