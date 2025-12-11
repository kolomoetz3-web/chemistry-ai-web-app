@echo off
chcp 65001 >nul
title Автоматический деплой на Render.com
color 0A

echo.
echo ============================================================
echo    АВТОМАТИЧЕСКИЙ ДЕПЛОЙ НА RENDER.COM
echo ============================================================
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не найден!
    echo Установите Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python найден
echo.

python DO_IT_ALL.py

echo.
echo ============================================================
pause


