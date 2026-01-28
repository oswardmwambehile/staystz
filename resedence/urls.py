from django.urls import path
from . import views

urlpatterns = [
    path("add-residence/", views.add_residence_property_all_in_one, name="add_residence_all_in_one"),
     path('my-properties/', views.my_residence_properties, name='my_residence_properties'),
      path(
        'residence/<int:pk>/',
        views.residence_property_detail,
        name='residence_property_detail'
    ),

    path(
        'residence/<int:pk>/delete/',
        views.residence_property_delete,
        name='residence_property_delete'
    ),

    path('residence/<int:pk>/update-status/', views.update_residence_status, name='update_residence_status'),
      path('residences/', views.residence_properties, name='residence_property_list_all'),
      path('residences-categories/', views.resedence, name='residence'),
      path('residence-property/<int:pk>/', views.residence_property_details, name='residence_property_details'),
     path('residences/<str:property_type>/', views.residence_properties, name='residence_properties_type'),
]
