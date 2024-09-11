from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.home, name='home'),  # Root URL points to the home view
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_profile', views.user_profile, name='user_profile'),
    #----------------------------------------------------------------
    path('average_salary', views.average_salary, name='average_salary'),
]
