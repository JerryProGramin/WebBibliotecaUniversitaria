# web/views.py
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.serializers import CustomRegisterSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

API_LOGIN = 'http://127.0.0.1:8000/api/auth/login/'

def login_view(request):
    register_errors = {}
    login_error = None

    # LOGIN
    if request.method == 'POST' and request.POST.get('form_type') == 'login':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)     # <- aquí se guarda la sesión
            return redirect('dashboard')  # <- esto sí te manda al dashboard
        else:
            login_error = "Usuario o contraseña incorrectos."

    # REGISTRO (igual que antes)
    if request.method == 'POST' and request.POST.get('form_type') == 'register':
        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "password1": request.POST.get("password1"),
            "password2": request.POST.get("password2"),
            "first_name": request.POST.get("first_name", ""),
            "last_name": request.POST.get("last_name", ""),
        }
        serializer = CustomRegisterSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(request)
            return redirect('login')
        else:
            register_errors = serializer.errors

    return render(request, 'web/login.html', {
        "error": login_error,
        "register_errors": register_errors,
    })


@login_required(login_url='login')
def dashboard(request):
    context = {
        'libros_disponibles': 50000,
        'libros_prestados': 20000,
        'libros_espera': 10000,
    }
    return render(request, 'web/dashboard.html', context)


def logout_view(request):
    # borra el token que guardamos cuando hicimos login contra el API
    request.session.flush()
    return redirect('login')
