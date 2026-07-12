@echo off
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    py tools\build_gallery.py
    goto sprawdz
)

where python >nul 2>nul
if %errorlevel%==0 (
    python tools\build_gallery.py
    goto sprawdz
)

echo.
echo Python nie jest zainstalowany.
echo Nie jest to problem - GitHub Actions wygeneruje galerie po Push origin.
pause
exit /b 0

:sprawdz
if errorlevel 1 (
    echo.
    echo Wystapil blad.
    pause
    exit /b 1
)

echo.
echo Galeria zostala zaktualizowana.
pause