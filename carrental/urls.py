from django.urls import path
from . import views

urlpatterns = [

    path('car-rental/add/', views.add_car_all_in_one, name='add_car_rental'),
    path('my-car-rentals/', views.my_car_rentals, name='my_car_rentals'),
     path('car-rentals/<int:pk>/', views.car_rental_detail, name='car_rental_detail'),
     path('car-rentals-details/<int:pk>/', views.car_rental_details, name='car_rental_details'),
      path('car-rentals/<str:car_type>/', views.car_rental_list, name='car_rental_list_by_type'),
]
