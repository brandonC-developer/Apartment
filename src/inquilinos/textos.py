"""Borrador del texto informativo del consentimiento (RF-39, OL-13; decisión del solicitante del 24-oct-2026).

**NO es asesoría legal y NO está validado por un abogado** (DP-17, DP-21). Lo redactó el asistente a partir del
texto del art. 5 de la Ley 8968 (leído en la copia del MICITT generada el 7-ene-2026) y de lo que el sistema
realmente hace según la ERS v1.16. Lo que depende de una interpretación legal va marcado «[A VALIDAR POR EL
ABOGADO: …]» dentro del propio texto. Cuando el abogado entregue el texto definitivo se carga como una versión
nueva (`manage.py cargar_texto_consentimiento --archivo … --validado`); las versiones anteriores y los
consentimientos que apuntan a ellas no se tocan.

El texto cita los ocho puntos del artículo 5, 1.-, incisos a) a h), en el mismo orden.
"""

MARCA_DE_BORRADOR = 'BORRADOR SIN VALIDAR POR UN ABOGADO'

BORRADOR = '''\
BORRADOR SIN VALIDAR POR UN ABOGADO

AVISO INFORMATIVO Y CONSENTIMIENTO PARA EL TRATAMIENTO DE DATOS PERSONALES
(Ley N.º 8968, artículo 5)

Antes de pedirle sus datos personales, le informamos de modo expreso, preciso e inequívoco lo siguiente.

1. Existencia de una base de datos. Los datos que usted nos facilite se guardarán en una base de datos de carácter personal llamada «Sistema de Gestión de Alquileres», que sirve para administrar los alquileres de los que es responsable la persona indicada en el punto 8.

2. Fines de la recolección. Sus datos se recogen para: identificarlo y verificar su identidad como inquilino; preparar y administrar el contrato de alquiler, las obligaciones de pago, los pagos recibidos y su historial; que el administrador pueda contactarlo por su cuenta cuando lo necesite; y cumplir las obligaciones legales relacionadas con el alquiler. No se usan para publicidad ni se venden.

3. Destinatarios y quiénes pueden consultarlos. Solo puede consultar sus datos la persona que administra el sistema, mediante una cuenta protegida con segundo factor de autenticación. Para que el sistema funcione, sus datos están alojados, y sus copias de seguridad guardadas cifradas, en servidores de un proveedor de infraestructura ubicados en el extranjero (Estados Unidos), y un servicio de correo envía avisos al administrador sin incluir su número de documento ni imágenes. Los datos también podrán entregarse a una autoridad cuando la ley lo exija. [A VALIDAR POR EL ABOGADO: si el alojamiento y el correo en el extranjero son una transferencia de datos y qué debe decir este punto (DP-31).]

4. Carácter obligatorio o facultativo de sus respuestas. Son obligatorios su nombre completo, el tipo y el número de su documento de identidad y, antes de formalizar un contrato, la fotografía del frente de su documento. Son facultativos su teléfono, su correo electrónico y la fotografía del reverso del documento.

5. Tratamiento que se dará a los datos. Se guardan en el sistema; las fotografías del documento se guardan en un almacenamiento privado, solo las ve el administrador y cada vez que una se consulta queda un registro con la fecha y hora, sin copiar la imagen. Se conservan mientras el contrato esté vigente y hasta cinco años después de su fin; si no llega a formalizarse un contrato, hasta un año. Vencido el plazo se eliminan las fotografías y se desvinculan sus datos personales, y se conservan los movimientos de dinero sin identificarlo. [A VALIDAR POR EL ABOGADO: los plazos de conservación y su relación con las obligaciones contables o tributarias (DP-18).]

6. Consecuencias de negarse a dar los datos. Si usted no suministra los datos obligatorios o no da su consentimiento, no se le podrá registrar como inquilino en el sistema ni formalizar un contrato a través de él.

7. Derechos que le asisten. Usted puede pedir en cualquier momento que le informemos qué datos suyos tenemos (acceso), que los corrijamos o actualicemos (rectificación y actualización) y que los eliminemos (supresión), y puede revocar este consentimiento. Las solicitudes se resuelven en un plazo máximo de cinco días hábiles y son gratuitas. También puede acudir a la Agencia de Protección de Datos de los Habitantes. [A VALIDAR POR EL ABOGADO: alcance de la supresión frente a obligaciones legales de conservar datos (DP-18) y de la información que debe darse sobre la Agencia.]

8. Identidad y dirección del responsable de la base de datos. {nombre_responsable}, con dirección en {direccion_responsable}.

CONSENTIMIENTO

Con su firma en un documento físico, o con su aceptación en un documento electrónico, usted declara que leyó este aviso y da su consentimiento expreso para que sus datos personales se traten en la forma y para los fines indicados. Este consentimiento puede revocarse de la misma forma, por escrito, físico o electrónico, y la revocación no tiene efecto retroactivo: no afecta lo que se hizo con sus datos antes de ella.
'''


class FaltaIdentidadDelResponsable(Exception):
    """El texto debe decir quién es el responsable (punto 8): sin su nombre y dirección no se puede generar."""


def construir_borrador(nombre_responsable, direccion_responsable):
    nombre = (nombre_responsable or '').strip()
    direccion = (direccion_responsable or '').strip()
    if not nombre or not direccion:
        raise FaltaIdentidadDelResponsable(
            'Falta el nombre o la dirección del responsable de la base de datos: defínalos con '
            '`manage.py configurar_organizacion --nombre-responsable ... --direccion-responsable ...`.')
    return BORRADOR.format(nombre_responsable=nombre, direccion_responsable=direccion)
