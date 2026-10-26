"""Validación y limpieza de las fotografías del documento en el servidor (RF-02, ADR-003, BR-05, BR-06;
CA-74, CA-83; decisión 2 de la E1, 24-oct-2026).

Cada archivo que llega pasa por aquí, con o sin la reducción del navegador (que no es un control de seguridad):

1. no vacío y de hasta 5 242 880 bytes;
2. tipo REAL JPEG o PNG, por el contenido y no por el nombre ni por el tipo que declara el navegador;
3. tope de píxeles (60 millones) comprobado ANTES de decodificar, contra las «bombas de descompresión»;
4. decodificación completa: un archivo truncado o dañado se rechaza (CA-83);
5. se aplica la orientación EXIF y se escribe un archivo NUEVO sin metadatos (ubicación, cámara, fecha, comentarios,
   XMP, imágenes adicionales de un MPO): lo que se guarda no es el archivo recibido. Se conserva el perfil de color ICC, que no es un dato personal.

Esto sigue la recomendación de OWASP de decodificar y volver a codificar, y sus límites: «rewriting does not
guarantee that all malicious content is removed, and the image processor itself handles untrusted input». Por eso
la biblioteca se mantiene al día (`pip-audit`) y el servicio corre aislado (systemd).
"""
import warnings
from dataclasses import dataclass
from io import BytesIO

from PIL import Image, ImageFile, ImageOps

from .models import TAMANO_MAXIMO

MAX_PIXELES = 60_000_000  # propuesta del asistente: un iPhone de 48 MP cabe
Image.MAX_IMAGE_PIXELS = MAX_PIXELES
ImageFile.LOAD_TRUNCATED_IMAGES = False  # un archivo truncado se rechaza

# Pillow llama «MPO» a un JPEG que lleva una extensión de varias imágenes (miniaturas, mapa de profundidad o de ganancia
# HDR): es lo normal en un iPhone, un Pixel o un Samsung recientes. Sigue siendo un JPEG; solo se guarda la primera
# imagen, de modo que las demás (y sus metadatos) no pasan al archivo nuevo.
_TIPOS = {'JPEG': 'image/jpeg', 'MPO': 'image/jpeg', 'PNG': 'image/png'}
# Para abrir solo JPEG y PNG; un JPEG con varias imágenes se abre como JPEG y Pillow lo devuelve como «MPO».
_FORMATOS_DE_ENTRADA = ['JPEG', 'PNG']
_EXTENSIONES = {'image/jpeg': 'jpg', 'image/png': 'png'}


class ImagenInvalida(Exception):
    """El archivo no se acepta; el mensaje es para el administrador."""


@dataclass(frozen=True)
class ImagenLimpia:
    contenido: bytes
    tipo: str
    ancho: int
    alto: int

    @property
    def extension(self):
        return _EXTENSIONES[self.tipo]


def procesar_imagen(datos):
    if not datos:
        raise ImagenInvalida('El archivo está vacío.')
    if len(datos) > TAMANO_MAXIMO:
        raise ImagenInvalida('El archivo pesa más de 5 MiB.')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            imagen = Image.open(BytesIO(datos), formats=_FORMATOS_DE_ENTRADA)
            formato = imagen.format
            tipo = _TIPOS[formato]
            if imagen.width * imagen.height > MAX_PIXELES:
                raise ImagenInvalida('La imagen tiene demasiados píxeles.')
            imagen.load()  # decodificación completa (CA-83)
    except ImagenInvalida:
        raise
    except Image.UnidentifiedImageError:
        raise ImagenInvalida('El archivo no es una imagen JPEG o PNG.')
    except (Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise ImagenInvalida('La imagen tiene demasiados píxeles.')
    except (OSError, SyntaxError, ValueError, EOFError, MemoryError, OverflowError):
        raise ImagenInvalida('La imagen está dañada o incompleta y no se pudo leer.')

    icc = imagen.info.get('icc_profile')
    orientacion = imagen.getexif().get(0x0112, 1)
    salida = BytesIO()
    argumentos = {'icc_profile': icc} if icc else {}
    try:
        if formato == 'JPEG' and orientacion in (1, None) and imagen.mode in ('RGB', 'L', 'CMYK'):
            # Sin girar se guarda con las mismas tablas de calidad y submuestreo («keep»), así el peso y el aspecto casi
            # no cambian; NO es una transcodificación sin pérdida (Pillow vuelve a codificar desde los píxeles). Se
            # vacía `info` porque Pillow copia de ahí, por ejemplo, el comentario.
            imagen.info = {}
            imagen.save(salida, 'JPEG', quality='keep', subsampling='keep', qtables='keep', **argumentos)
        else:
            limpia = ImageOps.exif_transpose(imagen)  # copia con la orientación aplicada y sin la marca
            if limpia.mode == 'P':
                limpia = limpia.convert('RGBA' if 'transparency' in limpia.info else 'RGB')
            limpia.info = {}  # fuera EXIF, XMP, comentarios y demás metadatos
            if tipo == 'image/jpeg':
                if limpia.mode not in ('RGB', 'L', 'CMYK'):
                    limpia = limpia.convert('RGB')
                # Un MPO no admite «keep» (Pillow lo exige de un JPEG simple): se vuelve a codificar a 90 (propuesta).
                limpia.save(salida, 'JPEG', quality=90 if formato == 'MPO' else 95, **argumentos)
            else:
                limpia.save(salida, 'PNG', optimize=True, **argumentos)
            imagen = limpia
    except (OSError, ValueError, KeyError) as error:
        raise ImagenInvalida(f'No se pudo procesar la imagen: {error}')
    resultado = salida.getvalue()
    if len(resultado) > TAMANO_MAXIMO:
        raise ImagenInvalida('La imagen pesa más de 5 MiB después de limpiarla; use una más pequeña.')
    return ImagenLimpia(contenido=resultado, tipo=tipo, ancho=imagen.width, alto=imagen.height)
