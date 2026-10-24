from django.urls import path

from . import views

app_name = 'nucleo'
urlpatterns = [
    path('auditoria/', views.consultar_auditoria, name='auditoria'),
]
