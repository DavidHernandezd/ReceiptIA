# Registro de errores, riesgos y correcciones de ReceiptIA

## 1. El backend requería la API Key al importar main.py

### Problema

El cliente de Gemini se creaba inmediatamente al importar el archivo
`main.py`. Esto impedía ejecutar pruebas automáticas cuando no existía
un archivo `.env` con una clave real.

### Riesgo

La clave podía terminar guardándose dentro de GitHub Actions o dentro
del repositorio.

### Corrección

Se creó la función `obtener_cliente_gemini()`. Ahora el cliente de
Gemini solamente se crea cuando se ejecuta una operación que realmente
necesita inteligencia artificial.

---

## 2. No existía un endpoint de verificación

### Problema

El backend no tenía una ruta simple para comprobar si el servicio estaba
disponible.

### Corrección

Se agregó el endpoint `GET /health`, que responde con el estado del
backend.

---

## 3. Las pruebas no deben depender de Gemini

### Problema

Una prueba real contra Gemini puede variar, consumir solicitudes o fallar
por problemas de conexión.

### Corrección

Las pruebas verifican funciones internas, validación del OCR, estructura
de las facturas y endpoints que no consumen Gemini.

---

## 4. Las pruebas no deben depender de una imagen real

### Problema

Procesar imágenes dentro de GitHub Actions requeriría configurar
Tesseract, idiomas OCR y archivos de prueba.

### Corrección

Las pruebas mínimas verifican la validación del texto OCR y la
normalización de resultados sin procesar imágenes reales.

---

## 5. Variables sensibles

### Problema

El archivo `.env` contiene información privada.

### Corrección

Se agregó `.env` al `.gitignore` y se creó `.env.example` con valores
de ejemplo.

---

## 6. Variable de excepción fuera de alcance

### Problema

GitHub Actions falló durante la revisión con Ruff y mostró el error:

```text
F821 Undefined name `e`