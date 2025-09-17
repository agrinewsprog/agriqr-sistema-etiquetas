@echo off
REM Empaqueta la app en un ejecutable usando PyInstaller con icono corporativo
echo 🏢 Compilando Sistema de Etiquetas AgriQR...
echo.

REM Instala dependencias primero
echo 📦 Instalando dependencias...
python -m pip install -r requirements.txt

REM Ejecuta PyInstaller (instálalo si no está)
echo 🔧 Instalando/actualizando PyInstaller...
python -m pip install pyinstaller

REM Compilar usando el archivo de especificación con icono
echo 🚀 Compilando ejecutable con icono corporativo...
python -m PyInstaller ProgramaQR.spec

echo.
echo ✅ Compilación completada!
echo 📁 El ejecutable está en: dist\SistemaEtiquetasAgriQR.exe
echo.
pause
