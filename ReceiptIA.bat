@echo off
title ReceiptIA

set "ROOT=%~dp0"
set "BACKEND=%ROOT%Backend"
set "FRONTEND=%ROOT%Frontend"
set "PYTHON=%BACKEND%\venv\Scripts\python.exe"

echo ==============================
echo Iniciando ReceiptIA
echo ==============================

if not exist "%PYTHON%" (
    echo ERROR: No se encontro Python en el entorno virtual:
    echo %PYTHON%
    pause
    exit
)

if not exist "%BACKEND%\main.py" (
    echo ERROR: No se encontro Backend\main.py
    pause
    exit
)

if not exist "%FRONTEND%\index.html" (
    echo ERROR: No se encontro Frontend\index.html
    pause
    exit
)

echo Iniciando backend...
start /min "Backend ReceiptIA" cmd /k ""%PYTHON%" -m uvicorn main:app --reload --app-dir "%BACKEND%""

echo Iniciando frontend...
start /min "Frontend ReceiptIA" cmd /k ""%PYTHON%" -m http.server 5501 --directory "%FRONTEND%""

echo Esperando servidores...
timeout /t 8 >nul

echo Abriendo pagina...
start "" "http://127.0.0.1:5501/index.html"

exit