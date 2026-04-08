from django.urls import path
from . import views

urlpatterns = [

    path('car-rental/add/', views.add_car_all_in_one, name='add_car_rental'),
    path('car-category/', views.car, name='car'),
     path("car-rental-booking/<int:car_id>/book/", views.book_car, name="book_car"),
    path('my-car-rentals/', views.my_car_rentals, name='my_car_rentals'),
     path('car-rentals/<int:pk>/', views.car_rental_detail, name='car_rental_detail'),
     path('car-rentals-details/<int:pk>/', views.car_rental_details, name='car_rental_details'),
      path('car-rentals/<str:car_type>/', views.car_rental_list, name='car_rental_list_by_type'),
      path('my-bookings-car/', views.my_bookings_car, name='my_bookings-car'),
      path('bookings-services/', views.bookings_services, name='bookings-services'),
      path('about-staystz/', views.about, name='about-stays'),
      path('mission/', views.mission_view, name='mission'),


]
