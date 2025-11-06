# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, AuthorViewSet, CategoryViewSet, BookViewSet,
    BookDetailViewSet, StudentViewSet, LoanViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'books', BookViewSet)
router.register(r'book-details', BookDetailViewSet)
router.register(r'students', StudentViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
