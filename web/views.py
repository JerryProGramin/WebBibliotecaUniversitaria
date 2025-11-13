# web/views.py
import requests
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Count
from django.contrib import messages
from django.db.models.functions import TruncMonth
from datetime import timedelta
import json
from django.utils.safestring import mark_safe
from accounts.serializers import CustomRegisterSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from library.models import (
    tb_student,
    tb_book,
    tb_book_detail,
    tb_loan,
    tb_category,
)

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
    hoy = timezone.now().date()

    # MÉTRICAS RÁPIDAS
    total_students = tb_student.objects.count()
    total_books = tb_book.objects.count()
    total_copies = tb_book_detail.objects.count()
    total_loans = tb_loan.objects.count()
    active_loans = tb_loan.objects.filter(fecha_fin__gte=hoy).count()

    # 📌 1) Libros por categoría (para gráfico de barras / pie)
    cats = (
        tb_category.objects
        .annotate(total=Count("tb_book"))  # reverse de ManyToMany
        .order_by("nombre")
    )

    cat_labels = [c.nombre for c in cats if c.total > 0]
    cat_counts = [c.total for c in cats if c.total > 0]

    # 📌 2) Préstamos por mes (últimos 6 meses)
    seis_meses = hoy - timedelta(days=180)
    loans_month_qs = (
        tb_loan.objects
        .filter(fecha_inicio__gte=seis_meses)
        .annotate(month=TruncMonth("fecha_inicio"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    month_labels = [item["month"].strftime("%b %Y") for item in loans_month_qs]
    month_counts = [item["total"] for item in loans_month_qs]

    context = {
        "total_students": total_students,
        "total_books": total_books,
        "total_copies": total_copies,
        "total_loans": total_loans,
        "active_loans": active_loans,

        # datos JSON para los gráficos
        "cat_labels_json": mark_safe(json.dumps(cat_labels)),
        "cat_counts_json": mark_safe(json.dumps(cat_counts)),
        "month_labels_json": mark_safe(json.dumps(month_labels)),
        "month_counts_json": mark_safe(json.dumps(month_counts)),
    }
    return render(request, "web/dashboard.html", context)


def logout_view(request):
    # borra el token que guardamos cuando hicimos login contra el API
    request.session.flush()
    return redirect('login')

@login_required(login_url='login')
def students_page(request):
    return render(request, 'web/students.html')

@login_required(login_url='login')
def categories_page(request):
    return render(request, "web/categories.html")


@login_required(login_url='login')
def authors_page(request):
    return render(request, "web/authors.html")

@login_required(login_url='login')
def books_page(request):
    return render(request, "web/books.html")

@login_required(login_url='login')
def loans_page(request):
    return render(request, "web/loans.html")