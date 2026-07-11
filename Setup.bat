@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Configuracion inicial de ReceiptIA

set "ROOT=%~dp0"
set "BACKEND=%ROOT%Backend"
set "VENV=%BACKEND%\venv"
set "PYTHON_EXE=%VENV%\Scripts\python.exe"
set "ENV_FILE=%BACKEND%\.env"

echo ==============================
echo Configuracion inicial ReceiptIA
echo ==============================
echo.

if not exist "%BACKEND%\main.py" (
    echo ERROR: No se encontro Backend\main.py
    pause
    exit /b
)

if not exist "%BACKEND%\requirements.txt" (
    echo ERROR: No se encontro Backend\requirements.txt
    pause
    exit /b
)

echo Verificando Python...
python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python no esta instalado o no esta agregado al PATH.
    echo Instala Python 3.11 o 3.12 y vuelve a ejecutar este archivo.
    pause
    exit /b
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
        exit /b
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
    exit /b
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

    if "!GEMINI_KEY!"=="" (
        echo.
        echo ERROR: No se ingreso ninguna API Key.
        echo Debe volver a ejecutar Setup.bat y pegar su API Key.
        pause
        exit /b
    )

    (
        echo GEMINI_API_KEY=!GEMINI_KEY!
        echo GEMINI_MODEL=gemini-2.5-flash
        echo GEMINI_FALLBACK_MODEL=gemini-2.5-flash-lite
        echo # Opcional si Tesseract esta en otra ruta:
        echo # TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
    ) > "%ENV_FILE%"

    echo Archivo .env creado correctamente.
)

echo.
echo Verificando archivo .env...

findstr /B "GEMINI_API_KEY=" "%ENV_FILE%" >nul 2>&1

if errorlevel 1 (
    echo ERROR: El archivo .env se creo, pero no contiene GEMINI_API_KEY.
    echo Abra Backend\.env y revise la API Key.
    pause
    exit /b
)

echo Archivo .env verificado correctamente.

echo.
echo ==============================
echo Configuracion finalizada
echo ==============================
echo.
echo Ahora puede ejecutar ReceiptIA.bat para abrir ReceiptIA.
echo.

pause