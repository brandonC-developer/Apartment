from django.contrib.auth.backends import BaseBackend

from .autenticacion import comprobar_contrasena
from .models import Administrador


class BackendAdministrador(BaseBackend):
    """Verifica solo la contraseña y el contador de intentos.

    ADVERTENCIA: una contraseña correcta NO basta para iniciar sesión (RNF-01): la vista debe
    exigir también `autenticacion.verificar_totp` antes de llamar a `login()` (lo hace `views.segundo_paso`). No
    llame a `authenticate()` + `login()` en otro sitio. Sin PermissionsMixin, este backend no concede permisos.
    """

    def authenticate(self, request, usuario=None, contrasena=None, **kwargs):
        if usuario is None or contrasena is None:
            return None
        respuesta = comprobar_contrasena(usuario, contrasena)
        return respuesta.administrador if respuesta.correcto else None

    def get_user(self, user_id):
        try:
            return Administrador.objects.get(pk=user_id)
        except Administrador.DoesNotExist:
            return None
