# library/models.py
from django.db import models

class tb_user(models.Model):
    # esto venía en tus migraciones iniciales
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'tb_user'

    def __str__(self):
        return self.nombre


class tb_author(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tb_author'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class tb_category(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tb_category'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class tb_book(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey('tb_author', on_delete=models.CASCADE)
    anio_publicacion = models.IntegerField()
    # de tu migración: libro puede tener muchas categorías
    category = models.ManyToManyField('tb_category', blank=True)

    class Meta:
        db_table = 'tb_book'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


class tb_book_detail(models.Model):
    # ejemplares físicos
    codigo_isbn = models.CharField(max_length=13)
    estado_fisico = models.CharField(max_length=100)
    estado_prestamo = models.BooleanField()  # True = prestado, False = disponible
    libro_padre = models.ForeignKey('tb_book', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_book_detail'

    def __str__(self):
        return f"{self.libro_padre.titulo} - {self.codigo_isbn}"


class tb_student(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)

    class Meta:
        db_table = 'tb_student'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"


class tb_loan(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    comentarios = models.CharField(max_length=200)
    libro = models.ForeignKey('tb_book_detail', on_delete=models.CASCADE)
    estudiante = models.ForeignKey('tb_student', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_loan'

    def __str__(self):
        return f"Préstamo {self.id} - {self.estudiante}"
