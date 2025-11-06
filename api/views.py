# api/views.py
from rest_framework import viewsets
from library.models import (
    tb_user, tb_author, tb_category, tb_book,
    tb_book_detail, tb_student, tb_loan
)
from .serializers import (
    UserSerializer, AuthorSerializer, CategorySerializer, BookSerializer,
    BookDetailSerializer, StudentSerializer, LoanSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = tb_user.objects.all()
    serializer_class = UserSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = tb_author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = tb_category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = tb_book.objects.all()
    serializer_class = BookSerializer


class BookDetailViewSet(viewsets.ModelViewSet):
    queryset = tb_book_detail.objects.all()
    serializer_class = BookDetailSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = tb_student.objects.all()
    serializer_class = StudentSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = tb_loan.objects.all()
    serializer_class = LoanSerializer
