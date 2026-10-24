from django.contrib.postgres.operations import BtreeGistExtension
from django.db import migrations


class Migration(migrations.Migration):
    """Extensión `btree_gist` para la restricción de exclusión de solape de contratos, R2 (ADR-031,
    decisión 1; la usa la E2). Es una extensión «de confianza»: la puede crear el rol dueño, que es
    dueño de la base, sin ser superusuario."""
    dependencies = [('nucleo', '0003_organizacion_inicial')]
    operations = [BtreeGistExtension()]
