from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # === API principal ===
    path('api/', include('api.urls')),

    # === Autenticación REST ===
    path('api/auth/', include('dj_rest_auth.urls')),  # login/logout/password
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # === Proveedores sociales (Google, GitHub, etc.) ===
    path('accounts/', include('allauth.urls')),

    # === Perfil de staff ===
    path('api/accounts/', include('accounts.urls')),

    # === Web (frontend) ===
    path('', include('web.urls')),
]
