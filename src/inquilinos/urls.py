from django.urls import path

from . import views

app_name = 'inquilinos'
urlpatterns = [
    path('inquilinos/<int:inquilino_id>/fotografias/<str:cara>/', views.subir_fotografia, name='subir_fotografia'),
    path('inquilinos/documentos/<int:pk>/ver/', views.ver_documento, name='ver_documento'),
    path('inquilinos/documentos/<int:pk>/descargar/', views.descargar_documento, name='descargar_documento'),
]
