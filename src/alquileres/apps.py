from django.apps import AppConfig


class AlquileresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alquileres'

    def ready(self):
        # CA-29: el bloqueo real de desactivar a un inquilino con contrato (decisión 5 de la E1).
        from inquilinos import bloqueos as bloqueos_de_inquilinos

        from . import bloqueos
        bloqueos_de_inquilinos.registrar(bloqueos.por_contrato)
