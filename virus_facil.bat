@echo off
title Cyber Rescue - Modo Facil
cls
echo ==========================================
echo  INICIANDO CYBER RESCUE (MODO SENCILLO)
echo ==========================================
echo.
python src\main_facil.py
if %errorlevel% neq 0 (
    echo.
    echo [X] Ocurrio un error al ejecutar la aplicacion.
    echo Asegurese de que Python esta agregado al PATH.
    echo.
    pause
)
