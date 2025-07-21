from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
    path('login/', views.custom_login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('check_otp/', views.check_otp, name='check_otp'),


]