# api/serializers.py
from rest_framework import serializers
from library.models import (
    tb_user, tb_author, tb_category, tb_book,
    tb_book_detail, tb_student, tb_loan
)
from accounts.models import StaffProfile, StaffRole
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class StaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRole
        fields = '__all__'


class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StaffProfile
        fields = ['id', 'user', 'role', 'is_active_staff']


class TbUserSerializer(serializers.ModelSerializer):
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
