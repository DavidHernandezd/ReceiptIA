# Plan de Contingencia de Demostración - ReceiptIA

## Objetivo

Definir acciones de prevención y respuesta ante fallas durante la demostración pública de ReceiptIA.

## Servicios involucrados

- Frontend: Railway + Nginx
- Backend: Railway + FastAPI
- OCR: Tesseract OCR
- IA: Gemini 2.5 Flash
- Autenticación: Firebase Authentication
- Persistencia: Firebase Firestore

## Riesgos y respuesta

| Riesgo | Prevención | Respuesta preparada |
|---|---|---|
| Servicio Railway detenido o lento | Abrir frontend y backend 15 minutos antes | Verificar `/health`, esperar reinicio y reintentar |
| Cuota de Gemini agotada | Revisar cuota antes de la exposición y limitar pruebas innecesarias | Mostrar el error HTTP 429 controlado y explicar la dependencia externa |
| Gemini lento | Evitar múltiples solicitudes previas a la demo | Esperar el timeout configurado y mostrar mensaje controlado |
| Error del frontend | Probar el flujo completo antes de iniciar | Recargar la aplicación y volver a iniciar sesión |
| Sesión Firebase vencida | Iniciar sesión antes de la exposición | Volver a autenticar con la cuenta de demostración |
| Problema de Firestore | Verificar previamente historial y sesión | Demostrar el procesamiento sin depender de datos históricos |
| Configuración CORS | Probar producción después de cada despliegue | Volver al último commit estable |
| Fallo de red | Probar red y navegador antes de iniciar | Utilizar una segunda red o hotspot disponible |
| Problema de navegador | Tener ventana privada preparada | Cambiar de navegador o dispositivo |
| Problema de audio/pantalla | Probar presentación y pantalla previamente | Utilizar copia local de la presentación |
| Release incorrecto | Congelar el commit final antes de la evaluación | Volver al tag estable mediante rollback |
| Datos sensibles | Usar únicamente facturas ficticias o autorizadas | Detener la visualización si aparece información no autorizada |

## Preparación 24 horas antes

- Congelar la versión candidata.
- Ejecutar pruebas automatizadas.
- Revisar GitHub Actions.
- Probar frontend público.
- Probar backend público.
- Verificar `/health`.
- Verificar `/metadata`.
- Probar una factura ficticia.
- Revisar secretos y datos personales.
- Preparar capturas o video de respaldo.

## Preparación 15 minutos antes

- Abrir el frontend público.
- Iniciar sesión.
- Abrir `/health`.
- Abrir `/metadata`.
- Tener una factura ficticia lista.
- Cerrar notificaciones.
- Abrir la presentación.
- Preparar red alternativa.

## Flujo alternativo ante cuota 429

ReceiptIA maneja explícitamente la respuesta HTTP 429 cuando Gemini alcanza su límite de cuota.

Durante la demostración, si ocurre este caso:

1. Mostrar el mensaje controlado al usuario.
2. Explicar que Tesseract y el backend sí procesaron la solicitud.
3. Mostrar `/health` para verificar que el backend sigue operativo.
4. Mostrar `/metadata` para identificar la versión desplegada.
5. Utilizar evidencia de respaldo si el docente lo autoriza.

## Datos de demostración

Se utilizarán únicamente facturas ficticias o documentos autorizados.

No se mostrarán:

- API Keys.
- Tokens.
- Credenciales.
- Datos personales no autorizados.
- Logs con contenido OCR sensible.

## Responsable de contingencia

Durante la exposición, un integrante será responsable de:

- Supervisar Railway.
- Revisar `/health`.
- Verificar cuota.
- Ejecutar rollback si fuera necesario.
- Abrir evidencia de respaldo.

## Estado

Documento provisional. Se actualizará al congelar el release final.
