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

class BookDetailViewSet(viewsets.ModelViewSet):
    queryset = tb_book_detail.objects.all().select_related("libro_padre")
    serializer_class = BookDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = tb_student.objects.all().order_by('apellidos', 'nombres')
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]  # solo logueados

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = tb_category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = tb_author.objects.all().order_by("id")
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    queryset = tb_book.objects.all().select_related("autor").prefetch_related("category")
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoanViewSet(viewsets.ModelViewSet):
    queryset = tb_loan.objects.all().select_related("estudiante", "libro", "libro__libro_padre")
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # al eliminar el préstamo, liberar el ejemplar
        libro = instance.libro
        super().perform_destroy(instance)
        if libro:
            libro.estado_prestamo = False
            libro.save(update_fields=["estado_prestamo"])


class StaffRoleViewSet(viewsets.ModelViewSet):
    queryset = StaffRole.objects.all()
    serializer_class = StaffRoleSerializer
    permission_classes = [IsLibraryStaff]


class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.select_related('user', 'role')
    serializer_class = StaffProfileSerializer
    permission_classes = [IsLibraryStaff]
