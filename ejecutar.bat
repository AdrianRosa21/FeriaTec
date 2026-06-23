@echo off
title Cyber Rescue Windows - Simulación Educativa
echo ==========================================================
echo [!] INICIANDO CYBER RESCUE WINDOWS (MODO DESARROLLO)
echo ==========================================================
echo.
echo [!] Verificando e instalando dependencias (customtkinter)...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [X] ERROR: No se pudo verificar o instalar las dependencias.
    echo Asegurese de que Python esta agregado al PATH de Windows.
    echo.
    pause
    exit /b
)

echo.
echo [OK] Dependencias listas.
echo [!] Iniciando aplicacion principal...
python src/main.py
if %errorlevel% neq 0 (
    echo.
    echo [X] Ocurrio un error al ejecutar la aplicacion.
    echo.
    pause
)
