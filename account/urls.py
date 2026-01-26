# account/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # example
    path('', views.home, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("register/", views.signup, name="register"),
    path("verify-email/<str:username>/", views.verify_email, name="verify-email"),
    path("resend-otp/", views.resend_otp, name="resend-otp"),
    path("login/", views.signin, name="signin"),
    path('logout',views.logout_user, name='logout'),
      path('about/', views.about, name='about'),
       path('profile/', views.user_profile, name='user_profile'),
       path("search/", views.global_search, name="global_search"),
       path('city/<str:city>/', views.city_search, name='city_search'),
      path('account/change-password/', views.change_password, name='change_password'),
      path('account/owner-change-password/', views.property_change_password, name='property_change_password'),
   

]