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

class BookDetailSerializer(serializers.ModelSerializer):
    libro_titulo = serializers.CharField(source="libro_padre.titulo", read_only=True)

    class Meta:
        model = tb_book_detail
        fields = [
            "id",
            "codigo_isbn",
            "estado_fisico",
            "estado_prestamo",
            "libro_padre",
            "libro_titulo",
        ]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_student
        fields = ['id', 'nombres', 'apellidos', 'dni']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_category
        fields = ["id", "nombre"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_author
        fields = ["id", "nombre"]

class BookSerializer(serializers.ModelSerializer):
    # solo mandas ID de autor y categorías, pero también devolvemos nombres
    autor_nombre = serializers.CharField(source="autor.nombre", read_only=True)
    categorias_nombres = serializers.SerializerMethodField()

    class Meta:
        model = tb_book
        fields = [
            "id",
            "titulo",
            "anio_publicacion",
            "autor",
            "autor_nombre",
            "category",           # lista de IDs (ManyToMany)
            "categorias_nombres", # lista de nombres para mostrar en la tabla
        ]

    def get_categorias_nombres(self, obj):
        return [c.nombre for c in obj.category.all()]

class LoanSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.SerializerMethodField()
    libro_titulo = serializers.CharField(source="libro.libro_padre.titulo", read_only=True)
    libro_codigo = serializers.CharField(source="libro.codigo_isbn", read_only=True)

    class Meta:
        model = tb_loan
        fields = [
            "id",
            "fecha_inicio",
            "fecha_fin",
            "comentarios",
            "estudiante",
            "estudiante_nombre",
            "libro",
            "libro_titulo",
            "libro_codigo",
        ]

    def get_estudiante_nombre(self, obj):
        return f"{obj.estudiante.nombres} {obj.estudiante.apellidos}"

    def validate(self, attrs):
        libro = attrs.get("libro")
        if libro and libro.estado_prestamo:
            raise serializers.ValidationError(
                {"libro": "Este ejemplar ya está prestado."}
            )
        return attrs

    def create(self, validated_data):
        loan = super().create(validated_data)
        # marcar ejemplar como prestado
        libro = loan.libro
        libro.estado_prestamo = True
        libro.save(update_fields=["estado_prestamo"])
        return loan
