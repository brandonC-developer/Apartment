from django.db import migrations

# R12 y R21: la anulación (de un contrato o de una obligación) se completa una sola vez y no se cambia después. La base
# lo impone con un disparador, porque los privilegios por columna no distinguen «primera vez» de «otra vez».
CREAR = """
CREATE FUNCTION alquileres_contrato_anulacion_una_vez() RETURNS trigger AS $$
BEGIN
    IF OLD.anulado_en IS NOT NULL AND (NEW.anulado_en IS DISTINCT FROM OLD.anulado_en
                                       OR NEW.motivo_anulacion IS DISTINCT FROM OLD.motivo_anulacion) THEN
        RAISE EXCEPTION 'La anulacion de un contrato se completa una sola vez' USING ERRCODE = 'integrity_constraint_violation';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER contrato_anulacion_una_vez BEFORE UPDATE ON alquileres_contrato
    FOR EACH ROW EXECUTE FUNCTION alquileres_contrato_anulacion_una_vez();

CREATE FUNCTION alquileres_obligacion_anulacion_una_vez() RETURNS trigger AS $$
BEGIN
    IF OLD.anulada_en IS NOT NULL AND (NEW.anulada_en IS DISTINCT FROM OLD.anulada_en
                                       OR NEW.motivo_anulacion IS DISTINCT FROM OLD.motivo_anulacion) THEN
        RAISE EXCEPTION 'La anulacion de una obligacion se completa una sola vez' USING ERRCODE = 'integrity_constraint_violation';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER obligacion_anulacion_una_vez BEFORE UPDATE ON alquileres_obligacion
    FOR EACH ROW EXECUTE FUNCTION alquileres_obligacion_anulacion_una_vez();
"""

QUITAR = """
DROP TRIGGER obligacion_anulacion_una_vez ON alquileres_obligacion;
DROP FUNCTION alquileres_obligacion_anulacion_una_vez();
DROP TRIGGER contrato_anulacion_una_vez ON alquileres_contrato;
DROP FUNCTION alquileres_contrato_anulacion_una_vez();
"""


class Migration(migrations.Migration):
    dependencies = [('alquileres', '0001_initial')]
    operations = [migrations.RunSQL(CREAR, QUITAR)]
