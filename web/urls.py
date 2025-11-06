# web/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/metrics/', views.dashboard_metrics_api, name='dashboard_metrics'),
    path('libro/', views.libro_view, name='libro'),
    path('alumno/', views.alumno_view, name='alumno'),
    path('prestamo/', views.prestamo_view, name='prestamo'),
    path('logout/', views.logout_view, name='logout'),
]
