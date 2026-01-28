from django.urls import path
from . import views

urlpatterns = [
    path("add-property/", views.add_property_all_in_one, name="add_property_all_in_one"),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('booking/<str:property_type>/', views.booking_properties, name='booking_properties'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path("booking-property/<int:pk>/", views.booking_property_detail, name="booking_property_detail"),
     path('property/delete/<int:pk>/', views.property_delete, name='property_delete'),
      path('property/<int:pk>/book/', views.book_property, name='book_property'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),
     path('my-bookings/', views.my_bookings, name='my_bookings'),
     path('categories-bookings/', views.book, name='book'),
     path('owner/bookings/', views.owner_bookings, name='owner_bookings'),
     path('owner/bookings/<int:booking_id>/', views.owner_booking_detail, name='owner_booking_detail'),
     path('booking/<int:pk>/update-status/', views.update_owner_booking_status, name='update_booking_status'),
    
    
]
