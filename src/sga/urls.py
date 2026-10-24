"""Rutas del proyecto. La E0 define el inicio de sesión, una página protegida provisional y la
consulta de la auditoría."""
from django.urls import include, path

urlpatterns = [
    path('', include('cuentas.urls')),
    path('', include('nucleo.urls')),
]
