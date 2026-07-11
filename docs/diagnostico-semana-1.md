# Diagnostico Tecnico - Semana 1

## Cual es el estado actual del proyecto

ReceiptIA es un prototipo funcional enfocado a la digitalizacion y analisis inteligente de facturas y tickets de compra. El sistema permite la carga individual y por lotes de imagenes, se hace un reconocimiento de caracteres (OCR) mediante Tesseract y utiliza Gemini 2.5 Flash para estructurar la información extraida.

La aplicacion cuenta con autenticacion basada en Firebase y un Dashboard para la visualización y gestion del historial de facturas procesadas.

---

## Que partes funcionan actualmente.

- Autenticacion y gestion de sesiones mediante Firebase Authentication.
- Carga individual y multiple de facturas.
- Extracción de texto mediante Tesseract OCR.
- Procesamiento inteligente de información utilizando Gemini 2.5 Flash.
- Dashboard con visualizacion de resultados.
- Historial de facturas procesadas.
- Exportación de resultados.
- Automatización de instalación mediante el archivo Setup.bat.

---

## Que partes son manuales, incompletas o fragiles.

- Dependencia de instalación local de Tesseract OCR.
- Ausencia de pruebas automatizadas.
- Escasa instrumentación de logs y métricas.
- Falta de contenedorización y despliegue automatizado.
- Manejo limitado de errores de conectividad con Gemini.

---

## Que dependencias tecnicas tiene.

- Python 3.10+
- FastAPI
- Uvicorn
- Pytesseract
- OpenCV
- Pillow
- Google GenAI SDK
- Firebase Authentication
- Firebase Firestore

---

## Que datos, archivos, servicios o credenciales necesita

- Archivo ".env"
- Clave "GEMINI_API_KEY"
- Instalación de Tesseract OCR
- Conexión a Firebase

---

## Como se ejecuta actualmente

1. Ejecutar `Setup.bat`.
2. Configurar la API Key de Gemini.
3. Ejecutar `ReceiptIA.bat`.

---

## Que evidencia existe de que el prototipo funciona.

- Procesamiento exitoso de facturas individuales.
- Procesamiento por lotes.
- Historial persistente en Firebase.
- Dashboard funcional.
- Exportación de datos.