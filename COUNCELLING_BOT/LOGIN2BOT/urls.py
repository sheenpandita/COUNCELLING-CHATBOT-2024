from django.contrib import admin
from django.urls import path, include
from .  import  views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL points to the home view
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]