# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('saludo/', views.SaludoAPIView.as_view(), name='saludo'),
]
