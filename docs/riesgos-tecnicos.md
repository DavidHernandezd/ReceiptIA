# Riesgos Tecnicos y Deuda Tecnica

| Riesgo | Categoria | Probabilidad | Impacto | Mitigacion |
|---------|------------|---------------|----------|------------|
| Dependencia de Tesseract local | Dependencias | Alta | Alto | Dockerizacion |
| Saturacion de la API de Gemini | Servicios Externos | Media | Alto | Reintentos automaticos y modelos alternativos |
| Perdida de conectividad a internet | Infraestructura | Media | Alto | Validaciones y mensajes de error |
| Errores en OCR por imagenes de baja calidad | Datos | Alta | Medio | Preprocesamiento de imagenes |
| Ausencia de pruebas automatizadas | Codigo | Alta | Medio | Implementar pytest |
| Manejo limitado de logs | Observabilidad | Media | Medio | Integracion de logging |
| Configuracion manual de variables de entorno | Configuracion | Media | Bajo | Automatizacion mediante Setup.bat |
| Exposicion accidental de credenciales | Seguridad | Baja | Alto | Uso de .env y .gitignore |