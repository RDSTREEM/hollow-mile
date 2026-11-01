 @echo off
setlocal
title HOLLOW MILE - Build

echo.
echo ================================
echo       HOLLOW MILE BUILDER
echo ================================
echo.

cd /d "%~dp0"

echo [1/4] Installing project dependencies...
python -m pip install -e .
if errorlevel 1 goto error

echo.
echo [2/4] Installing PyInstaller...
python -m pip install pyinstaller
if errorlevel 1 goto error

echo.
echo [3/4] Cleaning previous builds...

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist hollow-mile.spec del hollow-mile.spec

echo.
echo [4/4] Building executable...

python -m PyInstaller ^
    --onefile ^
    --console ^
    --name hollow-mile ^
    --paths src ^
    build.py

if errorlevel 1 goto error

echo.
echo ================================
echo       BUILD SUCCESSFUL
echo ================================
echo.
echo Executable: dist\hollow-mile.exe
echo.

pause
exit /b 0

:error
echo.
echo ================================
echo          BUILD FAILED
echo ================================
echo.
pause
exit /b 1