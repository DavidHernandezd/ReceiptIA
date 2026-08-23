# Procedimiento de Rollback - ReceiptIA

## Objetivo

Definir un procedimiento para regresar ReceiptIA a una versión estable si el release presentado produce una falla crítica.

## Cuándo aplicar rollback

Se aplicará rollback si ocurre alguno de los siguientes casos:

- El frontend público deja de cargar.
- El backend no responde correctamente en `/health`.
- `/metadata` muestra una versión incorrecta.
- El frontend no logra comunicarse con el backend.
- Se presenta un error de CORS después de un despliegue.
- El flujo crítico de procesamiento deja de funcionar.
- Se despliega un commit diferente al release evaluado.
- Se detecta una regresión grave en producción.

## Versión estable

Antes de la evaluación se registrarán:

- Commit estable.
- Tag del release.
- Versión de la aplicación.
- URL del frontend.
- URL del backend.

Estos valores se completarán al congelar el release final.

## Procedimiento de rollback

1. Identificar el último commit o tag estable.
2. Confirmar que dicho commit corresponde a una versión previamente verificada.
3. Seleccionar en Railway el deployment correspondiente al commit estable o redeplegar esa versión.
4. Esperar a que el deployment finalice correctamente.
5. Verificar el backend mediante:
   - `/health`
   - `/metadata`
6. Confirmar que `/metadata` muestra la versión esperada.
7. Abrir el frontend público.
8. Iniciar sesión con la cuenta de demostración.
9. Ejecutar el flujo crítico con una factura ficticia o autorizada.
10. Verificar que el frontend reciba correctamente la respuesta del backend.
11. Registrar el incidente y conservar evidencia del rollback.

## Verificación posterior

El rollback se considera exitoso cuando:

- El frontend carga correctamente.
- `/health` responde HTTP 200.
- `/metadata` muestra la versión esperada.
- El frontend puede comunicarse con el backend.
- El flujo crítico puede ejecutarse.
- No existen errores de CORS.
- No se exponen secretos o datos personales.

## Limitaciones

El rollback restaura el código desplegado, pero no corrige fallas externas.

Por ejemplo:

- Una cuota agotada de Gemini puede seguir causando HTTP 429.
- Una indisponibilidad de Firebase no se soluciona mediante rollback.
- Una falla general de Railway puede impedir temporalmente el redeploy.

## Estado

Procedimiento provisional. Se completará con el commit y tag exactos del release final.
