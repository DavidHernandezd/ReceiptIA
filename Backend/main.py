from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from typing import List
from typing import Annotated
import json
import logging
import time
import uuid
from contextvars import ContextVar
import io
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

from PIL import Image

import pytesseract
import cv2
import numpy as np

app = FastAPI(
    title="ReceiptIA API",
    description="Backend para auditoría inteligente de facturas y recibos.",
    version="1.0.0",
)

# ==============================
# OBSERVABILIDAD - SEMANA 5
# ==============================
# Versiones explícitas para poder correlacionar las mediciones y los logs.
APP_VERSION = "1.0.0"
AI_MODEL = "gemini-2.5-flash"
AI_COMPONENT = "Gemini 2.5 Flash"
PROMPT_VERSION = "1.0"

_request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")


class JsonFormatter(logging.Formatter):
    """Formatter de logs estructurados para observabilidad.

    Nunca registra contraseñas, tokens, headers de autorización, contenido de
    archivos ni texto OCR completo.
    """

    def format(self, record):
        payload = {
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "service": "receiptia-backend",
            "request_id": getattr(record, "request_id", _request_id_ctx.get()),
            "route": getattr(record, "route", None),
            "method": getattr(record, "method", None),
            "status": getattr(record, "status", None),
            "duration_ms": getattr(record, "duration_ms", None),
            "app_version": APP_VERSION,
            "ai_component": AI_COMPONENT,
            "ai_model": AI_MODEL,
            "prompt_version": PROMPT_VERSION,
            "event": getattr(record, "event", record.getMessage()),
            "error_type": getattr(record, "error_type", None),
        }

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


logger = logging.getLogger("receiptia")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
logger.propagate = False


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    """Registra una línea estructurada por solicitud.

    Campos mínimos de Semana 5: request_id, ruta, estado, duración y versión
    del componente IA. El identificador también se devuelve en X-Request-ID.
    """
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    token = _request_id_ctx.set(request_id)
    started = time.perf_counter()
    status_code = 500
    event = "request_error"
    error_type = None

    try:
        response = await call_next(request)
        status_code = response.status_code
        event = "request_completed" if status_code < 400 else "request_failed"
        if status_code >= 400:
            error_type = f"HTTP_{status_code}"
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as exc:
        error_type = type(exc).__name__
        logger.error(
            "Solicitud finalizada con excepción",
            extra={
                "request_id": request_id,
                "route": request.url.path,
                "method": request.method,
                "status": 500,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
                "event": "request_error",
                "error_type": error_type,
            },
            exc_info=True,
        )
        raise
    finally:
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        if event != "request_error" or status_code != 500:
            log_level = logging.INFO if status_code < 400 else logging.WARNING
            logger.log(
                log_level,
                "Solicitud procesada",
                extra={
                    "request_id": request_id,
                    "route": request.url.path,
                    "method": request.method,
                    "status": status_code,
                    "duration_ms": duration_ms,
                    "event": event,
                    "error_type": error_type,
                },
            )
        _request_id_ctx.reset(token)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# RUTAS DE INFORMACIÓN DEL SERVICIO
# ==============================

@app.get("/")
def inicio():
    """Muestra información general del backend."""
    return {
        "aplicacion": "ReceiptIA",
        "version": "1.0.0",
        "documentacion": "/docs",
    }


@app.get("/health")
def health():
    """Permite verificar que el backend está disponible."""
    return {
        "status": "ok",
        "servicio": "ReceiptIA Backend",
    }


# ==============================
# CONFIGURACIÓN DE VARIABLES DE ENTORNO
# ==============================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


# ==============================
# CONFIGURACIÓN DE GEMINI
# ==============================

def obtener_cliente_gemini():
    """
    Crea el cliente de Gemini únicamente cuando se necesita.

    Esto permite importar y probar el backend sin guardar
    una clave real dentro de GitHub Actions.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if (
        not api_key
        or not api_key.strip()
        or api_key == "TU_API_KEY_VA_AQUI"
    ):
        raise RuntimeError(
            "No se encontró la API Key de Gemini. "
            "Crea un archivo .env en la misma carpeta de main.py y coloca: "
            "GEMINI_API_KEY=TU_API_KEY_REAL"
        )

    return genai.Client(api_key=api_key)


GEMINI_CONFIG = types.GenerateContentConfig(
    temperature=0,
    response_mime_type="application/json",
)


# ==============================
# CONFIGURACIÓN DE TESSERACT
# ==============================

def configurar_tesseract():
    """
    Busca Tesseract OCR de forma flexible.

    Orden de búsqueda:
    1. Variable TESSERACT_CMD en el archivo .env
    2. Carpeta portable dentro del proyecto: Backend/Tesseract-OCR/tesseract.exe
    3. Ruta normal de instalación en Windows
    4. Ruta normal de instalación en Windows 32 bits
    5. Tesseract disponible en el PATH del sistema
    """

    rutas_posibles = [
        os.getenv("TESSERACT_CMD"),
        str(BASE_DIR / "Tesseract-OCR" / "tesseract.exe"),
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        shutil.which("tesseract")
    ]

    for ruta in rutas_posibles:
        if ruta and os.path.exists(ruta):
            pytesseract.pytesseract.tesseract_cmd = ruta
            print(f"Tesseract OCR encontrado en: {ruta}")
            return ruta

    print("ADVERTENCIA: No se encontró Tesseract OCR instalado.")
    print("Ejecuta Instalar_Tesseract.bat o instala Tesseract manualmente.")
    print("También puedes configurar la ruta en .env con:")
    print("TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe")

    return None


TESSERACT_CMD_DETECTADO = configurar_tesseract()


# ==============================
# FUNCIONES DE TESSERACT
# ==============================

def limpiar_imagen_para_ocr(img):
    """
    Mejora la imagen para que Tesseract pueda leer mejor el texto.
    """

    img = img.convert("RGB")
    imagen_np = np.array(img)

    imagen_cv = cv2.cvtColor(imagen_np, cv2.COLOR_RGB2BGR)

    gris = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2GRAY)

    gris = cv2.resize(
        gris,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    _, umbral = cv2.threshold(
        gris,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return umbral


def leer_texto_con_tesseract(imagen_limpia):
    """
    Lee el texto usando Tesseract.
    Primero intenta español + inglés.
    Si falla por idioma, usa solo inglés.
    Si Tesseract no está instalado, devuelve un error claro.
    """

    if not TESSERACT_CMD_DETECTADO:
        raise RuntimeError(
            "No se encontró Tesseract OCR. "
            "Ejecuta Instalar_Tesseract.bat o configura TESSERACT_CMD en el archivo .env."
        )

    try:
        texto = pytesseract.image_to_string(imagen_limpia, lang="spa+eng")
    except pytesseract.TesseractNotFoundError:
        raise RuntimeError(
            "Tesseract OCR no fue encontrado. "
            "Instálalo o configura TESSERACT_CMD en el archivo .env."
        )
    except pytesseract.TesseractError:
        texto = pytesseract.image_to_string(imagen_limpia, lang="eng")

    return texto


def texto_ocr_es_valido(texto):
    """
    Verifica si Tesseract logró extraer suficiente texto.
    """

    if not texto:
        return False

    texto_limpio = texto.strip()

    if len(texto_limpio) < 20:
        return False

    return True


def limpiar_json_respuesta(texto):
    """
    Extrae el JSON puro desde la respuesta de Gemini.
    """

    inicio = texto.find("{")
    fin = texto.rfind("}") + 1

    if inicio == -1 or fin == 0:
        raise ValueError("Gemini no devolvió un JSON válido.")

    json_limpio = texto[inicio:fin]

    return json.loads(json_limpio)


def generar_con_gemini(prompt):
    """
    Envía el prompt a Gemini usando configuración estable.

    También mide el tiempo empleado exclusivamente por Gemini.
    """

    client = obtener_cliente_gemini()

    inicio_gemini = time.perf_counter()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=GEMINI_CONFIG,
        )

        duracion_gemini_ms = round(
            (time.perf_counter() - inicio_gemini) * 1000,
            2
        )

        print(f"Gemini completado en: {duracion_gemini_ms} ms")

        return response

    except Exception as e:
        duracion_gemini_ms = round(
            (time.perf_counter() - inicio_gemini) * 1000,
            2
        )

        print(
            f"Gemini falló después de: "
            f"{duracion_gemini_ms} ms"
        )

        raise


def crear_respuesta_error_ocr(texto_ocr):
    """
    Devuelve una respuesta estándar si el OCR no pudo leer bien.
    """

    return {
        "error": "Tesseract no pudo extraer suficiente texto de la imagen. Intenta con una imagen más clara.",
        "comercio": None,
        "nit_emisor": None,
        "fecha": None,
        "items": [],
        "subtotal": 0.00,
        "iva": 0.00,
        "total": 0.00,
        "es_exenta": False,
        "tiene_anomalias": True,
        "anomalias": [
            {
                "tipo": "Texto no detectado",
                "ubicacion": "Imagen completa",
                "descripcion": "El OCR no logró extraer suficiente texto para que Gemini pueda analizar la factura.",
                "valor_detectado": texto_ocr,
                "valor_esperado": "Texto legible de la factura"
            }
        ],
        "texto_ocr": texto_ocr,
        "metodo": "Tesseract OCR + Gemini texto"
    }


def crear_respuesta_error_lote(factura_id, nombre_archivo, texto_ocr, mensaje):
    """
    Devuelve una factura con error para procesamiento por lote.
    """

    return {
        "factura_id": factura_id,
        "nombre_archivo": nombre_archivo,
        "comercio": None,
        "nit_emisor": None,
        "fecha": None,
        "items": [],
        "subtotal": 0.00,
        "iva": 0.00,
        "total": 0.00,
        "es_exenta": False,
        "tiene_anomalias": True,
        "anomalias": [
            {
                "tipo": "Error de OCR",
                "ubicacion": "Imagen completa",
                "descripcion": mensaje,
                "valor_detectado": texto_ocr,
                "valor_esperado": "Texto legible de la factura"
            }
        ],
        "texto_ocr": texto_ocr,
        "metodo": "Tesseract OCR + Gemini texto en lote"
    }


def normalizar_factura(factura):
    """
    Asegura que la factura tenga todos los campos esperados.
    """

    factura.setdefault("comercio", None)
    factura.setdefault("nit_emisor", None)
    factura.setdefault("fecha", None)
    factura.setdefault("items", [])
    factura.setdefault("subtotal", 0.00)
    factura.setdefault("iva", 0.00)
    factura.setdefault("total", 0.00)
    factura.setdefault("es_exenta", False)
    factura.setdefault("tiene_anomalias", False)
    factura.setdefault("anomalias", [])

    return factura


def corregir_falsos_positivos_factura_consumidor_final(factura):
    """
    Corrección adicional después de Gemini.

    Evita que una Factura Consumidor Final sea marcada como anomalía
    únicamente porque no muestra IVA separado.

    Esto ayuda con casos como:
    - Total: 50.00
    - IVA: 0.00
    - Factura Consumidor Final
    """

    texto_ocr = str(factura.get("texto_ocr", "")).lower()
    metodo = str(factura.get("metodo", "")).lower()

    es_factura_consumidor_final = (
        "factura consumidor final" in texto_ocr
        or "consumidor final" in texto_ocr
    )

    if not es_factura_consumidor_final:
        return factura

    anomalias = factura.get("anomalias", [])

    if not anomalias:
        return factura

    nuevas_anomalias = []

    for anomalia in anomalias:
        texto_anomalia = (
            str(anomalia.get("tipo", "")) + " " +
            str(anomalia.get("ubicacion", "")) + " " +
            str(anomalia.get("descripcion", "")) + " " +
            str(anomalia.get("valor_detectado", "")) + " " +
            str(anomalia.get("valor_esperado", ""))
        ).lower()

        es_falso_positivo_iva = (
            "iva" in texto_anomalia
            and (
                "13%" in texto_anomalia
                or "6.50" in texto_anomalia
                or "no corresponde" in texto_anomalia
                or "diferencia matemática" in texto_anomalia
                or "ventas gravadas" in texto_anomalia
            )
            and (
                "no muestra iva separado" in texto_ocr
                or "factura consumidor final" in texto_ocr
                or "consumidor final" in texto_ocr
            )
        )

        if not es_falso_positivo_iva:
            nuevas_anomalias.append(anomalia)

    factura["anomalias"] = nuevas_anomalias
    factura["tiene_anomalias"] = len(nuevas_anomalias) > 0

    return factura


def reglas_auditoria_salvadorenas():
    """
    Reglas usadas por Gemini para reducir falsos positivos.
    """

    return """
REGLAS GENERALES PARA EL SALVADOR:

1. No todas las ventas generan IVA.
   Una factura puede tener:
   - Ventas gravadas
   - Ventas exentas
   - Ventas no sujetas
   - Otros montos no afectos

2. Solo calcula IVA del 13% sobre montos que estén claramente en "Ventas Gravadas",
   excepto cuando el documento sea Factura Consumidor Final, ticket POS o factura
   con precio final al consumidor.

3. Si un monto aparece en "Ventas Exentas" y el IVA es $0.00, eso puede ser correcto.
   No lo marques como anomalía.

4. Si un monto aparece en "Ventas No Sujetas" y el IVA es $0.00, eso puede ser correcto.
   No lo marques como anomalía.

5. No asumas que todos los productos o servicios deben pagar IVA.

6. Si el emisor parece ser:
   - Universidad
   - Centro educativo
   - Colegio
   - Institución pública
   - ONG
   - Fundación
   - Institución de salud
   - Clínica
   - Hospital
   - Asociación
   y el documento muestra ventas exentas o IVA $0.00, no marques anomalía salvo que exista una contradicción matemática clara.

7. Si el documento muestra:
   Ventas Exentas > 0
   Ventas Gravadas = 0
   IVA = 0
   Total = Ventas Exentas
   entonces NO hay anomalía.

8. Si el documento muestra:
   Ventas No Sujetas > 0
   Ventas Gravadas = 0
   IVA = 0
   Total = Ventas No Sujetas
   entonces NO hay anomalía.

9. Si el documento tiene ventas gravadas mayores a $0.00, entonces sí puedes revisar si el IVA corresponde aproximadamente al 13% de las ventas gravadas,
   excepto cuando el documento sea Factura Consumidor Final o ticket donde el precio puede venir como precio final al consumidor.

10. No trates "IVA Retenido" como si fuera el IVA normal de la venta.
    IVA, IVA Retenido, Retención, Percepción, Renta Retenida y Otros Montos no Afectos son conceptos diferentes.

11. Si aparece "IVA Retenido: $0.00", eso no significa que la factura esté mal.

12. Si hay descuentos, rebajas o descuentos por ítem, calcula el total después de restarlos.

13. Si hay:
   - Propina
   - Servicio
   - Envío
   - Recargo
   - Comisión
   - Otros montos no afectos
   inclúyelos en la validación del total si el documento los suma.

14. Permite diferencias pequeñas por redondeo.
    No marques anomalía si la diferencia matemática es menor o igual a $0.02.
    Si la diferencia está entre $0.03 y $0.10, solo marca "requiere revisión manual".
    Solo marca anomalía matemática clara si la diferencia es mayor a $0.10.

REGLA PRIORITARIA PARA FACTURA CONSUMIDOR FINAL:

15. Si el documento dice "Factura Consumidor Final", "FACTURA CONSUMIDOR FINAL",
    "Consumidor Final" o parece ticket POS:

    - Esta regla tiene prioridad sobre la regla general de IVA.
    - No calcules automáticamente un IVA esperado del 13% solo porque aparece una columna llamada "Gravada".
    - En Factura Consumidor Final, el precio puede presentarse como precio final al consumidor.
    - Puede no mostrar IVA separado.
    - Puede mostrar IVA como $0.00 si el documento no separa el impuesto.
    - No marques anomalía únicamente porque IVA aparezca como $0.00.
    - No marques anomalía únicamente porque no aparece IVA separado.
    - Si el Total a pagar coincide con el Monto total de la operación y no hay otra contradicción clara, considera la factura correcta.
    - Solo marca anomalía si el documento muestra explícitamente un IVA calculado y ese IVA no coincide,
      o si el total interno no cuadra con los montos mostrados.

REGLAS SEGÚN TIPO DE DOCUMENTO:

16. Si el documento dice "Comprobante de Crédito Fiscal":
    - Revisa con más detalle ventas gravadas, IVA, subtotal y total.
    - Respeta ventas exentas y ventas no sujetas.
    - No exijas IVA sobre ventas exentas o no sujetas.

17. Si el documento dice "Nota de Crédito":
    - No lo trates como una factura normal.
    - Puede disminuir montos.
    - Busca documento relacionado, motivo y monto ajustado.
    - No marques anomalía solo porque los montos sean negativos o de ajuste.

18. Si el documento dice "Nota de Débito":
    - No lo trates como una factura normal.
    - Puede aumentar montos.
    - Busca documento relacionado, motivo y monto ajustado.

19. Si el documento dice "Factura de Sujeto Excluido":
    - No exijas IVA como en una factura normal.
    - Puede estar relacionado con retenciones.
    - No marques anomalía por ausencia de IVA.

20. Si el documento dice "Comprobante de Retención":
    - No lo trates como una venta normal.
    - Analiza retenciones, sujeto retenido, base y monto retenido.
    - No exijas estructura de factura común.

21. Si el documento dice "Comprobante de Donación":
    - No lo trates como una venta gravada normal.
    - Puede no tener IVA.

22. Si el documento dice "Factura de Exportación":
    - No exijas IVA como una factura local común.
    - Puede tener tratamiento tributario diferente.

23. Si el documento tiene:
    - Código de generación
    - Sello de recepción
    - Número de control
    - Tipo de DTE
    - Modelo de facturación
    - Tipo de transmisión
    - Código QR
    entonces trátalo como Documento Tributario Electrónico.
    No marques anomalía solo porque no tenga número de factura tradicional.

REGLAS SOBRE CAMPOS:

24. NIT del emisor:
    - Si aparece claramente, extrae el NIT.
    - Si no aparece por error OCR, usa null.
    - No marques anomalía fiscal grave si el documento es ticket o recibo simple.
    - En DTE puede aparecer también NRC, DUI, número de control o código de generación.

25. Fecha:
    - Acepta formatos como:
      2026-02-27
      27/02/2026
      27-02-2026
      2026/02/27
      Fecha y hora de emisión
    - Si hay fecha y hora, extrae la fecha principal.
    - Si la fecha está ilegible, marca "requiere revisión manual", no necesariamente anomalía fiscal.

26. Comercio:
    - Puede aparecer como nombre comercial, razón social, emisor, establecimiento o sucursal.
    - Si el OCR mezcla líneas, usa el nombre más probable.
    - No inventes el comercio si no aparece.

27. Receptor:
    - Puede aparecer con nombre, DUI, NIT, NRC, correo o dirección.
    - No es obligatorio devolverlo en el JSON, pero úsalo para interpretar el documento.

28. Items:
    - Extrae solo productos o servicios reales.
    - No confundas totales, subtotales, descuentos, QR, códigos de generación, sellos de recepción, NRC, NIT o números de control como productos.
    - Si una línea tiene descripción y monto, puede ser item.
    - Si la descripción está parcialmente dañada por OCR, extrae lo más legible.

29. Montos:
    - Acepta montos con $.
    - Acepta montos sin $.
    - Acepta 143.75, 1,143.75, 1143.75.
    - Si OCR lee O como 0 o I como 1, interpreta con cuidado.
    - No inventes montos que no aparezcan.

30. Subtotal:
    - Puede aparecer como Subtotal, Sub-Total, Suma, Sumas, Monto global, Total de ventas o Total operaciones.
    - No siempre significa lo mismo en todos los documentos.
    - Si no aparece claramente, calcúlalo solo si los datos son suficientes.

31. Total:
    - Puede aparecer como Total, Total a pagar, Monto total de la operación, Total operaciones o Total venta.
    - El total final debe ser el monto más representativo a pagar, no un código ni un número de control.

32. IVA:
    - Puede aparecer como IVA, Débito fiscal, IVA retenido, IVA percibido.
    - No confundas IVA retenido con IVA cobrado.
    - Si solo aparece IVA retenido y es $0.00, no marques anomalía automáticamente.

REGLAS PARA DETECTAR ANOMALÍAS:

33. Marca anomalía únicamente cuando exista un error claro y sustentado por el texto.

34. No marques como anomalía:
    - Venta exenta con IVA $0.00.
    - Venta no sujeta con IVA $0.00.
    - Ticket sin IVA separado.
    - Factura Consumidor Final sin IVA separado.
    - Factura Consumidor Final con precio final al consumidor.
    - Documento educativo exento.
    - Documento médico exento.
    - Documento de donación sin IVA.
    - Nota de crédito con valores de ajuste.
    - Factura de sujeto excluido sin IVA.
    - Error leve de redondeo.

35. Sí puedes marcar anomalía cuando:
    - En Comprobante de Crédito Fiscal, ventas gravadas > 0 y el IVA no corresponde al 13%, con diferencia mayor a $0.10.
    - Subtotal + IVA - descuentos + otros cargos no coincide con total, con diferencia mayor a $0.10.
    - Falta total y el documento debería tenerlo.
    - El total es menor que cero en una factura normal que no sea nota de crédito.
    - Hay productos sin monto claramente visibles.
    - Hay montos ilegibles que impiden validar la factura.
    - Hay contradicción clara entre columnas.
    - El documento dice gravado, pero todo aparece sin IVA y sin explicación, siempre que NO sea Factura Consumidor Final.

36. Si hay duda razonable, no uses una anomalía definitiva.
    Usa una anomalía suave con tipo:
    "Requiere revisión manual"

37. No uses palabras como fraude, ilegal o falsificado.
    Usa términos como:
    - inconsistencia
    - posible error
    - requiere revisión
    - dato no detectado
    - diferencia matemática

38. Si el documento parece correcto, devuelve:
    "tiene_anomalias": false
    "anomalias": []

CASO ESPECIAL IMPORTANTE:

Si el texto muestra una factura de universidad, centro educativo o institución similar, y el monto aparece en "Ventas Exentas" con IVA $0.00 y total igual al monto exento, considera la factura correcta.

Ejemplo correcto:
Ventas Exentas: 143.75
Ventas Gravadas: 0.00
IVA: 0.00
Total a pagar: 143.75

En ese caso devuelve:
"tiene_anomalias": false
"anomalias": []

CASO ESPECIAL FACTURA CONSUMIDOR FINAL:

Si el texto muestra:
- FACTURA CONSUMIDOR FINAL
- Total a pagar igual al monto total de la operación
- IVA no separado o IVA $0.00
- No hay contradicción matemática interna

Entonces devuelve:
"tiene_anomalias": false
"anomalias": []

No generes una anomalía diciendo que el IVA esperado debería ser 13% solo por aparecer una columna "Gravada".

REGLAS FINALES DE DECISIÓN:

- Si no hay anomalías claras, usa:
  "tiene_anomalias": false
  "anomalias": []

- Si hay una o más anomalías claras, usa:
  "tiene_anomalias": true

- Si la factura parece correcta pero el OCR tiene dudas menores, no marques anomalía fiscal fuerte.
  Solo marca revisión manual si realmente impide validar los montos.

- No castigues al documento por errores del OCR.
- No inventes datos.
- No asumas IVA si la venta es exenta o no sujeta.
- Prioriza la estructura del documento sobre reglas generales.
- Factura Consumidor Final tiene prioridad sobre el cálculo automático de IVA.
"""


def crear_prompt_factura_individual(texto_ocr):
    """
    Prompt para analizar una sola factura.
    """

    return f"""
Eres un auditor fiscal experto de El Salvador.

Vas a analizar el texto extraído de una factura, recibo, ticket o Documento Tributario Electrónico de El Salvador.

IMPORTANTE:
El texto fue extraído usando OCR con Tesseract, por lo que puede tener errores de lectura, letras confundidas, columnas desordenadas o valores movidos.
Debes interpretar el contenido con criterio, pero sin inventar datos que no aparezcan.
Si un dato no aparece claramente, usa null.
Si algo no es seguro por mala lectura OCR, no afirmes que la factura está incorrecta. En ese caso, marca una observación como "requiere revisión manual".

Tu tarea es:
1. Extraer la información principal.
2. Identificar el tipo de documento si es posible.
3. Detectar anomalías fiscales o numéricas.
4. Evitar falsos positivos cuando el documento sea válido.

{reglas_auditoria_salvadorenas()}

FORMATO DE RESPUESTA:

Responde ÚNICAMENTE con un objeto JSON puro.
No escribas explicaciones fuera del JSON.
No uses markdown.
No uses ```json.

Usa exactamente esta estructura:

{{
    "comercio": "nombre del comercio o null",
    "nit_emisor": "NIT del emisor o null",
    "fecha": "fecha detectada o null",
    "items": [
        {{
            "descripcion": "nombre del producto o servicio",
            "monto": 0.00
        }}
    ],
    "subtotal": 0.00,
    "iva": 0.00,
    "total": 0.00,
    "es_exenta": false,
    "tiene_anomalias": false,
    "anomalias": [
        {{
            "tipo": "nombre corto de la anomalía",
            "ubicacion": "dónde aparece el problema en la factura",
            "descripcion": "explicación clara del problema",
            "valor_detectado": "valor que aparece en la factura",
            "valor_esperado": "valor correcto o esperado"
        }}
    ]
}}

TEXTO EXTRAÍDO POR TESSERACT OCR:
-------------------------
{texto_ocr}
-------------------------
"""


def crear_prompt_lote(bloques_facturas):
    """
    Prompt para analizar varias facturas en una sola solicitud.
    """

    return f"""
Eres un auditor fiscal experto de El Salvador.

Vas a analizar un LOTE de facturas, recibos, tickets o Documentos Tributarios Electrónicos de El Salvador.

IMPORTANTE:
Cada factura fue convertida a texto con OCR Tesseract.
Cada documento está separado por:
==================== INICIO FACTURA ====================
y
==================== FIN FACTURA ====================

Debes analizar cada factura por separado.
No mezcles datos entre facturas.
No uses el comercio, fecha, total o NIT de una factura para completar otra.
Si un dato no aparece claramente en una factura específica, usa null para esa factura.

{reglas_auditoria_salvadorenas()}

FORMATO DE RESPUESTA:

Responde ÚNICAMENTE con un objeto JSON puro.
No escribas explicaciones fuera del JSON.
No uses markdown.
No uses ```json.

Debes devolver exactamente esta estructura:

{{
    "facturas": [
        {{
            "factura_id": "id de la factura proporcionado",
            "nombre_archivo": "nombre del archivo proporcionado",
            "comercio": "nombre del comercio o null",
            "nit_emisor": "NIT del emisor o null",
            "fecha": "fecha detectada o null",
            "items": [
                {{
                    "descripcion": "nombre del producto o servicio",
                    "monto": 0.00
                }}
            ],
            "subtotal": 0.00,
            "iva": 0.00,
            "total": 0.00,
            "es_exenta": false,
            "tiene_anomalias": false,
            "anomalias": [
                {{
                    "tipo": "nombre corto de la anomalía",
                    "ubicacion": "dónde aparece el problema en la factura",
                    "descripcion": "explicación clara del problema",
                    "valor_detectado": "valor que aparece en la factura",
                    "valor_esperado": "valor correcto o esperado"
                }}
            ]
        }}
    ]
}}

REGLAS IMPORTANTES PARA EL LOTE:

- Debes devolver una factura por cada FACTURA_ID recibido.
- Conserva exactamente el mismo factura_id.
- Conserva exactamente el mismo nombre_archivo.
- No omitas facturas.
- No mezcles facturas.
- Si una factura parece correcta, usa:
  "tiene_anomalias": false
  "anomalias": []
- Si una factura tiene una inconsistencia clara, usa:
  "tiene_anomalias": true
- Si no estás seguro por error OCR, usa una anomalía suave con tipo "Requiere revisión manual".

LOTE DE FACTURAS EXTRAÍDAS POR TESSERACT OCR:
-------------------------
{bloques_facturas}
-------------------------
"""


def extraer_texto_de_archivo(file_name, content):
    """
    Abre una imagen, la limpia y extrae texto OCR.

    También mide el tiempo empleado exclusivamente por el proceso OCR.
    """

    inicio_ocr = time.perf_counter()

    img = Image.open(io.BytesIO(content)).convert("RGB")
    imagen_limpia = limpiar_imagen_para_ocr(img)
    texto_ocr = leer_texto_con_tesseract(imagen_limpia)

    duracion_ocr_ms = round(
        (time.perf_counter() - inicio_ocr) * 1000,
        2
    )

    print(f"OCR completado en: {duracion_ocr_ms} ms")

    return texto_ocr


# ==============================
# METADATOS DE LA API
# ==============================

@app.get("/metadata")
def metadata():
    """Muestra las tecnologías principales utilizadas por ReceiptIA."""
    return {
        "nombre": "ReceiptIA",
        "descripcion": "Sistema inteligente para el análisis de facturas mediante OCR e IA.",
        "version": APP_VERSION,
        "backend": "FastAPI",
        "ocr": "Tesseract OCR",
        "modelo_ia": AI_COMPONENT,
        "modelo_id": AI_MODEL,
        "prompt_version": PROMPT_VERSION,
    }

# ==============================
# RUTA PRINCIPAL INDIVIDUAL
# TESSERACT OCR + GEMINI TEXTO
# ==============================

@app.post("/procesar")
async def procesar(file: UploadFile = File(...)):

    try:
        # ==============================
        # VALIDAR EL ARCHIVO
        # ==============================

        if file.content_type not in [
            "image/jpeg",
            "image/png"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Solo se permiten imágenes JPG o PNG."
            )

        print("====================================")
        print(f"Archivo recibido: {file.filename}")
        print(f"Tipo de archivo: {file.content_type}")

        content = await file.read()

        print(f"Tamaño recibido: {len(content)} bytes")

        # ==============================
        # OCR
        # ==============================

        texto_ocr = extraer_texto_de_archivo(
            file.filename,
            content
        )

        print("Tesseract terminó de leer")
        print(f"Cantidad de caracteres OCR: {len(texto_ocr)}")
        print("Primeros 300 caracteres OCR:")
        print(texto_ocr[:300])

        if not texto_ocr_es_valido(texto_ocr):
            return crear_respuesta_error_ocr(texto_ocr)

        # ==============================
        # GEMINI
        # ==============================

        prompt = crear_prompt_factura_individual(
            texto_ocr
        )

        print("Enviando texto a Gemini...")

        response = generar_con_gemini(prompt)

        print("Gemini respondió")

        # ==============================
        # PROCESAR RESPUESTA
        # ==============================

        resultado = limpiar_json_respuesta(
            response.text
        )

        resultado = normalizar_factura(
            resultado
        )

        resultado["metodo"] = (
            "Tesseract OCR + Gemini texto"
        )

        resultado["texto_ocr"] = texto_ocr

        resultado = (
            corregir_falsos_positivos_factura_consumidor_final(
                resultado
            )
        )

        print(
            "Procesamiento individual "
            "finalizado correctamente"
        )

        return resultado

    # ==============================
    # ERRORES HTTP CONTROLADOS
    # ==============================

    except HTTPException:
        raise

    # ==============================
    # ERRORES GENERALES
    # ==============================

    except Exception as e:

        error_str = str(e)
        error_lower = error_str.lower()

        print(
            f"Error en el servidor: {error_str}"
        )

        # ==============================
        # CUOTA / LIMITE DE GEMINI
        # ==============================

        if (
            getattr(e, "code", None) == 429
            or "resource_exhausted" in error_lower
            or "quota exceeded" in error_lower
            or "too many requests" in error_lower
        ):
            raise HTTPException(
                status_code=429,
                detail=(
                    "El servicio de IA alcanzó "
                    "temporalmente su límite de "
                    "solicitudes. "
                    "Intente nuevamente más tarde."
                )
            )

        # ==============================
        # OTROS ERRORES
        # ==============================

        raise HTTPException(
            status_code=500,
            detail=(
                "Error interno durante el "
                "procesamiento de la factura."
            )
        )

# ==============================
# RUTA POR LOTE
# VARIAS IMÁGENES + UNA SOLICITUD A GEMINI
# ==============================

@app.post(
    "/procesar-lote",
    openapi_extra={
        "requestBody": {
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "required": ["files"],
                        "properties": {
                            "files": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "format": "binary"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
)
async def procesar_lote(
    files: Annotated[List[UploadFile], File(...)]
):
    try:
        print("====================================")
        print(f"Lote recibido con {len(files)} archivo(s)")

        if len(files) == 0:
            return {"error": "No se recibieron archivos."}

        if len(files) > 25:
            return {
                "error": "El backend permite máximo 25 imágenes por lote. En el index.html se deben enviar grupos más pequeños."
            }

        facturas_invalidas = []
        facturas_validas = []

        for index, file in enumerate(files):
            factura_id = f"factura_{index + 1}"
            nombre_archivo = file.filename

            print("------------------------------------")
            print(f"Procesando OCR de {factura_id}: {nombre_archivo}")

            # ==============================
            # VALIDACIÓN DEL TIPO DE ARCHIVO
            # ==============================

            if file.content_type not in [
                "image/jpeg",
                "image/png"
            ]:
                facturas_invalidas.append(
                    crear_respuesta_error_lote(
                        factura_id,
                        nombre_archivo,
                        "",
                        "Formato de imagen no permitido."
                    )
                )
                continue

            try:
                content = await file.read()
                texto_ocr = extraer_texto_de_archivo(nombre_archivo, content)

                print(f"Caracteres OCR de {nombre_archivo}: {len(texto_ocr)}")

                if not texto_ocr_es_valido(texto_ocr):
                    facturas_invalidas.append(
                        crear_respuesta_error_lote(
                            factura_id,
                            nombre_archivo,
                            texto_ocr,
                            "El OCR no logró extraer suficiente texto para analizar esta factura."
                        )
                    )
                    continue

                facturas_validas.append({
                    "factura_id": factura_id,
                    "nombre_archivo": nombre_archivo,
                    "texto_ocr": texto_ocr
                })

            except Exception as e:
                error_str = str(e)
                print(f"Error procesando OCR de {nombre_archivo}: {error_str}")

                facturas_invalidas.append(
                    crear_respuesta_error_lote(
                        factura_id,
                        nombre_archivo,
                        "",
                        f"Error durante el procesamiento OCR: {error_str}"
                    )
                )
                continue

        if len(facturas_validas) == 0:
            return {
                "facturas": facturas_invalidas,
                "metodo": "Tesseract OCR + Gemini texto en lote",
                "cantidad": len(facturas_invalidas)
            }

        # ==============================
        # PREPARAR LOTE PARA GEMINI
        # ==============================

        bloques = []

        for factura in facturas_validas:
            bloque = f"""
==================== INICIO FACTURA ====================
FACTURA_ID: {factura["factura_id"]}
NOMBRE_ARCHIVO: {factura["nombre_archivo"]}

TEXTO_OCR:
{factura["texto_ocr"]}
==================== FIN FACTURA ====================
"""
            bloques.append(bloque)

        bloques_facturas = "\n".join(bloques)

        prompt = crear_prompt_lote(bloques_facturas)

        # ==============================
        # GEMINI
        # ==============================

        print("Enviando lote a Gemini...")

        try:
            response = generar_con_gemini(prompt)
            print("Gemini respondió al lote")

        except Exception as e:
            error_str = str(e)
            error_lower = error_str.lower()

            print("====================================")
            print("ERROR DE GEMINI")
            print(f"Tipo: {type(e).__name__}")
            print(f"Mensaje: {error_str}")
            print("====================================")

            if (
                getattr(e, "code", None) == 429
                or "resource_exhausted" in error_lower
                or "quota exceeded" in error_lower
                or "too many requests" in error_lower
                or "429" in error_lower
            ):
                raise HTTPException(
                    status_code=429,
                    detail=(
                        "El servicio de IA alcanzó temporalmente "
                        "su límite de solicitudes. "
                        "Intente nuevamente más tarde."
                    )
                ) from e

            raise HTTPException(
                status_code=500,
                detail="Error interno durante el procesamiento con Gemini."
            ) from e

        # ==============================
        # PROCESAR RESPUESTA DE GEMINI
        # ==============================

        resultado_lote = limpiar_json_respuesta(response.text)

        facturas_gemini = resultado_lote.get("facturas", [])

        facturas_finales = []

        for factura in facturas_gemini:
            factura = normalizar_factura(factura)
            factura["metodo"] = "Tesseract OCR + Gemini texto en lote"

            texto_original = ""

            for original in facturas_validas:
                if original["factura_id"] == factura.get("factura_id"):
                    texto_original = original["texto_ocr"]
                    break

            factura["texto_ocr"] = texto_original

            factura = corregir_falsos_positivos_factura_consumidor_final(
                factura
            )

            facturas_finales.append(factura)

        # ==============================
        # DETECTAR FACTURAS OMITIDAS
        # ==============================

        ids_devuelto = {
            factura.get("factura_id")
            for factura in facturas_finales
        }

        for original in facturas_validas:
            if original["factura_id"] not in ids_devuelto:
                facturas_finales.append(
                    crear_respuesta_error_lote(
                        original["factura_id"],
                        original["nombre_archivo"],
                        original["texto_ocr"],
                        "Gemini no devolvió resultado para esta factura dentro del lote."
                    )
                )

        facturas_finales.extend(facturas_invalidas)

        print("Procesamiento por lote finalizado correctamente")

        return {
            "facturas": facturas_finales,
            "metodo": "Tesseract OCR + Gemini texto en lote",
            "cantidad": len(facturas_finales)
        }

    except HTTPException:
        raise

    except Exception as e:
        error_str = str(e)

        print("====================================")
        print("ERROR EN PROCESAMIENTO POR LOTE")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {error_str}")
        print("====================================")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from e


# ==============================
# RUTA EXTRA PARA PROBAR SOLO OCR
# ==============================

@app.post("/leer-texto")
async def leer_texto(file: UploadFile = File(...)):
    try:
        content = await file.read()
        texto_ocr = extraer_texto_de_archivo(file.filename, content)

        return {
            "texto_ocr": texto_ocr,
            "metodo": "Solo Tesseract OCR"
        }

    except Exception as e:
        print(f"Error leyendo texto: {e}")
        return {"error": str(e)}