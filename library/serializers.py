from rest_framework import serializers
from .models import tb_author, tb_category, tb_book, tb_student, tb_loan, tb_book_detail

class AuthorSerializer(serializers.ModelSerializer):
    class Meta: model = tb_author; fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta: model = tb_category; fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta: model = tb_book; fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    class Meta: model = tb_student; fields = "__all__"

class LoanDetailSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    class Meta: model = tb_book_detail; fields = "__all__"

class LoanSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.first_name', read_only=True)
    details = LoanDetailSerializer(many=True, read_only=True)
    class Meta: model = tb_loan; fields = "__all__"
