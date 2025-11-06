# api/serializers.py
from rest_framework import serializers
from library.models import (
    tb_user, tb_author, tb_category, tb_book,
    tb_book_detail, tb_student, tb_loan
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_user
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_author
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_book
        fields = '__all__'


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_book_detail
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_student
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_loan
        fields = '__all__'
