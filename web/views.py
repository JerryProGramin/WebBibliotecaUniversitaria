from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from library.models import tb_book, tb_student, tb_loan, tb_book_detail,tb_author,tb_category,tb_student
from django.utils import timezone
from django.views.decorators.http import require_http_methods

@login_required
def dashboard(request):
    total_libros = tb_book.objects.count()
    total_estudiantes = tb_student.objects.count()
    prestamos_activos = tb_loan.objects.count()
    return render(request, 'web/dashboard.html', {
        'total_libros': total_libros,
        'total_estudiantes': total_estudiantes,
        'prestamos_activos': prestamos_activos,
    })

@login_required
@require_http_methods(["GET", "POST"])
def prestamo_create(request):
    if request.method == "POST":
        estudiante_id = request.POST.get('estudiante')
        ejemplar_id = request.POST.get('ejemplar')
        fecha_fin = request.POST.get('fecha_fin')
        comentarios = request.POST.get('comentarios', '')

        estudiante = tb_student.objects.get(id=estudiante_id)
        ejemplar = tb_book_detail.objects.get(id=ejemplar_id)

        # aquí podrías validar si el ejemplar está disponible
        tb_loan.objects.create(
            fecha_inicio=timezone.now().date(),
            fecha_fin=fecha_fin,
            comentarios=comentarios,
            libro=ejemplar,
            estudiante=estudiante
        )

        # podrías marcar el ejemplar como prestado:
        ejemplar.estado_prestamo = True
        ejemplar.save()

        return redirect('dashboard')

    estudiantes = tb_student.objects.all()
    ejemplares_disponibles = tb_book_detail.objects.filter(estado_prestamo=False)
    return render(request, 'web/prestamo_form.html', {
        'estudiantes': estudiantes,
        'ejemplares': ejemplares_disponibles
    })

@login_required
def book_create(request):
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        autor_id = request.POST.get('autor')
        anio = request.POST.get('anio_publicacion')
        categorias_ids = request.POST.getlist('categorias')

        autor = tb_author.objects.get(id=autor_id)
        book = tb_book.objects.create(
            titulo=titulo,
            autor=autor,
            anio_publicacion=anio
        )
        if categorias_ids:
            book.category.set(categorias_ids)

        return redirect('dashboard')

    autores = tb_author.objects.all()
    categorias = tb_category.objects.all()
    return render(request, 'web/book_form.html', {
        'autores': autores,
        'categorias': categorias
    })

@login_required
def student_create(request):
    if request.method == "POST":
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        dni = request.POST.get('dni')
        tb_student.objects.create(
            nombres=nombres,
            apellidos=apellidos,
            dni=dni
        )
        return redirect('dashboard')
    return render(request, 'web/student_form.html')