from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('student/create/', views.student_create, name='student_create'),
    path('student/update/<int:id>/', views.student_update, name='student_update'),
    path('student/delete/<int:id>/', views.student_delete, name='student_delete'),
]
