from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='web/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('', views.dashboard, name='dashboard'),

    path('prestamos/', views.prestamo_create, name='prestamo_create'),
    path('libros/registrar/', views.book_create, name='book_create'),
    path('estudiantes/registrar/', views.student_create, name='student_create'),
]
