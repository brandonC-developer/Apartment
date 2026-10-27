"""Lectura de inquilinos: lista, filtros y ficha (RF-03, RF-05). No audita: las lecturas ordinarias de
fichas no se auditan (RF-45); solo se audita ver una fotografía de cédula, que es de otro módulo."""
from django.db.models import Exists, OuterRef, Q

from .models import Consentimiento, DocumentoIdentidad, Inquilino, TextoConsentimiento

ESTADOS = ('activos', 'inactivos', 'todos')


def _frente_activo():
    return DocumentoIdentidad.objects.filter(
        inquilino=OuterRef('pk'), cara=DocumentoIdentidad.FRENTE, eliminado_en__isnull=True)


def listar_inquilinos(*, busqueda=None, estado='activos', sin_frente=False):
    """Inquilinos con `tiene_frente`. `busqueda` mira nombre, documento, teléfono y correo (sin distinguir
    mayúsculas). `sin_frente` incluye al que solo tiene el reverso o ninguna fotografía (RF-03).
    Los desasociados (sin datos personales) no se listan."""
    if estado not in ESTADOS:
        raise ValueError(f'Estado desconocido: {estado}')
    inquilinos = Inquilino.objects.filter(desasociado_en__isnull=True).annotate(tiene_frente=Exists(_frente_activo()))
    if estado == 'activos':
        inquilinos = inquilinos.filter(activo=True)
    elif estado == 'inactivos':
        inquilinos = inquilinos.filter(activo=False)
    texto = (busqueda or '').strip()
    if texto:
        inquilinos = inquilinos.filter(
            Q(nombre_completo__icontains=texto) | Q(numero_documento__icontains=texto)
            | Q(telefono__icontains=texto) | Q(correo__icontains=texto))
    if sin_frente:
        inquilinos = inquilinos.filter(tiene_frente=False)
    return inquilinos


def texto_vigente():
    """La versión más reciente del texto informativo, o None si aún no hay ninguna (RF-39)."""
    return TextoConsentimiento.objects.order_by('-version').first()


def consentimiento_vigente(inquilino):
    """El consentimiento sin revocar más reciente, o None (RF-39)."""
    return inquilino.consentimientos.filter(revocado_en__isnull=True).order_by('-otorgado_en', '-id').first()


def tiene_consentimiento_vigente(inquilino):
    """¿Se pueden guardar fotografías y, desde la E2, crear contratos nuevos con este inquilino? (RF-39)"""
    return inquilino.consentimientos.filter(revocado_en__isnull=True).exists()


def obtener_ficha(inquilino_id):
    """Todo lo de un inquilino que existe en la E1 (RF-05): datos, consentimiento y fotografías activas.
    El contrato vigente, las obligaciones y el historial los agregan la E2 y la E3."""
    inquilino = Inquilino.objects.get(pk=inquilino_id)
    documentos = {d.cara: d for d in inquilino.documentos.filter(eliminado_en__isnull=True)}
    consentimientos = list(inquilino.consentimientos.select_related('texto'))
    vigente = next((c for c in consentimientos if c.revocado_en is None), None)
    return {
        'inquilino': inquilino,
        'consentimiento': consentimientos[0] if consentimientos else None,
        'consentimiento_vigente': vigente,
        # Aviso en la ficha cuando el consentimiento se revocó y no hay otro vigente (RF-39, CA-67).
        'consentimiento_revocado': vigente is None and any(c.revocado_en for c in consentimientos),
        'puede_crear_contratos': vigente is not None,
        'consentimientos': consentimientos,
        'frente': documentos.get(DocumentoIdentidad.FRENTE),
        'reverso': documentos.get(DocumentoIdentidad.REVERSO),
        'falta_frente': DocumentoIdentidad.FRENTE not in documentos,
    }


def tiene_frente(inquilino):
    """¿Tiene el frente de la fotografía del documento activo? Sin él no se le puede crear un contrato (R26, RF-07, CA-78)."""
    return inquilino.documentos.filter(cara=DocumentoIdentidad.FRENTE, eliminado_en__isnull=True).exists()
