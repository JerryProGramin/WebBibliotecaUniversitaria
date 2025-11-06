from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'web/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'web/dashboard.html')

@login_required
def dashboard_metrics_api(request):
    """Devuelve métricas de ejemplo desde la base de datos para los gráficos del dashboard."""
    # Ejemplos: conteos simples. Ajusta a tus tablas reales si existen.
    data = {
        'cards': {
            'libros': 0,
            'alumnos': 0,
            'prestamos': 0,
        },
        'prestamos_por_mes': {
            'labels': ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
            'values': [0,0,0,0,0,0,0,0,0,0,0,0]
        }
    }
    try:
        with connection.cursor() as cursor:
            # Ajusta los nombres de tablas si tus modelos existen y se migraron
            cursor.execute("SELECT COUNT(*) FROM api_libro")
            data['cards']['libros'] = cursor.fetchone()[0]
    except Exception:
        pass
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM api_alumno")
            data['cards']['alumnos'] = cursor.fetchone()[0]
    except Exception:
        pass
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM api_prestamo")
            data['cards']['prestamos'] = cursor.fetchone()[0]
            # Ejemplo de préstamos por mes (reemplaza fecha_prestamo por tu campo real)
            cursor.execute(
                """
                SELECT MONTH(fecha_prestamo) as m, COUNT(*)
                FROM api_prestamo
                GROUP BY MONTH(fecha_prestamo)
                ORDER BY m
                """
            )
            rows = cursor.fetchall()
            values = [0]*12
            for m, c in rows:
                if 1 <= m <= 12:
                    values[m-1] = c
            data['prestamos_por_mes']['values'] = values
    except Exception:
        pass
    return JsonResponse(data)

@login_required
def libro_view(request):
    return render(request, 'web/libro.html')

@login_required
def alumno_view(request):
    return render(request, 'web/alumno.html')

@login_required
def prestamo_view(request):
    return render(request, 'web/prestamo.html')

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('dashboard')
