# ReceiptIA

> Sistema inteligente para análisis, validación y organización de facturas con IA

## 1. Información General

**Módulo:** Desarrollo de Aplicaciones con IA  
**Semana:** Semana 5 – Observabilidad, Rendimiento y Escalabilidad
**Nombre del proyecto:** ReceiptIA  
**Integrantes:**  
- Jonathan Elias Gamez Larin  
- Wilber José Jiménez Ramírez  
- David Arnoldo Hernández Gómez  

---

## 2. Descripción del Problema

**Preguntas guía:**  
- ¿Qué problema real se quiere resolver?  
- ¿A quién afecta este problema?  
- ¿En qué contexto ocurre?  
- ¿Por qué una solución con IA puede aportar valor?  

**Descripción:**  
Muchas empresas, negocios y auditores deben revisar grandes cantidades de facturas de forma manual, lo que puede generar pérdida de tiempo, errores de digitación, dificultad para organizar documentos y problemas al detectar inconsistencias fiscales o numéricas.

ReceiptIA surge como una solución para automatizar parte de este proceso mediante inteligencia artificial. El sistema permite cargar facturas o recibos, extraer la información principal, detectar posibles anomalías y organizar los resultados en un historial digital. Esto facilita la revisión, clasificación y exportación de datos para procesos administrativos o de auditoría.

---

## 3. Usuarios o Beneficiarios


| Usuario / Beneficiario | Necesidad principal | Cómo ayuda la aplicación |
|---|---|---|
| Auditor | Revisar varias facturas de forma rápida y ordenada | Analiza documentos, detecta anomalías y permite exportar resultados |
| Administrador de negocio | Controlar facturas, recibos y registros de compras o ventas | Organiza documentos en historial y carpetas por cliente o categoría |
| Empresa o institución | Reducir errores manuales en la revisión documental | Automatiza extracción de datos y apoya la validación de información |
| Usuario general | Digitalizar y revisar facturas de manera sencilla | Permite subir imágenes y obtener datos estructurados automáticamente |

---

## 4. Descripción de la Solución

**Descripción:**  
ReceiptIA es una aplicación web que permite cargar imágenes de facturas o recibos para analizarlas mediante OCR e inteligencia artificial. El sistema convierte la imagen en texto, interpreta la información extraída y devuelve un resultado estructurado con los datos principales del documento.

**Entrada:**  
Imágenes de facturas, recibos o documentos tributarios.

**Resultado:**  
Datos estructurados como comercio, NIT, fecha, productos o servicios, subtotal, IVA, total, estado de revisión y posibles anomalías detectadas.

**Qué automatiza:**  
- Lectura de facturas mediante OCR.
- Extracción de datos importantes.
- Análisis de posibles inconsistencias.
- Clasificación de documentos como procesados o por revisar.
- Guardado de resultados en historial.
- Organización por carpetas.
- Exportación de información a Excel.

---

## 5. Componente de Inteligencia Artificial

| Elemento | Descripción |
|---|---|
| Tipo de IA utilizada | OCR + modelo generativo de lenguaje |
| Modelo, servicio o técnica | Tesseract OCR para lectura de texto y Gemini 2.5 Flash para interpretación y análisis |
| Datos de entrada | Imagen de factura, texto extraído por OCR y reglas de validación fiscal |
| Resultado generado por la IA | Información estructurada, detección de anomalías y clasificación del documento |
| Forma de evaluación | Comparación entre la factura original, el texto OCR y los resultados mostrados en el Dashboard |
| Limitaciones actuales | La calidad de la imagen puede afectar el OCR; Gemini depende de conexión a internet y API Key válida |

**Explicación breve:**  
La inteligencia artificial participa después de extraer el texto de la factura. Primero, Tesseract OCR convierte la imagen en texto. Luego, Gemini interpreta ese texto, identifica los datos importantes, revisa montos y detecta posibles inconsistencias. El resultado se muestra en el Dashboard para que el usuario pueda revisarlo antes de exportarlo.

---

## 6. Estado Actual del Proyecto *ACTUALIZADO 

### Funcionalidades que ya funcionan

- Carga de facturas desde la interfaz web.
- Procesamiento individual y por lote.
- Extracción de texto con Tesseract OCR.
- Análisis de facturas con Gemini.
- Detección de posibles anomalías fiscales o numéricas.
- Visualización de resultados en Dashboard.
- Registro de facturas en historial.
- Creación de carpetas para organizar facturas.
- Selección de facturas para exportación.
- Exportación de datos a Excel.
- Autenticación de usuarios con Firebase.
- Roles básicos de administrador y auditor.

# *semana 2*
- API REST estructurada con FastAPI.
- Contratos estrictos de entrada y salida utilizando Pydantic para validacion de datos.
- Endpoints de monitoreo y procesamiento completamente documentados.

# *semana 3*
- Pruebas automatizadas implementadas con Pytest, cobertura de endpoints y logica interna
- Analisis de codigo estatico integrado con Ruff
- Pipeline de Integracion Continua configurado en GitHub Actions.

# *semana 4*
- Dockerfile implementado.
- Contenedor Docker funcional.
- .dockerignore agregado.
- Variables documentadas mediante .env.example.
- Backend ejecutándose mediante Docker.
- Endpoint /health verificado.
- Endpoint principal probado desde Swagger.

# *semana 5*

- Middleware HTTP de observabilidad implementado en FastAPI.
- Generación de request_id único para correlacionar cada solicitud.
- Registro estructurado de ruta, método, estado HTTP, duración, modelo de IA y tipo de error.
- Registro de eventos exitosos y errores controlados sin almacenar el contenido sensible de las facturas.
- Validación de entradas inválidas mediante respuestas HTTP 400.
- Manejo y registro de errores internos mediante HTTP 500.
- Manejo explícito de límites temporales de la API de Gemini mediante HTTP 429.
- Benchmark del endpoint /procesar realizado con 20 solicitudes.
- Línea base obtenida: 16 solicitudes exitosas y 4 errores, con una tasa de error del 20 %.
- Identificación de la dependencia de Gemini y sus límites de cuota como restricción de rendimiento y disponibilidad.


### Funcionalidades incompletas o pendientes

- Mejorar manejo de errores cuando el backend no está activo.
- Agregar almacenamiento de imágenes en la nube en una etapa futura.
- Mejorar la precisión del OCR con imágenes borrosas.
- Documentar mejor la instalación en otra computadora.
- Ajustar reglas de validación para reducir falsos positivos.
- Fortalecer reglas de seguridad en Firebase.

### Observabilidad y medición de rendimiento

Se incorporo una capa mínima de observabilidad al Backend mediante un middleware HTTP.
Cada solicitud recibe un request_id único y se registra información operacional para correlacionar las peticiones y analizar su comportamiento.

CAMPOS REGISTRADOS

| campo | Descripcion | 
|---|---|
| request_id | Identificador único de la solicitud |
| route | Ruta o endpoint ejecutado |
| method | Método HTTP utilizado |
| status | Código de respuesta HTTP |
| duration_ms | Duración total de la solicitud en milisegundos |
| ai_model | Modelo de IA utilizado, actualmente Gemini 2.5 Flash |
| error_type | Clasificación del error cuando ocurre una falla |

LINEA BASE DE RENDIMIENTO

El endpoint crítico seleccionado fue POST /procesar. Se ejecutó un benchmark de 20 solicitudes utilizando una imagen de factura como entrada.

| Metrica | Resultado |
|---|---|
| solicitudes totales |20|
| solicitudes exitosas |16|
| errores |4|
| tasa de error |20.00%|
| p50 |10682.07 ms|
| p95 |13712.31 ms|
| tiempo maximo |17725.83 ms|

Se identifico que el procesamiento depende fuertemente del tiempo de respuesta del servicio de Gemini. Durante las pruebas también se observaron respuestas HTTP 429 (RESOURCE_EXHAUSTED) debido al límite de solicitudes del nivel gratuito de la API. Esto constituye una restricción externa relevante para la disponibilidad y escalabilidad del endpoint.

Evidencias generadas

benchmark_resultados.csv: resultados individuales de las solicitudes realizadas.
benchmark_resumen.txt: resumen de las métricas obtenidas.
Logs del Backend con request_id, ruta, estado, duración, modelo y tipo de error.
Evidencias de Swagger para solicitudes exitosas, entradas inválidas y errores controlados.


---

## 7. Inventario Técnico

| Componente | Descripción | Estado actual |
|---|---|---|
| Interfaz web | Pantallas en HTML, Tailwind CSS y JavaScript para carga, análisis, historial y exportación | Implementado |
| Backend | API desarrollada con FastAPI para recibir imágenes y procesarlas | Implementado |
| OCR | Tesseract OCR para convertir imágenes de facturas en texto | Implementado |
| IA generativa | Gemini 2.5 Flash para analizar el texto extraído y detectar anomalías | Implementado |
| Base de datos | Firestore para guardar usuarios, facturas, historial y carpetas | Implementado |
| Autenticación | Firebase Authentication para inicio de sesión y manejo de usuarios | Implementado |
| Roles | Administrador y auditor | Implementado |
| Exportación | SheetJS/XLSX para generar archivos de Excel | Implementado |
| Dependencias | FastAPI, Uvicorn, Google GenAI, Pillow, Pytesseract, OpenCV, NumPy y Python Multipart | Configuradas |
| Configuración | API Key de Gemini, configuración de Firebase y ruta local de Tesseract OCR | Configurada |

## 8. Arquitectura Objetivo

La arquitectura objetivo busca la separación entre interfaz, backend, inteligencia artificial, datos y configuración. El sistema evolucionará hacia una arquitectura desacoplada basada en una API REST stateless, permitiendo su despliegue en diferentes entornos y reduciendo las dependencias del sistema operativo del usuario.


**Archivo sugerido:** `docs/arquitectura-objetivo.md` o `docs/arquitectura-objetivo.png`

**Elementos esperados:**

- **API o endpoint inteligente:** Implementación de modelos Pydantic en FastAPI para establecer contratos estrictos de entrada y salida y mejorar la validación de datos.
- **Separación entre interfaz, backend, IA y datos:** Frontend desacoplado del Backend, FastAPI como servicio independiente, Firebase como fuente de autenticación y persistencia, y abstracción de los componentes de OCR e IA.
- **Pruebas mínimas:** Integración de pytest para validar funciones críticas de extracción, procesamiento y clasificación de datos.
- **Variables de entorno:** Centralización de la configuración mediante archivos `.env` y `.env.example`, evitando la exposición de credenciales y facilitando la portabilidad del proyecto.
- **Contenedor o estrategia de despliegue:** Implementación de un Dockerfile que incluya las dependencias del sistema, incluyendo Tesseract OCR, permitiendo el despliegue en plataformas PaaS o entornos Linux.
- **Logs, métricas o evidencia operacional:** Incorporación de logging en el Backend para registrar errores, tiempos de respuesta y trazabilidad del procesamiento de facturas.
- **Consideraciones de seguridad:** Refuerzo de las reglas de seguridad de Firebase, protección de las API Keys mediante variables de entorno y control de acceso basado en autenticación.

**Diagrama:**

<img width="178" height="591" alt="Captura de pantalla 2026-07-11 154722" src="https://github.com/user-attachments/assets/71c22e17-5653-440c-bb12-98d6cfbddf5e" />



---

## 9. Estructura del Repositorio *ACTUALIZADO

```text
ReceiptIA/
|
|-- .github/workflows/   # Pipeline de CI/CD 
|
|-- Backend/             # Logica del servidor FastAPI, OCR y conexion con Gemini
|   ├── main.py
|   ├── requirements.txt
|   ├── .env.example
|   ├── pyproject.toml
|   ├── requirements-dev.txt
|   ├── test/
|   └── ...
|
|-- Frontend/            # Interfaz web, autenticacion y Dashboard
|   ├── index.html
|   ├── Dashboard.html
|   ├── Historial.html
|   └── ...
|
|-- docs/                # Documentacion tecnica y arquitecturas
|   ├── api.md
|   ├── evidencias API.pdf
|   ├── arquitectura-actual.md
|   ├── arquitectura-objetivo.md
|   ├── diagnostico-semana-1.md
|   ├── plan-mejora.md
|   ├── riesgos-tecnicos.md
|   ├── REGISTRO_ERRORES.md
|   ├── Evidencias_Testing.pdf
|   ├── benchmark_resultados.csv
|   ├── benchmark_resumen.txt
|   ├── Semana5_Observabilidad_Rendimiento_ReceiptIA.pdf
|
|-- Setup.bat            # Configuracion inicial del proyecto
|-- benchmark.py
|-- ReceiptIA.bat        # Inicio automatico del sistema
|-- README.md            # Documentacion principal
|-- .gitignore           # Exclusion de archivos sensibles
```

**Notas sobre la estructura:El proyecto adopta una arquitectura cliente-servidor claramente desacoplada. La carpeta Frontend contiene la interfaz web, autenticación y visualización de resultados, mientras que Backend actúa como intermediario entre la aplicación, el motor OCR y el modelo de inteligencia artificial.

Los scripts Setup.bat y ReceiptIA.bat permiten automatizar la instalación de dependencias y la ejecución del sistema, reduciendo la configuración manual requerida por el usuario.**

---

## 10. Instalación y Ejecución

### Requisitos previos

Python: Versión 3.10 o superior.
Gestor de paquetes: pip.
Otros requisitos:
Conexion a Internet para consumir la API de Gemini.
Sistema operativo Windows (el proyecto incluye scripts .bat para automatizar la instalacion y ejecucion).
API Key de Google Gemini.
Tesseract OCR (el proyecto puede instalarlo automáticamente mediante Setup.bat).

### Instalación

# De forma automatica

# Descargar o clonar el repositorio
git clone <url-del-repositorio>

# Ejecutar el instalador automático
Setup.bat

# De forma manual

cd Backend

python -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt


# Despliegue con Docker

### Construir la imagen

```bash
docker build -t receiptia .
```

### Ejecutar el contenedor

```bash
docker run -p 8000:8000 receiptia
```

### Verificar funcionamiento

Health:

```
http://localhost:8000/health
```

Swagger:

```
http://localhost:8000/docs
```

Endpoint principal:

```
POST /procesar
```

### Ejecución

# Ejecucion Manual Backend

.\venv\Scripts\python.exe -m uvicorn main:app --reload

cd Frontend

python -m http.server 5501

http://127.0.0.1:5501

### Variables de entorno

El proyecto utiliza un archivo .env ubicado en la carpeta Backend/.

| Variable | Descripción | Obligatoria |
|---|---|---|
| GEMINI_API_KEY | Clave de acceso a la API de Google Gemini | Sí |
| GEMINI_MODEL | Modelo principal utilizado para el procesamiento | No |
| GEMINI_FALLBACK_MODEL | Modelo alternativo en caso de saturación del principal | No |
| TESSERACT_CMD | Ruta manual del ejecutable de Tesseract OCR | No |

## 11. API REST

La funcionalidad inteligente de ReceiptIA se encuentra expuesta mediante FastAPI.

### Endpoints disponibles

| Método | Endpoint | Descripción |
|---------|----------|-------------|
| GET | /health | Estado del servicio |
| GET | /metadata | Información general de la API |
| POST | /procesar | Procesa una factura individual |
| POST | /procesar-lote | Procesa múltiples facturas |
| POST | /leer-texto | Extrae únicamente el texto OCR |

## 12. Pruebas Automatizadas y CI/CD 

El proyecto cuenta con un conjunto de pruebas automatizadas y un pipeline de Integracion Continua mediante GitHub Actions.

### Ejecución de pruebas locales
Para ejecutar las pruebas se debe de estar dentro del entorno virtual y tener instaladas las dependencias de desarrollo.

1. Instalar requerimientos de desarrollo:
   ```bash
   python -m pip install -r Backend/requirements-dev.txt

2. analisis estatico con Ruff:
cd Backend
python -m ruff check .

3. pruebas con Pytest:
cd Backend
python -m pytest -v

## 13. Datos Utilizados

| Fuente de datos | Tipo de datos | Uso dentro del proyecto | Observaciones |
|---|---|---|---|
| Usuario | Imágenes JPG y PNG | Facturas y tickets de compra para análisis OCR | Principal fuente de información |
| Firebase Authentication | JSON / Tokens | Gestión de autenticación y sesiones | Información de usuarios autenticados |
| Gemini API | JSON | Estructuración y clasificación de datos extraídos | Respuesta generada por IA |
| Firebase Firestore | Documentos JSON | Almacenamiento de resultados e historial | Persistencia de información procesada |

**Consideraciones**
Los datos son privados, ya que corresponden a comprobantes fiscales proporcionados por el usuario.
Las imágenes pueden contener información sensible como:
-Nombres.
-Direcciones.
-Números de identificación tributaria.
-Montos de compra.

Las imágenes requieren procesos de validación y limpieza antes de ser analizadas.
La precisión del OCR depende de:
-Calidad de la imagen.
-Iluminación.
-Resolución.
-Legibilidad del documento.

---

## 14. Riesgos Técnicos y Deuda Técnica

| Riesgo | Categoría | Probabilidad | Impacto | Mitigación propuesta |
|---|---|---|---|---|
|  | Datos / Modelo / Código / Seguridad / Despliegue | Baja / Media / Alta | Bajo / Medio / Alto |  
| Dependencia de Tesseract OCR instalado localmente | Dependencias | Alta | Alto | Automatizar instalación mediante Setup.bat y Docker
| Saturación o indisponibilidad temporal de Gemini | Servicios Externos | Media | Alto | Implementar reintentos automáticos y modelos alternativos |
| Dependencia de conexión a Internet | Infraestructura | Media | Alto | Validaciones y manejo de errores |
| Límites de cuota de Gemini | Servicios Externos | Alta | Alto | Manejo de HTTP 429, reintentos controlados, modelos alternativos y futura estrategia de colas/workers |

## 15. Plan de Mejora por Semana

| Semana | Mejora esperada | Evidencia esperada |
|---|---|---|
| Semana 2 | Implementación de modelos Pydantic y contratos de entrada/salida | Endpoint inteligente, Swagger y validaciones |
| Semana 3 | Integración de pytest y automatización de pruebas | Tests unitarios y evidencia de ejecución |
| Semana 4 | Creación de Dockerfile y estrategia de despliegue | Contenedor funcional y entorno de prueba |
| Semana 5 | Implementación de logging, métricas y monitoreo | Logs, métricas y análisis de rendimiento |
| Semana 6 | Revisión de seguridad, documentación y preparación de defensa | README final, presentación y demostración |

## 16. Limitaciones Actuales

- El sistema depende de una conexión a Internet para consumir la API de Gemini.
- La precisión del OCR disminuye cuando las imágenes tienen baja calidad o están deterioradas.
- El sistema está optimizado para facturas y tickets en español y puede presentar limitaciones con otros formatos o idiomas.
- El procesamiento depende de servicios externos que pueden experimentar saturación temporal.
- Actualmente no existe un despliegue en producción; las pruebas automatizadas se ejecutan mediante Pytest y el pipeline de CI/CD mediante GitHub Actions.
- El despliegue se ha validado localmente mediante Docker.
- Aun no existe un despliegue en produccion (Render, Railway, Azure, etc.).

## 17. Evidencias *ACTUALIZADO

| Evidencia            | Enlace o ubicacion           | Descripcion                                                     |
| -------------------- | ---------------------------- | --------------------------------------------------------------- |
| Documentación API    | `docs/api.md`                | Contratos de entrada/salida y códigos HTTP de la API REST       |
| Capturas de Prueba   | `docs/Evidencias_API.pdf`    | Pruebas de Swagger, manejo de errores y procesamiento por lotes |
| Codigo fuente        | `Backend/main.py`            | Endpoint principal de procesamiento                             |
| Registro de errores  | `docs/REGISTRO_ERRORES.md`   | Documentacion de bloqueos, riesgos y soluciones implementadas   |
| Evidencias Pruebas   | `docs/Evidencias_Testing.pdf`| Capturas de ejecución de pruebas locales y GitHub Actions       |
| Docker               | `Evaluación Semana 4`        | Capturas de Docker Build, Docker Run, Endpoint/health, Endpoint/procesar,Swagger |
| Observabilidad       | `Backend/main.py`            | Middleware HTTP, request_id, duración, estado, modelo y clasificación de errores |
| Benchmark            | `benchmark.py y archivos generados` | Medición de 20 solicitudes y métricas p50, p95, máximo y tasa de error |
| Resultados Benchmark | `benchmark_resultados.csv, benchmark_resumen.txt` | Resultados individuales y resumen de la línea base de rendimiento |


## 18. Créditos y Referencias

FastAPI y Uvicorn: Framework utilizado para el desarrollo del Backend.
Google Gemini 2.5 Flash: Modelo de inteligencia artificial utilizado para la extracción y clasificación de datos.
Tesseract OCR y Pytesseract: Motor de reconocimiento óptico de caracteres.
Firebase Authentication y Firestore: Servicios de autenticación y persistencia de datos.
OpenCV y Pillow: Librerías utilizadas para el procesamiento y limpieza de imágenes.
SheetJS: Librería utilizada para la exportación de información a Excel.
Python Dotenv: Gestión segura de variables de entorno.
Google GenAI SDK: Cliente oficial para la integración con la API de Gemini.

## 19. Versiones

## Versiones

| Version | Descripcion |
|----------|-------------|
| v0.4.0 | Docker e infraestructura inicial |
| v0.5.0 | Observabilidad, rendimiento y escalabilidad |

## 20. Checklist de Revisión

## 20. Checklist de Revisión

* [x] El PDF corresponde al proyecto real y define un endpoint o flujo crítico.
* [x] Se documentan preguntas de observabilidad.
* [x] Existe `request_id` o correlación equivalente.
* [x] Se registran estado, duración y versión del componente IA.
* [x] Se presenta un evento exitoso y un error controlado.
* [x] No se publican claves, tokens ni datos sensibles.
* [x] Se documenta el escenario de medición.
* [x] Se ejecutan al menos 20 solicitudes o se documenta el bloqueo.
* [x] Se incluyen p50, p95, máximo y tasa de error.
* [x] Se identifica un cuello de botella o riesgo.
* [x] Se explica una mejora aplicada o propuesta.
* [x] Se incluye un plan de escalabilidad basado en indicadores.
* [x] README, repositorio, medición y evidencias están actualizados.
* [x] El PDF contiene el enlace funcional al repositorio.



