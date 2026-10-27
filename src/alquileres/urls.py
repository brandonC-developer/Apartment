from django.urls import path

from . import views

app_name = 'alquileres'
urlpatterns = [
    path('contratos/<int:contrato_id>/fotografias/', views.pagina_fotografias_del_contrato, name='fotografias_contrato'),
    path('contratos/<int:contrato_id>/fotografias/subir/', views.subir_fotografia_del_contrato, name='subir_fotografia_contrato'),
    path('contratos/fotografias/<int:pk>/ver/', views.ver_fotografia_del_contrato, name='ver_fotografia_contrato'),
    path('contratos/fotografias/<int:pk>/descargar/', views.descargar_fotografia_del_contrato, name='descargar_fotografia_contrato'),
    path('propiedades/<int:propiedad_id>/cedula/', views.pagina_cedula_de_la_propiedad, name='cedula_propiedad'),
    path('propiedades/<int:propiedad_id>/cedula/<str:cara>/', views.subir_cedula_desde_la_propiedad, name='subir_cedula_propiedad'),
]
