from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),   # ya lo tienes
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
]