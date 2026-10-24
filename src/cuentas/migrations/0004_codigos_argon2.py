from django.db import migrations, models


def borrar_codigos_antiguos(apps, schema_editor):
    """Los códigos guardados hasta ahora eran SHA-256 sin sal y no se pueden convertir a Argon2id
    (solo existía el hash). Se borran: dejan de servir y hay que emitir códigos nuevos con la
    pantalla «Códigos de recuperación nuevos». Solo había códigos de prueba (decisión del
    solicitante, 24-oct-2026, actualización 2026-10-24o)."""
    apps.get_model('cuentas', 'CodigoRecuperacion').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0003_administrador_token_registro_hash_and_more'),
    ]

    operations = [
        migrations.RunPython(borrar_codigos_antiguos, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='codigorecuperacion',
            name='hash_codigo',
            field=models.CharField(max_length=255),
        ),
    ]
