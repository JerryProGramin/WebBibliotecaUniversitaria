from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from web.models import tb_user, tb_student

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = tb_user.objects.get(email=email, password=password)
            # Guarda sesión
            request.session['usuario_id'] = user.id
            request.session['usuario_nombre'] = user.nombre
            return redirect('home')  # Redirige a otra página después del login
        except tb_user.DoesNotExist:
            return render(request, 'web/index.html', {'error': 'Credenciales incorrectas :('})

    return render(request, 'web/index.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')