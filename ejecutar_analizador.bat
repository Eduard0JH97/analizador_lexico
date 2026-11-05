@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ===================================================
echo     Iniciando Analizador Lexico y Sintactico
echo ===================================================
echo.

set PY_CMD=

py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PY_CMD=py -3
) else (
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PY_CMD=python
    )
)

if "%PY_CMD%"=="" (
    echo [ERROR] No se encontro un interprete de Python 3 en el sistema o en el PATH.
    echo Por favor instale Python 3 desde https://www.python.org/ y asegurese de marcar
    echo la opcion "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

%PY_CMD% main.py

echo.
pause
