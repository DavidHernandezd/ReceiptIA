@echo off
title Configuracion inicial de ReceiptIA

set "ROOT=%~dp0"
set "BACKEND=%ROOT%Backend"
set "FRONTEND=%ROOT%Frontend"
set "VENV=%BACKEND%\venv"
set "PYTHON_EXE=%VENV%\Scripts\python.exe"
set "ENV_FILE=%BACKEND%\.env"
set "ENV_EXAMPLE=%BACKEND%\.env.example"

echo ==============================
echo Configuracion inicial ReceiptIA
echo ==============================
echo.

if not exist "%BACKEND%\main.py" (
    echo ERROR: No se encontro Backend\main.py
    pause
    exit
)

if not exist "%BACKEND%\requirements.txt" (
    echo ERROR: No se encontro Backend\requirements.txt
    pause
    exit
)

echo Verificando Python...
python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python no esta instalado o no esta agregado al PATH.
    echo Instala Python 3.11 o 3.12 desde python.org y vuelve a ejecutar este archivo.
    pause
    exit
)

python --version

echo.
echo Verificando Tesseract OCR...

if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo Tesseract ya esta instalado.
) else (
    echo Tesseract no esta instalado.
    echo Intentando instalar Tesseract automaticamente con winget...
    echo.

    winget --version >nul 2>&1

    if errorlevel 1 (
        echo ERROR: winget no esta disponible en este equipo.
        echo Instala Tesseract manualmente o instala App Installer desde Microsoft Store.
        pause
        exit
    )

    winget install -e --id UB-Mannheim.TesseractOCR
)

echo.
echo Creando entorno virtual...

if not exist "%VENV%" (
    cd /d "%BACKEND%"
    python -m venv venv
) else (
    echo El entorno virtual ya existe.
)

if not exist "%PYTHON_EXE%" (
    echo ERROR: No se pudo crear el entorno virtual correctamente.
    pause
    exit
)

echo.
echo Actualizando pip...
"%PYTHON_EXE%" -m pip install --upgrade pip setuptools wheel

echo.
echo Instalando dependencias...
"%PYTHON_EXE%" -m pip install -r "%BACKEND%\requirements.txt"

echo.
echo Configurando archivo .env...

if exist "%ENV_FILE%" (
    echo El archivo .env ya existe. No se modificara.
) else (
    echo No existe archivo .env.
    echo.
    set /p GEMINI_KEY=Pegue aqui su API Key de Gemini y presione Enter: 

    echo GEMINI_API_KEY=%GEMINI_KEY%>"%ENV_FILE%"
    echo # Opcional si Tesseract esta en otra ruta:>>"%ENV_FILE%"
    echo # TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe>>"%ENV_FILE%"

    echo Archivo .env creado correctamente.
)

echo.
echo ==============================
echo Configuracion finalizada
echo ==============================
echo.
echo Ahora puede ejecutar Start.bat para abrir ReceiptIA.
echo.

pause