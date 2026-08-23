# Pruebas de Humo - ReceiptIA

## Objetivo

Verificar rápidamente que los componentes críticos de ReceiptIA funcionan correctamente después de un despliegue, cambio de versión o rollback.

## Entorno evaluado

- Frontend: Railway
- Backend: Railway
- OCR: Tesseract OCR
- IA: Gemini 2.5 Flash
- Autenticación: Firebase Authentication
- Persistencia: Firebase Firestore
- Versión de aplicación: 1.0.0
- Prompt version: 1.0

## URLs verificadas

- Frontend: https://receiptia-production-c5cc.up.railway.app
- Backend: https://receiptia-production.up.railway.app
- Health: https://receiptia-production.up.railway.app/health
- Metadata: https://receiptia-production.up.railway.app/metadata
- Swagger: https://receiptia-production.up.railway.app/docs

## Casos de prueba

| ID | Prueba | Resultado esperado |
|---|---|---|
| ST-01 | Abrir frontend público | La aplicación carga correctamente |
| ST-02 | GET `/health` | HTTP 200 y servicio disponible |
| ST-03 | GET `/metadata` | Devuelve versión, modelo y prompt |
| ST-04 | Abrir Swagger `/docs` | La documentación de la API carga correctamente |
| ST-05 | Iniciar sesión | Firebase Authentication permite el acceso |
| ST-06 | Cargar una factura ficticia o autorizada | El archivo es recibido por el sistema |
| ST-07 | Ejecutar OCR | Tesseract extrae información del documento |
| ST-08 | Ejecutar análisis de IA | Gemini devuelve un resultado estructurado |
| ST-09 | Manejo de cuota | Un HTTP 429 se presenta como error controlado |
| ST-10 | Procesamiento por lote | `/procesar-lote` responde correctamente |
| ST-11 | Comunicación CORS | El frontend público puede llamar al backend |
| ST-12 | Logs seguros | No aparecen API Keys ni fragmentos OCR sensibles |

## Registro de ejecución

| ID | Estado | Evidencia / observación |
|---|---|---|
| ST-01 | OK | Frontend público cargó correctamente en ventana privada |
| ST-02 | OK | `/health` respondió correctamente y el backend se encontró disponible |
| ST-03 | OK | `/metadata` mostró versión 1.0.0, modelo `gemini-2.5-flash` y prompt 1.0 |
| ST-04 | OK | Swagger `/docs` cargó correctamente |
| ST-05 | OK | Inicio de sesión exitoso con cuenta de demostración |
| ST-06 | OK | Factura ficticia o autorizada cargada correctamente |
| ST-07 | OK | Tesseract OCR extrajo información del documento |
| ST-08 | OK | Gemini devolvió una respuesta estructurada |
| ST-09 | OK / No reproducido | El manejo de HTTP 429 está implementado y fue observado previamente; no se reprodujo durante esta ejecución final |
| ST-10 | OK | Procesamiento por lote ejecutado correctamente |
| ST-11 | OK | El frontend público se comunicó correctamente con el backend sin errores CORS |
| ST-12 | OK | Logs revisados sin API Keys ni fragmentos OCR sensibles; se mantienen datos operativos de observabilidad |

## Verificación de metadata

Durante la prueba ST-03, el endpoint `/metadata` devolvió información coherente con la versión candidata:

{
  "nombre": "ReceiptIA",
  "descripcion": "Sistema inteligente para el análisis de facturas mediante OCR e IA.",
  "version": "1.0.0",
  "backend": "FastAPI",
  "ocr": "Tesseract OCR",
  "modelo_ia": "Gemini 2.5 Flash",
  "modelo_id": "gemini-2.5-flash",
  "prompt_version": "1.0"
}

Criterio de aceptación

El release candidato puede considerarse apto para demostración cuando:

El frontend carga correctamente.
/health responde correctamente.
/metadata reporta la versión esperada.
Swagger se encuentra disponible.
El usuario puede autenticarse.
El flujo crítico de procesamiento funciona con datos ficticios o autorizados.
OCR extrae información del documento.
Gemini devuelve resultados estructurados cuando existe disponibilidad de cuota.
El procesamiento por lote funciona correctamente.
El frontend se comunica con el backend sin errores CORS.
Los logs no exponen secretos ni contenido OCR sensible.
Los errores asociados a servicios externos se presentan de forma controlada.
Limitaciones observadas

ReceiptIA depende de servicios externos, por lo que una prueba exitosa no garantiza disponibilidad permanente.

Entre las principales limitaciones se encuentran:

La cuota de Gemini puede producir respuestas HTTP 429.
La disponibilidad de Railway puede afectar el frontend o backend.
Firebase Authentication y Firestore dependen de servicios externos.
La calidad del OCR depende de la legibilidad y calidad de las imágenes.
Los resultados generados por inteligencia artificial requieren revisión humana cuando exista duda.
Resultado general

Las pruebas de humo ejecutadas sobre el entorno público verificaron correctamente los componentes principales de ReceiptIA.

Los flujos de autenticación, procesamiento individual, OCR, análisis mediante Gemini, procesamiento por lote, comunicación frontend-backend y observabilidad funcionaron correctamente durante la ejecución final.

El caso ST-09 no fue reproducido durante esta ronda de pruebas. Sin embargo, el manejo del error HTTP 429 se encuentra implementado y este tipo de respuesta fue observado previamente durante pruebas de rendimiento.

Estado

Pruebas de humo ejecutadas sobre el entorno público de ReceiptIA.

Estado general: APROBADO PARA DEMOSTRACIÓN, sujeto a la disponibilidad de los servicios externos utilizados por la aplicación.
