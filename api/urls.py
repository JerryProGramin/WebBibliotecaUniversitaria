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
router.register(r'staff-roles', StaffRoleViewSet)
router.register(r'staff-profiles', StaffProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
