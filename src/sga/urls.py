"""Rutas del proyecto. La E0 solo define el inicio de sesión y una página protegida provisional."""
from django.urls import include, path

urlpatterns = [
    path('', include('cuentas.urls')),
]
