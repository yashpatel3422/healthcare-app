# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/patient/', views.patient_dashboard_view, name='patient_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard_view, name='doctor_dashboard'),
]
