from django.db import models

class tb_category(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class tb_author(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class tb_book(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    anio_publicacion = models.IntegerField()
    category = models.ManyToManyField('tb_category', blank=True)
    autor = models.ForeignKey(tb_author, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class tb_book_detail(models.Model):
    libro_padre = models.ForeignKey(tb_book, on_delete=models.CASCADE)
    codigo_isbn = models.CharField(max_length=13)
    estado_fisico = models.CharField(max_length=100)
    estado_prestamo = models.BooleanField()
    
    def __str__(self):
        return self.codigo_isbn

class tb_user(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class tb_student(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)

    def __str__(self):
        return self.nombres

class tb_loan(models.Model):
    estudiante = models.ForeignKey(tb_student, on_delete=models.CASCADE)
    libro = models.ForeignKey(tb_book_detail, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    comentarios = models.CharField(max_length=200)

    def __str__(self):
        return self.estudiante

