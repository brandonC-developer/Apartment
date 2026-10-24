from django.db import migrations


def crear_fila_unica(apps, schema_editor):
    """La organización es una sola fila (id 1) con los valores predeterminados de RF-33: zona
    America/Costa_Rica y proceso diario a las 07:00 (DP-02). Idempotente."""
    Organizacion = apps.get_model('nucleo', 'Organizacion')
    Organizacion.objects.get_or_create(pk=1)


class Migration(migrations.Migration):
    dependencies = [('nucleo', '0002_organizacion')]
    operations = [migrations.RunPython(crear_fila_unica, migrations.RunPython.noop)]
