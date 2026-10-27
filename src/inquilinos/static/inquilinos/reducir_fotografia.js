/*
 * Reducción de la fotografía del documento en el navegador, antes de enviarla (RF-50; CA-73, CA-74).
 *
 * No es un control de seguridad: el servidor valida y reescribe siempre (RF-02). Sirve para que la foto de un
 * teléfono pese menos. Reglas de RF-50:
 *   1. el lado mayor no pasa de 2048 píxeles y una imagen más pequeña no se amplía;
 *   2. se codifica como JPEG con calidad inicial 0,85;
 *   3. si pesa más de 2 MB (objetivo), se prueban calidades menores sin bajar de 0,70;
 *   4. si aun así pesa más de 5 MiB, se reduce el lado mayor hasta que no lo pase;
 *   5. se conserva la orientación visible (el navegador aplica la marca EXIF al decodificar).
 * Si el navegador no puede reducir, se envía el original solo si es JPEG o PNG de hasta 5 MiB; si no, se informa
 * antes de enviar. Un solo archivo por petición (RF-02).
 *
 * Sin bibliotecas, sin eval ni HTML en línea: la política de contenido solo admite `script-src 'self'`.
 * Los valores intermedios de calidad (0,80 y 0,75) y el tamaño mínimo del lado (600 px) son propuesta del asistente.
 */
(function () {
  'use strict';

  var LADO_MAXIMO = 2048;
  var CALIDADES = [0.85, 0.80, 0.75, 0.70];
  var OBJETIVO_BYTES = 2000000;       // 2 MB
  var LIMITE_BYTES = 5242880;         // 5 MiB
  var FACTOR_DEL_LADO = 0.85;
  var LADO_MINIMO = 600;
  var TIPOS_ADMITIDOS = ['image/jpeg', 'image/png'];

  function ErrorDeEnvio(mensaje) {
    this.name = 'ErrorDeEnvio';
    this.message = mensaje;
  }
  ErrorDeEnvio.prototype = Object.create(Error.prototype);

  function puedeReducir() {
    var lienzo = document.createElement('canvas');
    return typeof lienzo.getContext === 'function' && typeof lienzo.toBlob === 'function' &&
      (typeof window.createImageBitmap === 'function' || typeof window.URL.createObjectURL === 'function');
  }

  function decodificar(archivo) {
    // `from-image`: el navegador aplica la orientación EXIF, así que la imagen se dibuja como se ve.
    if (typeof window.createImageBitmap === 'function') {
      return window.createImageBitmap(archivo, { imageOrientation: 'from-image' }).catch(function () {
        return window.createImageBitmap(archivo);
      });
    }
    return new Promise(function (resolver, rechazar) {
      var direccion = window.URL.createObjectURL(archivo);
      var imagen = new window.Image();
      imagen.onload = function () { window.URL.revokeObjectURL(direccion); resolver(imagen); };
      imagen.onerror = function () { window.URL.revokeObjectURL(direccion); rechazar(new Error('No se pudo leer la imagen')); };
      imagen.src = direccion;
    });
  }

  function anchoYAlto(imagen) {
    return { ancho: imagen.width || imagen.naturalWidth, alto: imagen.height || imagen.naturalHeight };
  }

  function dibujar(imagen, ancho, alto) {
    var lienzo = document.createElement('canvas');
    lienzo.width = ancho;
    lienzo.height = alto;
    var contexto = lienzo.getContext('2d');
    contexto.fillStyle = '#ffffff';              // un PNG con transparencia no debe quedar negro en JPEG
    contexto.fillRect(0, 0, ancho, alto);
    contexto.imageSmoothingEnabled = true;
    contexto.imageSmoothingQuality = 'high';
    contexto.drawImage(imagen, 0, 0, ancho, alto);
    return lienzo;
  }

  function codificar(lienzo, calidad) {
    return new Promise(function (resolver, rechazar) {
      lienzo.toBlob(function (blob) {
        if (blob) { resolver(blob); } else { rechazar(new Error('El navegador no pudo codificar la imagen')); }
      }, 'image/jpeg', calidad);
    });
  }

  function reducir(archivo, ladoMaximo) {
    var ladoDePartida = ladoMaximo || LADO_MAXIMO;
    if (!puedeReducir()) { return Promise.reject(new Error('Este navegador no puede reducir imágenes')); }
    return decodificar(archivo).then(function (imagen) {
      var medidas = anchoYAlto(imagen);
      if (!medidas.ancho || !medidas.alto) { throw new Error('Imagen sin tamaño'); }
      var escala = Math.min(1, ladoDePartida / Math.max(medidas.ancho, medidas.alto));  // nunca se amplía
      var ancho = Math.max(1, Math.round(medidas.ancho * escala));
      var alto = Math.max(1, Math.round(medidas.alto * escala));
      var estado = { blob: null, calidad: CALIDADES[0], ancho: ancho, alto: alto };

      function probarCalidades() {
        var indice = 0;
        var lienzo = dibujar(imagen, estado.ancho, estado.alto);
        function siguiente() {
          estado.calidad = CALIDADES[indice];
          return codificar(lienzo, estado.calidad).then(function (blob) {
            estado.blob = blob;
            if (blob.size > OBJETIVO_BYTES && indice < CALIDADES.length - 1) { indice += 1; return siguiente(); }
            return blob;
          });
        }
        return siguiente();
      }

      function achicarHastaCaber() {
        return probarCalidades().then(function () {
          if (estado.blob.size <= LIMITE_BYTES) { return estado; }
          var lado = Math.max(estado.ancho, estado.alto);
          if (lado <= LADO_MINIMO) { throw new Error('No se pudo reducir por debajo de 5 MiB'); }
          var nuevo = Math.max(LADO_MINIMO, Math.round(lado * FACTOR_DEL_LADO));
          estado.ancho = Math.max(1, Math.round(estado.ancho * nuevo / lado));
          estado.alto = Math.max(1, Math.round(estado.alto * nuevo / lado));
          return achicarHastaCaber();
        });
      }
      if (typeof imagen.close === 'function') {
        return achicarHastaCaber().then(function (resultado) { imagen.close(); return resultado; });
      }
      return achicarHastaCaber();
    }).then(function (estado) {
      return { blob: estado.blob, ancho: estado.ancho, alto: estado.alto, calidad: estado.calidad, original: false };
    });
  }

  function prepararEnvio(archivo, ladoMaximo) {
    return reducir(archivo, ladoMaximo).catch(function () {
      if (TIPOS_ADMITIDOS.indexOf(archivo.type) !== -1 && archivo.size <= LIMITE_BYTES) {
        return { blob: archivo, ancho: 0, alto: 0, calidad: 0, original: true };
      }
      if (archivo.size > LIMITE_BYTES) {
        throw new ErrorDeEnvio('El archivo pesa más de 5 MiB y este navegador no puede reducirlo. Elija una imagen más pequeña.');
      }
      throw new ErrorDeEnvio('Este navegador no pudo preparar la imagen. Elija un JPEG o un PNG de hasta 5 MiB.');
    });
  }

  function mostrar(formulario, texto, estado) {
    var region = formulario.querySelector('[data-sga-mensaje]');
    if (region) { region.textContent = texto; }
    formulario.setAttribute('data-estado', estado);
  }

  function textoDeErrores(respuesta) {
    var errores = (respuesta && respuesta.errores) || {};
    var partes = [];
    Object.keys(errores).forEach(function (campo) { partes.push(errores[campo].join(' ')); });
    return partes.length ? partes.join(' ') : 'No se pudo guardar la fotografía.';
  }

  // La fotografía del contrato parte de un lado mayor de 3508 px (RF-52, DP-29): el formulario lo declara en
  // `data-lado-maximo`. Un valor ausente o fuera de rango se ignora y rige el de la cédula.
  function ladoDelFormulario(formulario) {
    var valor = parseInt(formulario.getAttribute('data-lado-maximo'), 10);
    return valor >= LADO_MINIMO && valor <= 8000 ? valor : LADO_MAXIMO;
  }

  function enlazar(formulario) {
    formulario.addEventListener('submit', function (evento) {
      evento.preventDefault();
      var entrada = formulario.querySelector('input[type="file"]');
      var archivo = entrada && entrada.files && entrada.files[0];
      if (!archivo) { mostrar(formulario, 'Elija una fotografía.', 'sin-enviar'); return; }
      mostrar(formulario, 'Preparando la fotografía…', 'preparando');
      prepararEnvio(archivo, ladoDelFormulario(formulario)).then(function (resultado) {
        var datos = new window.FormData();
        datos.append('archivo', resultado.blob, resultado.original ? archivo.name : 'documento.jpg');
        var token = formulario.querySelector('input[name="csrfmiddlewaretoken"]');
        formulario.setAttribute('data-enviado-bytes', String(resultado.blob.size));
        formulario.setAttribute('data-enviado-tipo', resultado.blob.type || '');
        formulario.setAttribute('data-enviado-ancho', String(resultado.ancho));
        formulario.setAttribute('data-enviado-alto', String(resultado.alto));
        formulario.setAttribute('data-enviado-calidad', String(resultado.calidad));
        formulario.setAttribute('data-enviado-original', resultado.original ? 'si' : 'no');
        mostrar(formulario, 'Enviando…', 'enviando');
        return window.fetch(formulario.getAttribute('action'), {
          method: 'POST', body: datos, credentials: 'same-origin',
          headers: { 'X-CSRFToken': token ? token.value : '' }
        }).then(function (respuesta) {
          return respuesta.json().catch(function () { return {}; }).then(function (cuerpo) {
            if (respuesta.status === 201) {
              mostrar(formulario, 'Fotografía guardada.', 'guardada');
            } else {
              mostrar(formulario, textoDeErrores(cuerpo), 'rechazada');
            }
          });
        });
      }).catch(function (error) {
        mostrar(formulario, error instanceof ErrorDeEnvio ? error.message : 'No se pudo enviar la fotografía.', 'sin-enviar');
      });
    });
  }

  function iniciar() {
    var formularios = document.querySelectorAll('form[data-sga-fotografia]');
    Array.prototype.forEach.call(formularios, enlazar);
  }

  window.SGA = window.SGA || {};
  window.SGA.fotografia = { prepararEnvio: prepararEnvio, reducir: reducir, enlazar: enlazar };
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', iniciar); } else { iniciar(); }
}());
