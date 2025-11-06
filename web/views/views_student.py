from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from web.models import tb_user, tb_student

def home_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    estudiantes = tb_student.objects.all()
    return render(request, 'web/home.html', {'estudiantes': estudiantes})

# Crear estudiante
def student_create(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        dni = request.POST['dni']
        tb_student.objects.create(nombres=nombres, apellidos=apellidos, dni=dni)
        return redirect('home')

    return render(request, 'web/student_form.html', {'accion': 'Crear'})

# Editar estudiante
def student_update(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')

    estudiante = get_object_or_404(tb_student, id=id)

    if request.method == 'POST':
        estudiante.nombres = request.POST['nombres']
        estudiante.apellidos = request.POST['apellidos']
        estudiante.dni = request.POST['dni']
        estudiante.save()
        return redirect('home')

    return render(request, 'web/student_form.html', {'accion': 'Editar', 'estudiante': estudiante})

# Eliminar estudiante
def student_delete(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')

    estudiante = get_object_or_404(tb_student, id=id)
    estudiante.delete()
    return redirect('home')