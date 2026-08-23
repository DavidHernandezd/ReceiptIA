# Pruebas de Humo - ReceiptIA

## Objetivo

Verificar rápidamente que los componentes críticos de ReceiptIA funcionan después de un despliegue, cambio de versión o rollback.

## Entorno evaluado

- Frontend: Railway
- Backend: Railway
- OCR: Tesseract OCR
- IA: Gemini 2.5 Flash
- Autenticación: Firebase Authentication
- Persistencia: Firebase Firestore

## Casos de prueba

| ID | Prueba | Resultado esperado |
|---|---|---|
| ST-01 | Abrir frontend público | La aplicación carga correctamente |
| ST-02 | GET `/health` | HTTP 200 y `status: ok` |
| ST-03 | GET `/metadata` | Devuelve versión, modelo y prompt |
| ST-04 | Abrir Swagger `/docs` | La documentación de la API carga correctamente |
| ST-05 | Iniciar sesión | Firebase Authentication permite el acceso |
| ST-06 | Cargar una factura ficticia | El archivo es recibido por el sistema |
| ST-07 | Ejecutar OCR | Tesseract extrae texto de la imagen |
| ST-08 | Ejecutar análisis de IA | Gemini devuelve un resultado estructurado si existe cuota |
| ST-09 | Manejo de cuota | Un HTTP 429 se presenta como error controlado |
| ST-10 | Procesamiento por lote | `/procesar-lote` responde correctamente |
| ST-11 | Comunicación CORS | El frontend público puede llamar al backend |
| ST-12 | Logs seguros | No aparecen API Keys ni fragmentos OCR sensibles |

## Registro de ejecución

| ID | Estado | Evidencia / observación |
|---|---|---|
| ST-01 | Pendiente | |
| ST-02 | Pendiente | |
| ST-03 | Pendiente | |
| ST-04 | Pendiente | |
| ST-05 | Pendiente | |
| ST-06 | Pendiente | |
| ST-07 | Pendiente | |
| ST-08 | Pendiente | |
| ST-09 | Pendiente | |
| ST-10 | Pendiente | |
| ST-11 | Pendiente | |
| ST-12 | Pendiente | |

## Criterio de aceptación

El release candidato puede considerarse apto para demostración cuando:

- El frontend carga correctamente.
- `/health` responde HTTP 200.
- `/metadata` reporta la versión esperada.
- El flujo crítico funciona con datos ficticios o autorizados.
- Los errores externos se presentan de forma controlada.
- No se exponen secretos ni información sensible.

## Estado

Documento provisional. Los resultados se completarán después de ejecutar las pruebas sobre el commit candidato a release final.
