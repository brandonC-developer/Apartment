"""Rutas del proyecto. La E0 define el inicio de sesión, una página protegida provisional y la
consulta de la auditoría y, desde la E1, las fotografías de los inquilinos."""
from django.urls import include, path

urlpatterns = [
    path('', include('cuentas.urls')),
    path('', include('nucleo.urls')),
    path('', include('inquilinos.urls')),
    path('', include('alquileres.urls')),
]
