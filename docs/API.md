# API de ReceiptIA

## Información general

**Nombre:** ReceiptIA API

**Versión:** 1.0.0

**Tecnología:** FastAPI

**OCR:** Tesseract OCR

**Modelo IA:** Gemini 2.5 Flash

Herramienta usada para pruebas: Interfaz web local y Swagger UI (FastAPI docs).

---

# Endpoint de salud

## GET /health

Verifica que el servicio se encuentre activo.

### Respuesta

```json
{
    "status":"OK",
    "service":"ReceiptIA",
    "version":"1.0.0"
}
```

---

# Endpoint de metadatos

## GET /metadata

Devuelve información general de la API.

### Respuesta

```json
{
    "nombre":"ReceiptIA",
    "descripcion":"Sistema inteligente para el análisis de facturas mediante OCR e IA.",
    "version":"1.0.0",
    "backend":"FastAPI",
    "ocr":"Tesseract OCR",
    "modelo_ia":"Gemini 2.5 Flash"
}
```

---

# Endpoint principal

## POST /procesar

Analiza una factura utilizando OCR e Inteligencia Artificial.

### Entrada

Tipo:

multipart/form-data

Campo:

```
file
```

Tipos permitidos

- JPG
- PNG

### Respuesta exitosa

Código:

```
200 OK
```

Ejemplo:

```json
{
    "comercio":"Super Selectos",
    "fecha":"2026-07-12",
    "subtotal":20.35,
    "iva":2.65,
    "total":23.00,
    "anomalias":[]
}
```

---

### Errores

#### 400 Bad Request

Cuando el archivo no es una imagen.

```json
{
    "detail":"Solo se permiten imágenes JPG o PNG."
}
```

---

#### 500 Internal Server Error

Cuando ocurre un error interno del servidor.

```json
{
    "detail":"Mensaje del error"
}
```

---

# Endpoint por lote

## POST /procesar-lote

Permite analizar hasta 25 facturas en una sola solicitud.

Entrada:

multipart/form-data

Campo:

```
files
```

Tipos permitidos

- JPG
- PNG

```json
{
    "facturas": [
        {
            "factura_id": "factura_1",
            "nombre_archivo": "ticket1.jpg",
            "comercio": "Farmacia",
            "total": 15.50,
            "tiene_anomalias": false,
            "anomalias": []
        }
    ],
    "metodo": "Tesseract OCR + Gemini texto en lote",
    "cantidad": 1
}
```
---

# Endpoint OCR

## POST /leer-texto

Extrae únicamente el texto utilizando Tesseract OCR.

No realiza análisis mediante IA.

Entrada
Tipo: multipart/form-data

Campo: file

```json
{
    "texto_ocr": "Texto crudo extraído de la imagen...",
    "metodo": "Solo Tesseract OCR"
}
```