# account/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # example
    path('', views.home, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("register/", views.register, name="register"),
    path('login/', views.login_view, name='login'),
    path('logout',views.logout_user, name='logout'),
      path('about/', views.about, name='about'),
       path('profile/', views.user_profile, name='user_profile'),
      path('account/change-password/', views.change_password, name='change_password'),
      path('account/owner-change-password/', views.property_change_password, name='property_change_password'),
   

]