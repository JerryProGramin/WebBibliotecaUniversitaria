# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TbUserViewSet, AuthorViewSet, CategoryViewSet,
    BookViewSet, BookDetailViewSet, StudentViewSet, LoanViewSet,
    StaffRoleViewSet, StaffProfileViewSet
)

router = DefaultRouter()
router.register(r'sys-users', TbUserViewSet)
router.register(r'students', StudentViewSet, basename='student')
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"authors", AuthorViewSet, basename="authors")
router.register(r"books", BookViewSet, basename="books")
router.register(r"book-details", BookDetailViewSet, basename="book-details")
router.register(r"loans", LoanViewSet, basename="loans") 
router.register(r'staff-roles', StaffRoleViewSet)
router.register(r'staff-profiles', StaffProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
