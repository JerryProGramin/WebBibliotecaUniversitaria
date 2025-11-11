# web/views.py
import requests
from django.shortcuts import render, redirect

API_LOGIN = 'http://127.0.0.1:8000/api/auth/login/'

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        r = requests.post(API_LOGIN, data={'username': username, 'password': password})
        if r.status_code == 200:
            data = r.json()
            token = data.get('key')
            # guardamos el token en la sesión
            request.session['auth_token'] = token
            return redirect('dashboard')
        else:
            return render(request, 'web/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'web/login.html')


def dashboard(request):
    # 👇 aquí está lo importante
    token = request.session.get('auth_token')
    if not token:
        return redirect('login')

    # si hay token, ya lo dejamos ver el dashboard
    return render(request, 'web/dashboard.html')
