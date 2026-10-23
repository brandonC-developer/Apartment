-- Prueba desechable del modelo MDD-SGA-001 v0.6 en PostgreSQL (sin zona temporal).
-- NO es el esquema de produccion ni fija ningun ADR: comprueba que R22, R23, R25, R26 y R27
-- (y la derivacion de RF-51) se pueden expresar y se cumplen. Los CHECK de R11 y R27 y la funcion
-- que aplica R26 son propuestas del asistente para la prueba.
-- La concurrencia (H18, R25 y R26) la hace ejecutar_prueba_v0.6.ps1 con dos sesiones reales.
DROP DATABASE IF EXISTS sga_prueba_v06;
CREATE DATABASE sga_prueba_v06;
\c sga_prueba_v06
CREATE EXTENSION btree_gist;

-- Entidades de apoyo (version minima; ids como bigint, ADR-028)
CREATE TABLE inquilino (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, nombre_completo text);
CREATE TABLE consentimiento (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, inquilino_id bigint NOT NULL REFERENCES inquilino,
  otorgado_en timestamptz NOT NULL DEFAULT now(), revocado_en timestamptz);
CREATE TABLE propiedad (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, alias text NOT NULL UNIQUE);
CREATE TABLE contrato (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  inquilino_id bigint NOT NULL REFERENCES inquilino, propiedad_id bigint NOT NULL REFERENCES propiedad,
  fecha_inicio date NOT NULL, fecha_fin date, anulado_en timestamptz,
  CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio),
  EXCLUDE USING gist (propiedad_id WITH =, daterange(fecha_inicio, fecha_fin, '[]') WITH &&) WHERE (anulado_en IS NULL));

-- Entidades del modelo v0.6
CREATE TABLE documento_identidad (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, inquilino_id bigint NOT NULL REFERENCES inquilino,
  cara text NOT NULL CHECK (cara IN ('frente','reverso')),
  referencia_archivo text NOT NULL,
  tipo_real_archivo text NOT NULL,
  tamano_bytes bigint NOT NULL,
  creado_en timestamptz NOT NULL DEFAULT now(), eliminado_en timestamptz,
  CONSTRAINT r11_nombre_aleatorio CHECK (referencia_archivo ~ '^[0-9a-f]{32}$'),
  CONSTRAINT r27_tipo CHECK (tipo_real_archivo IN ('image/jpeg','image/png')),
  CONSTRAINT r27_tamano CHECK (tamano_bytes BETWEEN 1 AND 5242880));
CREATE UNIQUE INDEX r25_una_activa_por_cara ON documento_identidad (inquilino_id, cara) WHERE eliminado_en IS NULL;

CREATE TABLE documento_contrato (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, contrato_id bigint NOT NULL REFERENCES contrato,
  orden int NOT NULL CHECK (orden >= 1),
  referencia_archivo text NOT NULL,
  tipo_real_archivo text NOT NULL,
  tamano_bytes bigint NOT NULL,
  creado_en timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT r11_nombre_aleatorio CHECK (referencia_archivo ~ '^[0-9a-f]{32}$'),
  CONSTRAINT r27_tipo CHECK (tipo_real_archivo IN ('image/jpeg','image/png')),
  CONSTRAINT r27_tamano CHECK (tamano_bytes BETWEEN 1 AND 5242880),
  CONSTRAINT r22_orden_unico UNIQUE (contrato_id, orden));

CREATE TABLE acceso_documento (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  documento_id bigint REFERENCES documento_identidad, documento_contrato_id bigint REFERENCES documento_contrato,
  actor text NOT NULL, accion text NOT NULL CHECK (accion IN ('consulta','descarga')),
  ocurrido_en timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT r23_exactamente_uno CHECK ((documento_id IS NULL) <> (documento_contrato_id IS NULL)));

-- R12: ACCESO_DOCUMENTO no admite UPDATE ni DELETE
CREATE FUNCTION inmutable() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'fila inmutable'; END $$;
CREATE TRIGGER i_acceso BEFORE UPDATE OR DELETE ON acceso_documento FOR EACH ROW EXECUTE FUNCTION inmutable();

-- Transaccion "agregar o reemplazar la fotografia del documento": consentimiento -> marcar la activa -> insertar
CREATE FUNCTION agregar_o_reemplazar_cedula(inq bigint, c text, ref text, tipo text, tam bigint) RETURNS bigint LANGUAGE plpgsql AS $$
DECLARE nuevo bigint;
BEGIN
  IF NOT EXISTS (SELECT 1 FROM consentimiento WHERE inquilino_id = inq AND revocado_en IS NULL) THEN
    RAISE EXCEPTION 'sin consentimiento vigente';
  END IF;
  UPDATE documento_identidad SET eliminado_en = now() WHERE inquilino_id = inq AND cara = c AND eliminado_en IS NULL;
  INSERT INTO documento_identidad(inquilino_id, cara, referencia_archivo, tipo_real_archivo, tamano_bytes)
    VALUES (inq, c, ref, tipo, tam) RETURNING id INTO nuevo;
  RETURN nuevo;
END $$;

-- R26: crear contrato solo si el inquilino tiene un frente activo (la aplica el servicio, no una restriccion de tabla)
CREATE FUNCTION crear_contrato(inq bigint, prop bigint, ini date, fin date, anulado timestamptz DEFAULT NULL) RETURNS bigint LANGUAGE plpgsql AS $$
DECLARE nuevo bigint;
BEGIN
  IF NOT EXISTS (SELECT 1 FROM documento_identidad WHERE inquilino_id = inq AND cara = 'frente' AND eliminado_en IS NULL) THEN
    RAISE EXCEPTION 'R26: el inquilino no tiene el frente de la fotografia cargado';
  END IF;
  INSERT INTO contrato(inquilino_id, propiedad_id, fecha_inicio, fecha_fin, anulado_en) VALUES (inq, prop, ini, fin, anulado) RETURNING id INTO nuevo;
  RETURN nuevo;
END $$;

-- H18: agregar la fotografia del contrato bloqueando primero la fila del contrato
CREATE FUNCTION agregar_fotografia_contrato(con bigint, ref text, tipo text, tam bigint) RETURNS bigint LANGUAGE plpgsql AS $$
DECLARE nuevo bigint; sig int;
BEGIN
  PERFORM 1 FROM contrato WHERE id = con FOR UPDATE;
  SELECT COALESCE(max(orden), 0) + 1 INTO sig FROM documento_contrato WHERE contrato_id = con;
  INSERT INTO documento_contrato(contrato_id, orden, referencia_archivo, tipo_real_archivo, tamano_bytes)
    VALUES (con, sig, ref, tipo, tam) RETURNING id INTO nuevo;
  RETURN nuevo;
END $$;
-- Misma operacion sin el bloqueo (para mostrar de nuevo el hallazgo H18)
CREATE FUNCTION agregar_fotografia_contrato_sin_bloqueo(con bigint, ref text, tipo text, tam bigint) RETURNS bigint LANGUAGE plpgsql AS $$
DECLARE nuevo bigint; sig int;
BEGIN
  SELECT COALESCE(max(orden), 0) + 1 INTO sig FROM documento_contrato WHERE contrato_id = con;
  INSERT INTO documento_contrato(contrato_id, orden, referencia_archivo, tipo_real_archivo, tamano_bytes)
    VALUES (con, sig, ref, tipo, tam) RETURNING id INTO nuevo;
  RETURN nuevo;
END $$;

-- Derivacion de RF-51: inquilino del contrato vigente de una propiedad
CREATE FUNCTION inquilinos_vigentes(prop bigint) RETURNS SETOF bigint LANGUAGE sql AS $$
  SELECT inquilino_id FROM contrato
   WHERE propiedad_id = prop AND anulado_en IS NULL AND fecha_inicio <= current_date
     AND (fecha_fin IS NULL OR fecha_fin >= current_date) $$;
-- Derivado de la seccion 5: inquilino con frente cargado
CREATE FUNCTION con_frente(inq bigint) RETURNS boolean LANGUAGE sql AS $$
  SELECT EXISTS (SELECT 1 FROM documento_identidad WHERE inquilino_id = inq AND cara = 'frente' AND eliminado_en IS NULL) $$;

-- Arnes
CREATE TABLE resultado (prueba text, ok boolean, detalle text);
CREATE FUNCTION espera_error(p text, sentencia text) RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  BEGIN EXECUTE sentencia; INSERT INTO resultado VALUES (p, false, 'no fallo');
  EXCEPTION WHEN OTHERS THEN INSERT INTO resultado VALUES (p, true, left(SQLERRM, 70)); END;
END $$;
CREATE FUNCTION espera_valor(p text, obtenido text, esperado text) RETURNS void LANGUAGE sql AS
$$ INSERT INTO resultado VALUES (p, obtenido IS NOT DISTINCT FROM esperado, 'obtenido=' || COALESCE(obtenido,'NULL') || ' esperado=' || esperado) $$;

-- Datos: 1 Ana, 2 Beto, 3 Carla, 4 Dani (sin consentimiento), 5 Eva (con consentimiento, sin fotografias)
INSERT INTO inquilino(nombre_completo) VALUES ('Ana'), ('Beto'), ('Carla'), ('Dani'), ('Eva');
INSERT INTO consentimiento(inquilino_id) VALUES (1), (2), (3), (5);
INSERT INTO propiedad(alias) VALUES ('Casa A'), ('Casa B');

-- R26: el inquilino recien registrado (sin fotografias) no admite contrato
SELECT espera_valor('R26 inquilino recien guardado no tiene frente', con_frente(5)::text, 'false');
SELECT espera_error('R26 contrato con un inquilino sin frente', $$SELECT crear_contrato(5, 2, current_date, NULL)$$);
SELECT espera_valor('R26 el rechazo no deja contrato', (SELECT count(*)::text FROM contrato), '0');
SELECT espera_error('consentimiento: agregar fotografia sin consentimiento vigente', $$SELECT agregar_o_reemplazar_cedula(4, 'frente', repeat('1',32), 'image/jpeg', 1000)$$);
SELECT agregar_o_reemplazar_cedula(5, 'reverso', repeat('2',32), 'image/png', 1000);
SELECT espera_valor('R26 solo con el reverso sigue sin frente', con_frente(5)::text, 'false');
SELECT espera_error('R26 contrato con un inquilino que solo tiene el reverso', $$SELECT crear_contrato(5, 2, current_date, NULL)$$);

-- Subir los frentes de Ana, Beto y Carla y crear sus contratos (Casa A: anulado solapado, vigente y futuro)
SELECT agregar_o_reemplazar_cedula(1, 'frente', repeat('a',32), 'image/jpeg', 1500000);
SELECT agregar_o_reemplazar_cedula(2, 'frente', repeat('b',32), 'image/jpeg', 1500000);
SELECT agregar_o_reemplazar_cedula(3, 'frente', repeat('c',32), 'image/jpeg', 1500000);
SELECT crear_contrato(1, 1, current_date - 100, current_date + 100, now());
SELECT crear_contrato(2, 1, current_date - 100, current_date + 100);
SELECT crear_contrato(3, 1, current_date + 101, NULL);
SELECT espera_valor('R26 con frente se crea el contrato (3 contratos)', (SELECT count(*)::text FROM contrato), '3');
SELECT espera_error('R2 contrato solapado sigue rechazado', $$SELECT crear_contrato(1, 1, current_date, current_date + 10)$$);

-- RF-51: derivacion del inquilino al que se agrega la cedula
SELECT espera_valor('RF-51 un solo inquilino vigente (ignora anulado y futuro)', (SELECT count(*)::text FROM inquilinos_vigentes(1)), '1');
SELECT espera_valor('RF-51 el vigente es Beto', (SELECT string_agg(i.nombre_completo, ',') FROM inquilinos_vigentes(1) v JOIN inquilino i ON i.id = v), 'Beto');
SELECT espera_valor('RF-51 propiedad sin contrato no ofrece la accion', (SELECT count(*)::text FROM inquilinos_vigentes(2)), '0');

-- R27: tope de 5 MiB = 5 242 880 bytes y tipo real
SELECT agregar_o_reemplazar_cedula(5, 'frente', repeat('3',32), 'image/jpeg', 5242880);
INSERT INTO resultado VALUES ('R27 5 242 880 bytes se acepta', true, 'frente de Eva');
SELECT espera_error('R27 5 242 881 bytes se rechaza', $$SELECT agregar_o_reemplazar_cedula(5, 'frente', repeat('4',32), 'image/jpeg', 5242881)$$);
SELECT espera_error('R27 cero bytes se rechaza', $$INSERT INTO documento_identidad(inquilino_id,cara,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (3,'reverso',repeat('4',32),'image/jpeg',0)$$);
SELECT espera_error('R27 PDF se rechaza', $$INSERT INTO documento_identidad(inquilino_id,cara,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (3,'reverso',repeat('4',32),'application/pdf',1000)$$);
SELECT espera_error('R27 5 242 881 bytes se rechaza tambien en la fotografia del contrato', $$SELECT agregar_fotografia_contrato(2, repeat('5',32), 'image/jpeg', 5242881)$$);
-- El rechazo del reemplazo deshace todo: Eva conserva su frente anterior (atomicidad del reemplazo)
SELECT espera_valor('R27/R25 el reemplazo rechazado deja el frente anterior activo', (SELECT referencia_archivo FROM documento_identidad WHERE inquilino_id=5 AND cara='frente' AND eliminado_en IS NULL), repeat('3',32));
SELECT espera_valor('R26 Eva ya tiene frente', con_frente(5)::text, 'true');
SELECT crear_contrato(5, 2, current_date, NULL);
INSERT INTO resultado VALUES ('R26 contrato de Eva en Casa B tras cargar el frente', true, 'creado');

-- R11 (propuesta de CHECK)
SELECT espera_error('R11 referencia con una URL', $$INSERT INTO documento_identidad(inquilino_id,cara,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (3,'reverso','https://sitio.com/cedula.jpg','image/jpeg',1)$$);
SELECT espera_error('R11 referencia con una ruta', $$INSERT INTO documento_contrato(contrato_id,orden,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (2,1,'../etc/passwd','image/jpeg',1)$$);

-- R25: una cedula activa por cara y reemplazo
SELECT espera_error('R25 segundo frente activo sin reemplazo (INSERT directo)', $$INSERT INTO documento_identidad(inquilino_id,cara,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (2,'frente',repeat('6',32),'image/jpeg',1000)$$);
SELECT agregar_o_reemplazar_cedula(2, 'frente', repeat('d',32), 'image/jpeg', 1400000);
INSERT INTO resultado VALUES ('R25 reemplazo: marca la anterior y acepta el nuevo frente', true, 'reemplazado');
SELECT espera_valor('R25 queda un solo frente activo', (SELECT count(*)::text FROM documento_identidad WHERE inquilino_id=2 AND cara='frente' AND eliminado_en IS NULL), '1');
SELECT espera_valor('R25 la anterior queda marcada, no borrada', (SELECT count(*)::text FROM documento_identidad WHERE inquilino_id=2 AND cara='frente' AND eliminado_en IS NOT NULL), '1');
SELECT espera_valor('R26 tras reemplazar el frente de Beto sigue con frente', con_frente(2)::text, 'true');
SELECT agregar_o_reemplazar_cedula(2, 'reverso', repeat('e',32), 'image/png', 2000000);
INSERT INTO resultado VALUES ('R25 el reverso es otra cara y se acepta', true, 'agregado');

-- R22: fotografias del contrato (con el bloqueo de H18)
SELECT agregar_fotografia_contrato(2, repeat('1',32), 'image/jpeg', 1800000);
SELECT agregar_fotografia_contrato(2, repeat('2',32), 'image/jpeg', 1700000);
SELECT espera_valor('R22 el orden de las fotografias es 1,2', (SELECT string_agg(orden::text, ',' ORDER BY orden) FROM documento_contrato WHERE contrato_id=2), '1,2');
SELECT espera_error('R22 orden repetido en el mismo contrato', $$INSERT INTO documento_contrato(contrato_id,orden,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (2,1,repeat('8',32),'image/jpeg',1)$$);
SELECT espera_error('R22 orden cero', $$INSERT INTO documento_contrato(contrato_id,orden,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (2,0,repeat('8',32),'image/jpeg',1)$$);
INSERT INTO documento_contrato(contrato_id,orden,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (3,1,repeat('7',32),'image/png',5);
INSERT INTO resultado VALUES ('R22 el mismo orden en otro contrato es valido', true, 'insertado');
SELECT espera_error('fotografia de un contrato inexistente', $$INSERT INTO documento_contrato(contrato_id,orden,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (999,1,repeat('7',32),'image/png',5)$$);

-- R23 y R12 sobre ACCESO_DOCUMENTO
INSERT INTO acceso_documento(documento_id,actor,accion) VALUES ((SELECT min(id) FROM documento_identidad),'admin','consulta');
INSERT INTO acceso_documento(documento_contrato_id,actor,accion) VALUES ((SELECT min(id) FROM documento_contrato),'admin','descarga');
INSERT INTO resultado VALUES ('R23 acceso a cedula y a contrato por separado', true, 'insertados');
SELECT espera_error('R23 acceso sin ningun documento', $$INSERT INTO acceso_documento(actor,accion) VALUES ('admin','consulta')$$);
SELECT espera_error('R23 acceso con los dos documentos', $$INSERT INTO acceso_documento(documento_id,documento_contrato_id,actor,accion) VALUES (1,1,'admin','consulta')$$);
SELECT espera_error('R12 UPDATE de acceso_documento', $$UPDATE acceso_documento SET actor='otro'$$);
SELECT espera_error('R12 DELETE de acceso_documento', $$DELETE FROM acceso_documento$$);

\echo ''
\echo '== Resultado de las comprobaciones de una sola sesion =='
SELECT CASE WHEN ok THEN ' OK   ' ELSE ' FALLA' END AS r, rpad(prueba, 95) AS prueba, detalle FROM resultado ORDER BY prueba;
SELECT count(*) FILTER (WHERE ok) AS ok, count(*) FILTER (WHERE NOT ok) AS fallas FROM resultado;
