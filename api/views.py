# api/views.py
from rest_framework import viewsets, permissions
from library.models import (
    tb_user, tb_author, tb_category, tb_book,
    tb_book_detail, tb_student, tb_loan
)
from accounts.models import StaffProfile, StaffRole
from .serializers import (
    TbUserSerializer, AuthorSerializer, CategorySerializer,
    BookSerializer, BookDetailSerializer, StudentSerializer, LoanSerializer,
    StaffProfileSerializer, StaffRoleSerializer
)

class IsLibraryStaff(permissions.BasePermission):
    """
    Permiso simple: deja pasar si el usuario está autenticado.
    Aquí podrías validar que tenga StaffProfile.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class TbUserViewSet(viewsets.ModelViewSet):
    queryset = tb_user.objects.all()
    serializer_class = TbUserSerializer
    permission_classes = [IsLibraryStaff]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = tb_author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibraryStaff]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = tb_category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLibraryStaff]


class BookViewSet(viewsets.ModelViewSet):
    queryset = tb_book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibraryStaff]


class BookDetailViewSet(viewsets.ModelViewSet):
    queryset = tb_book_detail.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [IsLibraryStaff]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = tb_student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsLibraryStaff]


class LoanViewSet(viewsets.ModelViewSet):
    queryset = tb_loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsLibraryStaff]


class StaffRoleViewSet(viewsets.ModelViewSet):
    queryset = StaffRole.objects.all()
    serializer_class = StaffRoleSerializer
    permission_classes = [IsLibraryStaff]


class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.select_related('user', 'role')
    serializer_class = StaffProfileSerializer
    permission_classes = [IsLibraryStaff]
