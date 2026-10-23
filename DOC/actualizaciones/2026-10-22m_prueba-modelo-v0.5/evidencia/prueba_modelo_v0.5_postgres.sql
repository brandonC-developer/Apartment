-- Prueba desechable de las entidades nuevas del modelo MDD-SGA-001 v0.5 en PostgreSQL.
-- NO es el esquema de produccion ni fija ningun ADR: solo comprueba que R11, R22, R23, R24 y R25
-- y las derivaciones de RF-51 se pueden expresar y se cumplen. Las restricciones adicionales
-- (CHECK de R11, destino/cara, expira_en) son propuestas del asistente para la prueba.
-- La prueba de concurrencia de R24 la hace ejecutar_prueba_v0.5.ps1 con dos sesiones reales.
DROP DATABASE IF EXISTS sga_prueba_v05;
CREATE DATABASE sga_prueba_v05;
\c sga_prueba_v05
CREATE EXTENSION btree_gist;

-- Entidades de apoyo (version minima; ids como bigint, ADR-028)
CREATE TABLE inquilino (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, nombre_completo text);
CREATE TABLE propiedad (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, alias text NOT NULL UNIQUE);
CREATE TABLE contrato (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  inquilino_id bigint NOT NULL REFERENCES inquilino, propiedad_id bigint NOT NULL REFERENCES propiedad,
  fecha_inicio date NOT NULL, fecha_fin date, anulado_en timestamptz,
  CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio),
  EXCLUDE USING gist (propiedad_id WITH =, daterange(fecha_inicio, fecha_fin, '[]') WITH &&) WHERE (anulado_en IS NULL));

-- Entidades nuevas o cambiadas en la v0.5
CREATE TABLE documento_identidad (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, inquilino_id bigint NOT NULL REFERENCES inquilino,
  cara text NOT NULL CHECK (cara IN ('frente','reverso')),
  referencia_archivo text NOT NULL,
  tipo_real_archivo text NOT NULL CHECK (tipo_real_archivo IN ('image/jpeg','image/png')),
  tamano_bytes bigint NOT NULL CHECK (tamano_bytes > 0),
  creado_en timestamptz NOT NULL DEFAULT now(), eliminado_en timestamptz,
  -- R11 (propuesta de CHECK): nombre aleatorio de 32 hex, nunca una URL ni una ruta
  CHECK (referencia_archivo ~ '^[0-9a-f]{32}$'));
CREATE UNIQUE INDEX r25_una_activa_por_cara ON documento_identidad (inquilino_id, cara) WHERE eliminado_en IS NULL;

CREATE TABLE documento_contrato (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, contrato_id bigint NOT NULL REFERENCES contrato,
  orden int NOT NULL CHECK (orden >= 1),
  referencia_archivo text NOT NULL CHECK (referencia_archivo ~ '^[0-9a-f]{32}$'),
  tipo_real_archivo text NOT NULL CHECK (tipo_real_archivo IN ('image/jpeg','image/png')),
  tamano_bytes bigint NOT NULL CHECK (tamano_bytes > 0),
  creado_en timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT r22_orden_unico UNIQUE (contrato_id, orden));

CREATE TABLE acceso_documento (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  documento_id bigint REFERENCES documento_identidad, documento_contrato_id bigint REFERENCES documento_contrato,
  actor text NOT NULL, accion text NOT NULL CHECK (accion IN ('consulta','descarga')),
  ocurrido_en timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT r23_exactamente_uno CHECK ((documento_id IS NULL) <> (documento_contrato_id IS NULL)));

CREATE TABLE archivo_temporal (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  identificador_hash text NOT NULL UNIQUE,
  destino text NOT NULL CHECK (destino IN ('documento_identidad','documento_contrato')),
  cara text CHECK (cara IN ('frente','reverso')),
  referencia_archivo text NOT NULL CHECK (referencia_archivo ~ '^[0-9a-f]{32}$'),
  tipo_real_archivo text NOT NULL CHECK (tipo_real_archivo IN ('image/jpeg','image/png')),
  tamano_bytes bigint NOT NULL CHECK (tamano_bytes > 0),
  sesion_hash text,
  creado_en timestamptz NOT NULL DEFAULT now(),
  expira_en timestamptz NOT NULL,
  usado_en timestamptz, eliminado_en timestamptz,
  CHECK ((destino = 'documento_identidad') = (cara IS NOT NULL)),          -- cara solo para la cedula
  CHECK (expira_en = creado_en + interval '24 hours'));                    -- 24 horas (decision del solicitante)

-- R12: ACCESO_DOCUMENTO no admite UPDATE ni DELETE
CREATE FUNCTION inmutable() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'fila inmutable'; END $$;
CREATE TRIGGER i_acceso BEFORE UPDATE OR DELETE ON acceso_documento FOR EACH ROW EXECUTE FUNCTION inmutable();

-- R24: consumir el identificador una sola vez (bloquea la fila; si otra transaccion lo usa primero, falla)
CREATE FUNCTION consumir_archivo_temporal(h text) RETURNS archivo_temporal LANGUAGE plpgsql AS $$
DECLARE r archivo_temporal;
BEGIN
  SELECT * INTO r FROM archivo_temporal
   WHERE identificador_hash = h AND usado_en IS NULL AND eliminado_en IS NULL AND expira_en > now() FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'identificador no valido, usado o vencido'; END IF;
  UPDATE archivo_temporal SET usado_en = now() WHERE id = r.id;
  RETURN r;
END $$;
-- Asociar a la cedula de un inquilino (una sola transaccion: consumir + insertar)
CREATE FUNCTION asociar_cedula(h text, inq bigint, ref_definitiva text) RETURNS bigint LANGUAGE plpgsql AS $$
DECLARE r archivo_temporal; nuevo bigint;
BEGIN
  r := consumir_archivo_temporal(h);
  IF r.destino <> 'documento_identidad' THEN RAISE EXCEPTION 'el archivo temporal no es de una cedula'; END IF;
  INSERT INTO documento_identidad(inquilino_id, cara, referencia_archivo, tipo_real_archivo, tamano_bytes)
    VALUES (inq, r.cara, ref_definitiva, r.tipo_real_archivo, r.tamano_bytes) RETURNING id INTO nuevo;
  RETURN nuevo;
END $$;
CREATE FUNCTION asociar_fotografia_contrato(h text, con bigint, ref_definitiva text) RETURNS bigint LANGUAGE plpgsql AS $$
DECLARE r archivo_temporal; nuevo bigint; sig int;
BEGIN
  r := consumir_archivo_temporal(h);
  IF r.destino <> 'documento_contrato' THEN RAISE EXCEPTION 'el archivo temporal no es de un contrato'; END IF;
  SELECT COALESCE(max(orden), 0) + 1 INTO sig FROM documento_contrato WHERE contrato_id = con;
  INSERT INTO documento_contrato(contrato_id, orden, referencia_archivo, tipo_real_archivo, tamano_bytes)
    VALUES (con, sig, ref_definitiva, r.tipo_real_archivo, r.tamano_bytes) RETURNING id INTO nuevo;
  RETURN nuevo;
END $$;
-- Proceso de limpieza: lo vencido y no asociado
CREATE FUNCTION limpiar_temporales() RETURNS int LANGUAGE sql AS $$
  WITH x AS (UPDATE archivo_temporal SET eliminado_en = now()
             WHERE usado_en IS NULL AND eliminado_en IS NULL AND expira_en <= now() RETURNING 1)
  SELECT count(*)::int FROM x $$;
-- Derivacion de RF-51: inquilino del contrato vigente de una propiedad
CREATE FUNCTION inquilinos_vigentes(prop bigint) RETURNS SETOF bigint LANGUAGE sql AS $$
  SELECT inquilino_id FROM contrato
   WHERE propiedad_id = prop AND anulado_en IS NULL AND fecha_inicio <= current_date
     AND (fecha_fin IS NULL OR fecha_fin >= current_date) $$;

-- Arnes
CREATE TABLE resultado (prueba text, ok boolean, detalle text);
CREATE FUNCTION espera_error(p text, sentencia text) RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  BEGIN EXECUTE sentencia; INSERT INTO resultado VALUES (p, false, 'no fallo');
  EXCEPTION WHEN OTHERS THEN INSERT INTO resultado VALUES (p, true, left(SQLERRM, 70)); END;
END $$;
CREATE FUNCTION espera_valor(p text, obtenido text, esperado text) RETURNS void LANGUAGE sql AS
$$ INSERT INTO resultado VALUES (p, obtenido IS NOT DISTINCT FROM esperado, 'obtenido=' || COALESCE(obtenido,'NULL') || ' esperado=' || esperado) $$;

-- Datos
INSERT INTO inquilino(nombre_completo) VALUES ('Ana'), ('Beto'), ('Carla');
INSERT INTO propiedad(alias) VALUES ('Casa A'), ('Casa B');
-- Casa A: un contrato anulado que se solapa con el vigente, el vigente (Beto) y uno futuro (Carla)
INSERT INTO contrato(inquilino_id, propiedad_id, fecha_inicio, fecha_fin, anulado_en)
  VALUES (1, 1, current_date - 100, current_date + 100, now());
INSERT INTO contrato(inquilino_id, propiedad_id, fecha_inicio, fecha_fin) VALUES (2, 1, current_date - 100, current_date + 100);
INSERT INTO contrato(inquilino_id, propiedad_id, fecha_inicio, fecha_fin) VALUES (3, 1, current_date + 101, NULL);
INSERT INTO resultado VALUES ('R2 anulado no cuenta; vigente y futuro contiguos', true, '3 contratos insertados');

-- RF-51: derivacion del inquilino al que se agrega la cedula
SELECT espera_valor('RF-51 un solo inquilino vigente (ignora anulado y futuro)', (SELECT count(*)::text FROM inquilinos_vigentes(1)), '1');
SELECT espera_valor('RF-51 el vigente es Beto', (SELECT string_agg(i.nombre_completo, ',') FROM inquilinos_vigentes(1) v JOIN inquilino i ON i.id = v), 'Beto');
SELECT espera_valor('RF-51 propiedad sin contrato no ofrece la accion', (SELECT count(*)::text FROM inquilinos_vigentes(2)), '0');

-- Archivos temporales de prueba
INSERT INTO archivo_temporal(identificador_hash,destino,cara,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en)
 VALUES ('h-frente','documento_identidad','frente',repeat('a',32),'image/jpeg',1500000,now(),now()+interval '24 hours');
INSERT INTO archivo_temporal(identificador_hash,destino,cara,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en)
 VALUES ('h-frente2','documento_identidad','frente',repeat('b',32),'image/jpeg',1400000,now(),now()+interval '24 hours');
INSERT INTO archivo_temporal(identificador_hash,destino,cara,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en)
 VALUES ('h-reverso','documento_identidad','reverso',repeat('c',32),'image/png',2000000,now(),now()+interval '24 hours');
INSERT INTO archivo_temporal(identificador_hash,destino,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en)
 VALUES ('h-contrato1','documento_contrato',repeat('d',32),'image/jpeg',1800000,now(),now()+interval '24 hours');
INSERT INTO archivo_temporal(identificador_hash,destino,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en)
 VALUES ('h-contrato2','documento_contrato',repeat('e',32),'image/jpeg',1700000,now(),now()+interval '24 hours');
INSERT INTO archivo_temporal(identificador_hash,destino,cara,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en)
 VALUES ('h-vencido','documento_identidad','frente',repeat('f',32),'image/jpeg',1000000,now()-interval '25 hours',now()-interval '1 hour');
INSERT INTO archivo_temporal(identificador_hash,destino,cara,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en)
 VALUES ('h-concurrente','documento_identidad','reverso',repeat('9',32),'image/jpeg',1000000,now(),now()+interval '24 hours');
INSERT INTO resultado VALUES ('archivo_temporal acepta filas validas (7)', true, 'insertadas');

-- Restricciones propias de archivo_temporal
SELECT espera_error('hash del identificador duplicado', $$INSERT INTO archivo_temporal(identificador_hash,destino,cara,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en) VALUES ('h-frente','documento_identidad','frente',repeat('1',32),'image/jpeg',1,now(),now()+interval '24 hours')$$);
SELECT espera_error('expira_en distinto de creado_en + 24 horas', $$INSERT INTO archivo_temporal(identificador_hash,destino,cara,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en) VALUES ('h-x1','documento_identidad','frente',repeat('1',32),'image/jpeg',1,now(),now()+interval '48 hours')$$);
SELECT espera_error('contrato con cara informada', $$INSERT INTO archivo_temporal(identificador_hash,destino,cara,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en) VALUES ('h-x2','documento_contrato','frente',repeat('1',32),'image/jpeg',1,now(),now()+interval '24 hours')$$);
SELECT espera_error('cedula sin cara', $$INSERT INTO archivo_temporal(identificador_hash,destino,referencia_archivo,tipo_real_archivo,tamano_bytes,creado_en,expira_en) VALUES ('h-x3','documento_identidad',repeat('1',32),'image/jpeg',1,now(),now()+interval '24 hours')$$);
-- R11 (propuesta de CHECK)
SELECT espera_error('R11 referencia con una URL', $$INSERT INTO documento_identidad(inquilino_id,cara,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (3,'frente','https://sitio.com/cedula.jpg','image/jpeg',1)$$);
SELECT espera_error('R11 referencia con una ruta', $$INSERT INTO documento_contrato(contrato_id,orden,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (2,1,'../etc/passwd','image/jpeg',1)$$);
SELECT espera_error('tipo real distinto de JPEG y PNG', $$INSERT INTO documento_identidad(inquilino_id,cara,referencia_archivo,tipo_real_archivo,tamano_bytes) VALUES (3,'frente',repeat('2',32),'application/pdf',1)$$);

-- R24: un solo uso, vencido, limpieza
SELECT asociar_cedula('h-frente', 2, repeat('a',32));
INSERT INTO resultado VALUES ('R24 primer uso del identificador', true, 'asociado a Beto');
SELECT espera_error('R24 segundo uso del mismo identificador', $$SELECT asociar_cedula('h-frente', 2, repeat('3',32))$$);
SELECT espera_error('R24 identificador vencido', $$SELECT asociar_cedula('h-vencido', 2, repeat('4',32))$$);
SELECT espera_error('R24 identificador inexistente', $$SELECT asociar_cedula('no-existe', 2, repeat('5',32))$$);
SELECT espera_error('R24 archivo de contrato usado como cedula', $$SELECT asociar_cedula('h-contrato1', 2, repeat('6',32))$$);
SELECT espera_valor('R24 el archivo de contrato rechazado como cedula queda sin usar (se deshizo)', (SELECT usado_en IS NULL FROM archivo_temporal WHERE identificador_hash='h-contrato1')::text, 'true');
SELECT espera_valor('R24 la limpieza elimina solo lo vencido y no asociado', limpiar_temporales()::text, '1');
SELECT espera_valor('R24 lo usado no se limpia', (SELECT eliminado_en IS NULL FROM archivo_temporal WHERE identificador_hash='h-frente')::text, 'true');
SELECT espera_error('R24 identificador ya limpiado', $$SELECT asociar_cedula('h-vencido', 2, repeat('4',32))$$);

-- R25: una cedula activa por cara
SELECT espera_error('R25 segundo frente activo del mismo inquilino', $$SELECT asociar_cedula('h-frente2', 2, repeat('7',32))$$);
SELECT espera_valor('R25 el identificador del frente rechazado queda sin usar (atomicidad)', (SELECT usado_en IS NULL FROM archivo_temporal WHERE identificador_hash='h-frente2')::text, 'true');
SELECT asociar_cedula('h-reverso', 2, repeat('c',32));
INSERT INTO resultado VALUES ('R25 el reverso es otra cara y se acepta', true, 'asociado');
UPDATE documento_identidad SET eliminado_en = now() WHERE inquilino_id = 2 AND cara = 'frente';
SELECT asociar_cedula('h-frente2', 2, repeat('b',32));
INSERT INTO resultado VALUES ('R25 reemplazo: marcado eliminado el anterior, el nuevo frente se acepta', true, 'asociado');
SELECT espera_valor('R25 queda un solo frente activo', (SELECT count(*)::text FROM documento_identidad WHERE inquilino_id=2 AND cara='frente' AND eliminado_en IS NULL), '1');

-- R22: fotografias del contrato
SELECT asociar_fotografia_contrato('h-contrato1', 2, repeat('d',32));
SELECT asociar_fotografia_contrato('h-contrato2', 2, repeat('e',32));
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
