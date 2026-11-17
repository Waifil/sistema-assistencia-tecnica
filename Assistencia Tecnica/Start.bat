@echo off
title Sistema de Assistencia Tecnica

cd /d "%~dp0Sistema"

start "Servidor do Sistema" cmd /k "py app.py"

timeout /t 3 /nobreak >nul

start http://127.0.0.1:5000

exit