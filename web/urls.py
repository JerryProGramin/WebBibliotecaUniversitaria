from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),   # ya lo tienes
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('estudiantes/', views.students_page, name='students_page'),
    path("categorias/", views.categories_page, name="categories_page"),
    path("autores/", views.authors_page, name="authors_page"),
    path("libros/", views.books_page, name="books_page"),
    path("prestamos/", views.loans_page, name="loans_page"),
]