FROM python:3.12-slim

# Evita archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Muestra inmediatamente los print()
ENV PYTHONUNBUFFERED=1

# Instalar Tesseract y librerías necesarias
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    tesseract-ocr-eng \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Puerto
EXPOSE 8000

# Ejecutar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
