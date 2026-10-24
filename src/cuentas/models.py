from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Q

from . import cifrado


class AdministradorManager(BaseUserManager):
    def crear_administrador(self, usuario, contrasena):
        """Crea la única cuenta (RN-25). El `id` es 1 porque una restricción de la tabla solo
        admite esa fila. La creación pública no existe: se hará con un comando en el servidor
        (RF-27), que aún no está escrito."""
        if not usuario:
            raise ValueError('El usuario es obligatorio.')
        administrador = self.model(id=1, usuario=usuario)
        administrador.set_password(contrasena)
        administrador.save(using=self._db, force_insert=True)
        return administrador

    def create_user(self, *args, **kwargs):
        raise NotImplementedError('Use Administrador.objects.crear_administrador (RF-27).')

    create_superuser = create_user


class Administrador(AbstractBaseUser):
    """Cuenta administradora única (RF-26, RF-27, RN-25; entidad ADMINISTRADOR del MDD v0.7).

    Sin PermissionsMixin: no hay roles ni permisos de Django, así que cada vista debe exigir
    la autenticación de forma explícita.
    """
    usuario = models.CharField(max_length=150, unique=True)
    secreto_segundo_factor = models.TextField(blank=True, default='')
    segundo_factor_activo = models.BooleanField(default=False)
    fallos_consecutivos = models.PositiveIntegerField(default=0)
    espera_hasta = models.DateTimeField(null=True, blank=True)
    ultimo_intervalo_totp = models.BigIntegerField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = []

    objects = AdministradorManager()

    class Meta:
        verbose_name = 'administrador'
        verbose_name_plural = 'administradores'
        constraints = [
            # RN-25: una sola cuenta. Con id único, solo cabe la fila de id 1.
            models.CheckConstraint(condition=Q(id=1), name='administrador_una_sola_cuenta'),
        ]

    def __str__(self):
        return self.usuario

    def fijar_secreto_segundo_factor(self, secreto):
        """Guarda el secreto TOTP (base32) cifrado; nunca en claro."""
        self.secreto_segundo_factor = cifrado.cifrar(secreto)

    def secreto_segundo_factor_en_claro(self):
        return cifrado.descifrar(self.secreto_segundo_factor)
