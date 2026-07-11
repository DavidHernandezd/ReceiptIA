# Arquitectura Actual

## Usuario o actor principal.

- Contadores.
- Empresas pequeñas y medianas.
- Usuarios que requieren digitalizar comprobantes fiscales.

---

## Interfaz o punto de entrada

Frontend Web desarrollado con HTML, CSS y JavaScript.

---

## Backend, script, notebook o servicio actual.

- FastAPI.
- Uvicorn.
- Endpoints REST para procesamiento de imágenes y extracción de información.

---

## Componente de IA

- Google Gemini 2.5 Flash.
- Clasificación y estructuración de datos extraídos del OCR.

---

## Datos utilizados

- Imágenes JPG y PNG.
- Datos estructurados en formato JSON.
- Información almacenada en Firebase.

---

## Servicios externos, si aplica.

- Firebase Authentication.
- Firebase Firestore.
- Google Gemini API.

---

## Flujo basico de informacion.

Usuario > Frontend > Backend > OCR > Gemini > Backend > Firebase > Dashboard

---

## Dependencias manuales o puntos fragiles

- Instalación de Tesseract.
- Configuración de variables de entorno.
- Dependencia de conectividad con Gemini.