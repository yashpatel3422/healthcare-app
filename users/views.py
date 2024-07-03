from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from .models import PatientProfile, DoctorProfile 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages


def home(request):
    return render(request, 'users/home.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data['user_type']
            if user_type == 'patient':
                user.is_patient = True
                user.save()
                PatientProfile.objects.create(user=user)
            elif user_type == 'doctor':
                user.is_doctor = True
                user.save()
                DoctorProfile.objects.create(user=user)
            user.save()
            messages.success(request, 'Signup successful! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


# users/views.py

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_patient:
                return redirect('patient_dashboard')
            elif user.is_doctor:
                return redirect('doctor_dashboard')
            else:
                return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')


@login_required
def user_dashboard(request):
    if request.user.is_patient:
        return render(request, 'users/patient_dashboard.html')
    elif request.user.is_doctor:
        return render(request, 'users/doctor_dashboard.html')
    else:
        return HttpResponse("Unauthorized user type")
  
@login_required
def patient_dashboard_view(request):
    return render(request, 'users/patient_dashboard.html')

@login_required
def doctor_dashboard_view(request):
    return render(request, 'users/doctor_dashboard.html')
