# ReceiptIA

> Sistema inteligente para análisis, validación y organización de facturas con IA

## 1. Información General

**Módulo:** Desarrollo de Aplicaciones con IA  
**Semana:** Semana 1 - Diagnóstico e inventario técnico del proyecto  
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
- *API REST estructurada con FastAPI.*
- *Contratos estrictos de entrada y salida utilizando Pydantic para validación de datos.*
- *Endpoints de monitoreo y procesamiento completamente documentados.*


### Funcionalidades incompletas o pendientes

- Mejorar manejo de errores cuando el backend no está activo.
- Agregar almacenamiento de imágenes en la nube en una etapa futura.
- Mejorar la precisión del OCR con imágenes borrosas.
- Documentar mejor la instalación en otra computadora.
- Ajustar reglas de validación para reducir falsos positivos.
- Fortalecer reglas de seguridad en Firebase.


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
|-- Backend/             # Logica del servidor FastAPI, OCR y conexion con Gemini
|   ├── main.py
|   ├── requirements.txt
|   ├── .env.example
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
|
|-- Setup.bat            # Configuracion inicial del proyecto
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

## 11. Datos Utilizados

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

## 12. Riesgos Técnicos y Deuda Técnica

| Riesgo | Categoría | Probabilidad | Impacto | Mitigación propuesta |
|---|---|---|---|---|
|  | Datos / Modelo / Código / Seguridad / Despliegue | Baja / Media / Alta | Bajo / Medio / Alto |  
| Dependencia de Tesseract OCR instalado localmente | Dependencias | Alta | Alto | Automatizar instalación mediante Setup.bat y Docker
| Saturación o indisponibilidad temporal de Gemini | Servicios Externos | Media | Alto | Implementar reintentos automáticos y modelos alternativos |
| Dependencia de conexión a Internet | Infraestructura | Media | Alto | Validaciones y manejo de errores |

## 13. Plan de Mejora por Semana

| Semana | Mejora esperada | Evidencia esperada |
|---|---|---|
| Semana 2 | Implementación de modelos Pydantic y contratos de entrada/salida | Endpoint inteligente, Swagger y validaciones |
| Semana 3 | Integración de pytest y automatización de pruebas | Tests unitarios y evidencia de ejecución |
| Semana 4 | Creación de Dockerfile y estrategia de despliegue | Contenedor funcional y entorno de prueba |
| Semana 5 | Implementación de logging, métricas y monitoreo | Logs, métricas y análisis de rendimiento |
| Semana 6 | Revisión de seguridad, documentación y preparación de defensa | README final, presentación y demostración |

## 14. Limitaciones Actuales

-El sistema depende de una conexión a Internet para consumir la API de Gemini.
-La precisión del OCR disminuye cuando las imágenes tienen baja calidad o están deterioradas.
-El sistema está optimizado para facturas y tickets en español y puede presentar limitaciones con otros formatos o idiomas.
-El procesamiento depende de servicios externos que pueden experimentar saturación temporal.
-Actualmente no existen pruebas automatizadas ni una estrategia de despliegue en producción.

## 15. Evidencias *ACTUALIZADO

| Evidencia            | Enlace o ubicacion           | Descripcion                                                     |
| -------------------- | ---------------------------- | --------------------------------------------------------------- |
| Documentación API    | `docs/api.md`                | Contratos de entrada/salida y códigos HTTP de la API REST       |
| Capturas de Prueba   | `docs/Evidencias_API.pdf`    | Pruebas de Swagger, manejo de errores y procesamiento por lotes |
| Codigo fuente        | `Backend/main.py`            | Endpoint principal de procesamiento                             |



## 16. Créditos y Referencias

FastAPI y Uvicorn: Framework utilizado para el desarrollo del Backend.
Google Gemini 2.5 Flash: Modelo de inteligencia artificial utilizado para la extracción y clasificación de datos.
Tesseract OCR y Pytesseract: Motor de reconocimiento óptico de caracteres.
Firebase Authentication y Firestore: Servicios de autenticación y persistencia de datos.
OpenCV y Pillow: Librerías utilizadas para el procesamiento y limpieza de imágenes.
SheetJS: Librería utilizada para la exportación de información a Excel.
Python Dotenv: Gestión segura de variables de entorno.
Google GenAI SDK: Cliente oficial para la integración con la API de Gemini.

## 17. Checklist de Revisión

Antes de entregar, verifiquen:

- [x] La API se ejecuta localmente o se explica claramente como probarla.
- [x] Existe endpoint de salud.
- [x] Existe endpoint de metadatos.
- [x] Existe endpoint inteligente principal.
- [x] El contrato de entrada y salida esta documentado.
- [x] Hay validacion basica.
- [x] Hay manejo de errores.
- [x] Hay evidencia de prueba exitosa.
- [x] Hay evidencia de entrada invalida o error controlado.
- [x] El README esta actualizado.
- [x] No se publican claves, tokens ni datos sensibles

## API REST

La funcionalidad inteligente de ReceiptIA se encuentra expuesta mediante FastAPI.

### Endpoints disponibles

| Método | Endpoint | Descripción |
|---------|----------|-------------|
| GET | /health | Estado del servicio |
| GET | /metadata | Información general de la API |
| POST | /procesar | Procesa una factura individual |
| POST | /procesar-lote | Procesa múltiples facturas |
| POST | /leer-texto | Extrae únicamente el texto OCR |


