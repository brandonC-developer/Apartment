from django.urls import path

from . import pantallas, views

app_name = 'inquilinos'
urlpatterns = [
    path('inquilinos/', pantallas.lista, name='lista'),
    path('inquilinos/nuevo/', pantallas.nuevo, name='nuevo'),
    path('inquilinos/<int:inquilino_id>/', pantallas.ficha, name='ficha'),
    path('inquilinos/<int:inquilino_id>/editar/', pantallas.editar, name='editar'),
    path('inquilinos/<int:inquilino_id>/desactivar/', pantallas.desactivar, name='desactivar'),
    path('inquilinos/<int:inquilino_id>/reactivar/', pantallas.reactivar, name='reactivar'),
    path('inquilinos/<int:inquilino_id>/consentimiento/revocar/', pantallas.revocar_consentimiento,
         name='revocar_consentimiento'),
    path('inquilinos/<int:inquilino_id>/fotografias/', views.pagina_fotografias, name='fotografias'),
    path('inquilinos/<int:inquilino_id>/fotografias/<str:cara>/', views.subir_fotografia, name='subir_fotografia'),
    path('inquilinos/documentos/<int:pk>/ver/', views.ver_documento, name='ver_documento'),
    path('inquilinos/documentos/<int:pk>/descargar/', views.descargar_documento, name='descargar_documento'),
]
