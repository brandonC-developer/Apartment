from django.urls import path

from . import views

app_name = 'cuentas'
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('entrar/', views.iniciar_sesion, name='iniciar_sesion'),
    path('entrar/codigo/', views.segundo_paso, name='segundo_paso'),
    path('entrar/registro/', views.registro_segundo_factor, name='registro_segundo_factor'),
    path('cuenta/codigos/', views.codigos_nuevos, name='codigos_nuevos'),
    path('salir/', views.cerrar_sesion, name='cerrar_sesion'),
]
