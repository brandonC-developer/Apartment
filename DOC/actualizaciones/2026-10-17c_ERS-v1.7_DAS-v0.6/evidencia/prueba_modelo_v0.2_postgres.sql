-- Prueba desechable del modelo logico MDD-SGA-001 v0.2 en PostgreSQL.
-- NO es el esquema de produccion ni fija ADR-002: solo comprueba que las
-- restricciones R1-R14 y las derivaciones del modelo se pueden expresar y se cumplen.
-- Uso: psql -p 54329 -U test -d postgres -v ON_ERROR_STOP=1 -f prueba_modelo_v0.2_postgres.sql
DROP DATABASE IF EXISTS sga_prueba;
CREATE DATABASE sga_prueba;
\c sga_prueba
CREATE EXTENSION btree_gist;

CREATE TABLE propiedad (id serial PRIMARY KEY, descripcion text NOT NULL);
CREATE TABLE contrato (
  id serial PRIMARY KEY, propiedad_id int NOT NULL REFERENCES propiedad,
  fecha_inicio date NOT NULL, fecha_fin date, moneda char(3) NOT NULL CHECK (moneda IN ('CRC','USD')),
  anulado boolean NOT NULL DEFAULT false,
  CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio),
  -- R2: ningun dia compartido (ambos extremos inclusive; sin fin = abierto)
  EXCLUDE USING gist (propiedad_id WITH =,
     daterange(fecha_inicio, fecha_fin, '[]') WITH &&) WHERE (NOT anulado)
);
CREATE TABLE condicion_contrato (
  id serial PRIMARY KEY, contrato_id int NOT NULL REFERENCES contrato,
  monto_mensual numeric(14,2) NOT NULL CHECK (monto_mensual > 0),
  dia_vencimiento int NOT NULL CHECK (dia_vencimiento BETWEEN 1 AND 31),
  dias_gracia int NOT NULL CHECK (dias_gracia >= 0),
  vigente_desde date NOT NULL, tipo text NOT NULL CHECK (tipo IN ('inicial','reajuste','correccion')));
CREATE TABLE obligacion (
  id serial PRIMARY KEY, contrato_id int NOT NULL REFERENCES contrato,
  tipo text NOT NULL CHECK (tipo IN ('regular','apertura')),
  periodo_inicio date, periodo_fin date, fecha_vencimiento date NOT NULL, fecha_limite date NOT NULL,
  importe_inicial numeric(14,2) NOT NULL, anulada_en timestamptz,
  CHECK ((tipo='apertura') = (periodo_inicio IS NULL)));
CREATE UNIQUE INDEX r1_regular ON obligacion (contrato_id, periodo_inicio) WHERE tipo='regular';
CREATE UNIQUE INDEX r1_apertura ON obligacion (contrato_id) WHERE tipo='apertura';
CREATE TABLE ajuste_obligacion (
  id serial PRIMARY KEY, obligacion_id int NOT NULL REFERENCES obligacion,
  tipo text NOT NULL CHECK (tipo IN ('reajuste','correccion','prorrateo_fin','ajuste_manual')),
  importe_delta numeric(14,2) NOT NULL CHECK (importe_delta <> 0),
  motivo text, registrado_en timestamptz NOT NULL DEFAULT now(),
  CHECK (tipo NOT IN ('correccion','ajuste_manual') OR motivo IS NOT NULL));
CREATE TABLE deposito (id serial PRIMARY KEY, contrato_id int NOT NULL UNIQUE REFERENCES contrato, importe_total numeric(14,2) NOT NULL);
CREATE TABLE movimiento (
  id serial PRIMARY KEY, tipo text NOT NULL CHECK (tipo IN ('abono','reversion')),
  obligacion_id int REFERENCES obligacion, deposito_id int REFERENCES deposito,
  importe_aplicado numeric(14,2) NOT NULL CHECK (importe_aplicado > 0),
  moneda_recibida char(3) NOT NULL, importe_recibido numeric(14,2) NOT NULL, tipo_cambio numeric(12,4),
  fecha_real date NOT NULL, registrado_en timestamptz NOT NULL DEFAULT now(),
  anula_a int REFERENCES movimiento, motivo text,
  clave_solicitud uuid NOT NULL UNIQUE DEFAULT gen_random_uuid(), -- R15 (H13); en la aplicacion la genera el formulario, sin valor por defecto
  CHECK ((obligacion_id IS NULL) <> (deposito_id IS NULL)),
  CHECK (tipo = 'abono' OR (anula_a IS NOT NULL AND motivo IS NOT NULL)),
  CHECK (tipo = 'reversion' OR anula_a IS NULL));
CREATE UNIQUE INDEX r5_una_reversion ON movimiento (anula_a) WHERE tipo='reversion';
CREATE SEQUENCE comprobante_numero;
CREATE TABLE comprobante (
  id serial PRIMARY KEY, numero bigint NOT NULL UNIQUE DEFAULT nextval('comprobante_numero'),
  movimiento_id int NOT NULL UNIQUE REFERENCES movimiento, estado text NOT NULL DEFAULT 'vigente');

-- Derivaciones (seccion 5 del modelo)
CREATE VIEW v_obligacion AS
SELECT o.id, o.contrato_id, o.fecha_limite,
  o.importe_inicial + COALESCE((SELECT sum(importe_delta) FROM ajuste_obligacion a WHERE a.obligacion_id=o.id),0) AS importe_vigente,
  COALESCE((SELECT sum(m.importe_aplicado) FROM movimiento m WHERE m.obligacion_id=o.id AND m.tipo='abono'
     AND NOT EXISTS (SELECT 1 FROM movimiento r WHERE r.anula_a=m.id)),0) AS abonado,
  o.anulada_en
FROM obligacion o;
CREATE VIEW v_obligacion_estado AS
SELECT *, importe_vigente-abonado AS saldo,
  CASE WHEN anulada_en IS NOT NULL THEN 'anulada'
       WHEN importe_vigente-abonado = 0 THEN 'pagada'
       WHEN current_date > fecha_limite THEN 'vencida' ELSE 'pendiente' END AS estado
FROM v_obligacion;

-- R6 y R13: el saldo nunca queda negativo ni el importe bajo lo abonado (bloquea la fila).
CREATE FUNCTION chequeo_saldo() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE oid int; v numeric; ab numeric;
BEGIN
  IF TG_TABLE_NAME = 'ajuste_obligacion' THEN
    oid := NEW.obligacion_id;
  ELSE
    oid := COALESCE(NEW.obligacion_id, (SELECT obligacion_id FROM movimiento WHERE id = NEW.anula_a));
  END IF;
  IF oid IS NULL THEN RETURN NEW; END IF;
  PERFORM 1 FROM obligacion WHERE id = oid FOR UPDATE;
  SELECT importe_vigente, abonado INTO v, ab FROM v_obligacion WHERE id = oid;
  IF v < ab THEN RAISE EXCEPTION 'R6/R13: importe vigente % por debajo de lo abonado %', v, ab; END IF;
  RETURN NEW;
END $$;
CREATE CONSTRAINT TRIGGER t_saldo_mov AFTER INSERT ON movimiento DEFERRABLE INITIALLY IMMEDIATE FOR EACH ROW EXECUTE FUNCTION chequeo_saldo();
CREATE CONSTRAINT TRIGGER t_saldo_aj  AFTER INSERT ON ajuste_obligacion DEFERRABLE INITIALLY IMMEDIATE FOR EACH ROW EXECUTE FUNCTION chequeo_saldo();

-- R12: inmutabilidad
CREATE FUNCTION inmutable() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'R12: % es inmutable', TG_TABLE_NAME; END $$;
CREATE TRIGGER i_mov BEFORE UPDATE OR DELETE ON movimiento FOR EACH ROW EXECUTE FUNCTION inmutable();
CREATE TRIGGER i_aj  BEFORE UPDATE OR DELETE ON ajuste_obligacion FOR EACH ROW EXECUTE FUNCTION inmutable();

-- Arnes
CREATE TABLE resultado (prueba text, ok boolean, detalle text);
CREATE FUNCTION espera_error(p text, sentencia text) RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  BEGIN
    EXECUTE sentencia;
    INSERT INTO resultado VALUES (p, false, 'no fallo');
  EXCEPTION WHEN OTHERS THEN
    INSERT INTO resultado VALUES (p, true, left(SQLERRM, 70));
  END;
END $$;
CREATE FUNCTION espera_valor(p text, obtenido text, esperado text) RETURNS void LANGUAGE sql AS
$$ INSERT INTO resultado VALUES (p, obtenido IS NOT DISTINCT FROM esperado, 'obtenido=' || COALESCE(obtenido,'NULL') || ' esperado=' || esperado) $$;

-- Datos
INSERT INTO propiedad(descripcion) VALUES ('Casa A');
INSERT INTO contrato(propiedad_id,fecha_inicio,fecha_fin,moneda) VALUES (1,'2026-01-10','2026-12-31','CRC');
INSERT INTO condicion_contrato(contrato_id,monto_mensual,dia_vencimiento,dias_gracia,vigente_desde,tipo) VALUES (1,300000,10,7,'2026-01-10','inicial');
INSERT INTO obligacion(contrato_id,tipo,periodo_inicio,periodo_fin,fecha_vencimiento,fecha_limite,importe_inicial)
 VALUES (1,'regular','2026-01-10','2026-02-09','2026-01-10','2026-01-17',300000);
INSERT INTO deposito(contrato_id,importe_total) VALUES (1,300000);

-- R2 (RF-08)
SELECT espera_error('R2 solape de un dia compartido', $$INSERT INTO contrato(propiedad_id,fecha_inicio,fecha_fin,moneda) VALUES (1,'2026-12-31','2027-06-30','CRC')$$);
SELECT espera_error('R2 contrato abierto sobre uno existente', $$INSERT INTO contrato(propiedad_id,fecha_inicio,moneda) VALUES (1,'2026-06-01','CRC')$$);
INSERT INTO contrato(propiedad_id,fecha_inicio,fecha_fin,moneda) VALUES (1,'2027-01-01','2027-06-30','CRC');
INSERT INTO resultado VALUES ('R2 contiguo sin compartir dia es valido', true, 'insertado');
-- R1
SELECT espera_error('R1 periodo regular duplicado', $$INSERT INTO obligacion(contrato_id,tipo,periodo_inicio,periodo_fin,fecha_vencimiento,fecha_limite,importe_inicial) VALUES (1,'regular','2026-01-10','2026-02-09','2026-01-10','2026-01-17',1)$$);
INSERT INTO obligacion(contrato_id,tipo,fecha_vencimiento,fecha_limite,importe_inicial) VALUES (1,'apertura','2026-01-10','2026-01-17',50000);
SELECT espera_error('R1 segunda apertura', $$INSERT INTO obligacion(contrato_id,tipo,fecha_vencimiento,fecha_limite,importe_inicial) VALUES (1,'apertura','2026-01-10','2026-01-17',1)$$);
-- R3
SELECT espera_error('R3 monto cero', $$INSERT INTO condicion_contrato(contrato_id,monto_mensual,dia_vencimiento,dias_gracia,vigente_desde,tipo) VALUES (1,0,10,7,'2026-01-10','inicial')$$);
SELECT espera_error('R3 dia vencimiento 32', $$INSERT INTO condicion_contrato(contrato_id,monto_mensual,dia_vencimiento,dias_gracia,vigente_desde,tipo) VALUES (1,1,32,7,'2026-01-10','inicial')$$);
-- R4
SELECT espera_error('R4 movimiento sin destino', $$INSERT INTO movimiento(tipo,importe_aplicado,moneda_recibida,importe_recibido,fecha_real) VALUES ('abono',1,'CRC',1,'2026-01-11')$$);
SELECT espera_error('R4 movimiento con dos destinos', $$INSERT INTO movimiento(tipo,obligacion_id,deposito_id,importe_aplicado,moneda_recibida,importe_recibido,fecha_real) VALUES ('abono',1,1,1,'CRC',1,'2026-01-11')$$);
SELECT espera_error('R4 reversion sin motivo', $$INSERT INTO movimiento(tipo,obligacion_id,importe_aplicado,moneda_recibida,importe_recibido,fecha_real,anula_a) VALUES ('reversion',1,1,'CRC',1,'2026-01-11',(SELECT min(id) FROM movimiento))$$);

-- Abonos y derivaciones: obligacion 1 de 300000, abono 100000 y 50000
INSERT INTO movimiento(tipo,obligacion_id,importe_aplicado,moneda_recibida,importe_recibido,fecha_real) VALUES ('abono',1,100000,'CRC',100000,'2026-01-12');
INSERT INTO movimiento(tipo,obligacion_id,importe_aplicado,moneda_recibida,importe_recibido,fecha_real) VALUES ('abono',1,50000,'CRC',50000,'2026-01-13');
SELECT espera_valor('Saldo tras dos abonos', (SELECT saldo::text FROM v_obligacion_estado WHERE id=1), '150000.00');
SELECT espera_valor('Estado vencida (hoy > fecha limite 2026-01-17)', (SELECT estado FROM v_obligacion_estado WHERE id=1), 'vencida');
-- R6
SELECT espera_error('R6 sobrepago (abono de 200000 con saldo 150000)', $$INSERT INTO movimiento(tipo,obligacion_id,importe_aplicado,moneda_recibida,importe_recibido,fecha_real) VALUES ('abono',1,200000,'CRC',200000,'2026-01-14')$$);
-- Reversion
INSERT INTO movimiento(tipo,obligacion_id,importe_aplicado,moneda_recibida,importe_recibido,fecha_real,anula_a,motivo) VALUES ('reversion',1,50000,'CRC',50000,'2026-01-14',(SELECT id FROM movimiento WHERE tipo='abono' AND importe_aplicado=50000),'error de digitacion');
SELECT espera_valor('Saldo tras anular el abono de 50000', (SELECT saldo::text FROM v_obligacion_estado WHERE id=1), '200000.00');
SELECT espera_error('R5 segunda reversion del mismo abono', $$INSERT INTO movimiento(tipo,obligacion_id,importe_aplicado,moneda_recibida,importe_recibido,fecha_real,anula_a,motivo) VALUES ('reversion',1,50000,'CRC',50000,'2026-01-14',(SELECT id FROM movimiento WHERE tipo='abono' AND importe_aplicado=50000),'otra')$$);
-- R12
SELECT espera_error('R12 UPDATE de movimiento', $$UPDATE movimiento SET importe_aplicado=1$$);
SELECT espera_error('R12 DELETE de movimiento', $$DELETE FROM movimiento WHERE tipo='abono'$$);
-- R7
INSERT INTO comprobante(movimiento_id) SELECT id FROM movimiento WHERE importe_aplicado=100000;
INSERT INTO comprobante(movimiento_id) SELECT id FROM movimiento WHERE tipo='abono' AND importe_aplicado=50000;
SELECT espera_valor('R7 numeros consecutivos', (SELECT string_agg(numero::text, ',' ORDER BY numero) FROM comprobante), '1,2');
SELECT espera_error('R7 dos comprobantes del mismo movimiento', $$INSERT INTO comprobante(movimiento_id) SELECT id FROM movimiento WHERE importe_aplicado=100000$$);
-- Ajustes (H9, R13)
SELECT espera_error('R13 ajuste de cero', $$INSERT INTO ajuste_obligacion(obligacion_id,tipo,importe_delta,motivo) VALUES (1,'reajuste',0,NULL)$$);
SELECT espera_error('R13 correccion sin motivo', $$INSERT INTO ajuste_obligacion(obligacion_id,tipo,importe_delta) VALUES (1,'correccion',-10)$$);
SELECT espera_error('R13 correccion que deja el importe bajo lo abonado (100000 abonado, delta -250000)', $$INSERT INTO ajuste_obligacion(obligacion_id,tipo,importe_delta,motivo) VALUES (1,'correccion',-250000,'error')$$);
INSERT INTO ajuste_obligacion(obligacion_id,tipo,importe_delta,motivo) VALUES (1,'correccion',-100000,'monto mal digitado');
SELECT espera_valor('Importe vigente tras correccion valida', (SELECT importe_vigente::text FROM v_obligacion_estado WHERE id=1), '200000.00');
SELECT espera_valor('Saldo tras correccion valida', (SELECT saldo::text FROM v_obligacion_estado WHERE id=1), '100000.00');
SELECT espera_error('R12 UPDATE de ajuste', $$UPDATE ajuste_obligacion SET importe_delta=-1$$);
-- Prorrateo (RN-12): 300000 x 11 / 31 = 106451,6129 -> 106452 (CRC, unidad entera, empate hacia arriba)
SELECT espera_valor('RN-12 prorrateo fin 20-ene en periodo 10-ene a 9-feb (11 dias de 31)', round(300000::numeric * 11 / 31)::text, '106452');
SELECT espera_valor('RN-12 dias del periodo 10-ene a 9-feb inclusive', ((date '2026-02-09' - date '2026-01-10') + 1)::text, '31');
SELECT espera_valor('RN-12 dias cobrables 10 a 20 ene inclusive', ((date '2026-01-20' - date '2026-01-10') + 1)::text, '11');
-- Empate hacia arriba (H5)
SELECT espera_valor('H5 empate USD 1.005 a 2 decimales', round(1.005::numeric, 2)::text, '1.01');
SELECT espera_valor('H5 empate CRC 0.5 a entero', round(0.5::numeric)::text, '1');


-- R15 / H13: el mismo envio repetido no duplica el abono
INSERT INTO movimiento(tipo,obligacion_id,importe_aplicado,moneda_recibida,importe_recibido,fecha_real,clave_solicitud) VALUES ('abono',1,1000,'CRC',1000,'2026-01-15','11111111-1111-4111-8111-111111111111');
SELECT espera_error('R15 mismo envio repetido (misma clave_solicitud)', $$INSERT INTO movimiento(tipo,obligacion_id,importe_aplicado,moneda_recibida,importe_recibido,fecha_real,clave_solicitud) VALUES ('abono',1,1000,'CRC',1000,'2026-01-15','11111111-1111-4111-8111-111111111111')$$);
SELECT espera_valor('R15 un solo abono de 1000 tras el reintento', (SELECT count(*)::text FROM movimiento WHERE importe_aplicado=1000), '1');

-- Hallazgo H11: una secuencia deja huecos al revertir. R7 exige numeracion consecutiva.
\echo '=== H11: huecos con secuencia ==='
SELECT nextval('comprobante_numero') AS numero_consumido_por_el_intento_fallido_anterior;
SELECT max(numero) AS ultimo_comprobante_real FROM comprobante;
-- Alternativa: contador en tabla, con bloqueo de fila, dentro de la misma transaccion.
CREATE TABLE contador_comprobante (id int PRIMARY KEY CHECK (id = 1), ultimo bigint NOT NULL);
INSERT INTO contador_comprobante VALUES (1, 0);
CREATE FUNCTION siguiente_comprobante() RETURNS bigint LANGUAGE sql AS
$$ UPDATE contador_comprobante SET ultimo = ultimo + 1 WHERE id = 1 RETURNING ultimo $$;
BEGIN; SELECT siguiente_comprobante() AS dentro_de_transaccion_que_se_revierte; ROLLBACK;
SELECT siguiente_comprobante() AS tras_rollback_sigue_en_1;

\echo '=== RESULTADOS ==='
SELECT CASE WHEN ok THEN 'OK   ' ELSE 'FALLA' END AS r, prueba, detalle FROM resultado ORDER BY ok, prueba;
SELECT count(*) FILTER (WHERE ok) AS ok, count(*) FILTER (WHERE NOT ok) AS fallas FROM resultado;
