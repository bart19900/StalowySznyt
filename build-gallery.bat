@echo off
cd /d "%~dp0.."
py tools\build_gallery.py
if errorlevel 1 (
  echo.
  echo Wystapil blad.
  pause
  exit /b 1
)
echo.
echo Galeria zostala zaktualizowana.
pause
