#!/bin/bash
# =====================================================
# 🍎 BUILD SCRIPT PARA macOS - AGRIQR SISTEMA ETIQUETAS
# =====================================================
# 🏢 Agrinews - Sistema Profesional de Etiquetas QR
# 📱 Compatible: macOS 10.14+ (Mojave y superior)
# =====================================================

echo "🍎 Compilando AgriQR para macOS..."
echo "================================================"

# Verificar que estamos en macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "❌ Este script debe ejecutarse en macOS"
    exit 1
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "📥 Instalar desde: https://python.org/downloads/"
    exit 1
fi

echo "🐍 Verificando versión de Python..."
python3 --version

# Crear entorno virtual temporal para build
echo "📦 Creando entorno virtual de build..."
if [ -d "venv_build_mac" ]; then
    rm -rf venv_build_mac
fi
python3 -m venv venv_build_mac
source venv_build_mac/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Instalar PyInstaller
echo "🔧 Instalando PyInstaller..."
pip install pyinstaller

# Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf build/ dist/

# Crear icono en formato ICNS (si no existe)
if [ ! -f "icono-agriQR.icns" ]; then
    echo "🎨 Creando icono ICNS para macOS..."
    if command -v sips &> /dev/null; then
        # Usar sips (incluido en macOS)
        mkdir -p AgriQR.iconset
        sips -z 16 16   icono-agriQR.png --out AgriQR.iconset/icon_16x16.png
        sips -z 32 32   icono-agriQR.png --out AgriQR.iconset/icon_16x16@2x.png
        sips -z 32 32   icono-agriQR.png --out AgriQR.iconset/icon_32x32.png
        sips -z 64 64   icono-agriQR.png --out AgriQR.iconset/icon_32x32@2x.png
        sips -z 128 128 icono-agriQR.png --out AgriQR.iconset/icon_128x128.png
        sips -z 256 256 icono-agriQR.png --out AgriQR.iconset/icon_128x128@2x.png
        sips -z 256 256 icono-agriQR.png --out AgriQR.iconset/icon_256x256.png
        sips -z 512 512 icono-agriQR.png --out AgriQR.iconset/icon_256x256@2x.png
        sips -z 512 512 icono-agriQR.png --out AgriQR.iconset/icon_512x512.png
        sips -z 1024 1024 icono-agriQR.png --out AgriQR.iconset/icon_512x512@2x.png
        iconutil -c icns AgriQR.iconset
        mv AgriQR.icns icono-agriQR.icns
        rm -rf AgriQR.iconset
        echo "✅ Icono ICNS creado exitosamente"
    else
        echo "⚠️  sips no disponible, usando PNG como icono"
    fi
fi

# Verificar dependencias específicas de macOS
echo "🔍 Verificando dependencias específicas..."
pip show brother_ql > /dev/null 2>&1 || pip install brother_ql

# Compilar con PyInstaller
echo "⚙️  Compilando aplicación..."
if [ -f "icono-agriQR.icns" ]; then
    ICON_FLAG="--icon=icono-agriQR.icns"
else
    ICON_FLAG="--icon=icono-agriQR.png"
fi

pyinstaller \
    --name "SistemaEtiquetasAgriQR" \
    --onefile \
    --windowed \
    $ICON_FLAG \
    --hidden-import=mysql.connector.locales.eng \
    --hidden-import=mysql.connector.catch23 \
    --hidden-import=pymysql \
    --hidden-import=brother_ql \
    --hidden-import=brother_ql.backends \
    --hidden-import=brother_ql.backends.pyusb \
    --hidden-import=brother_ql.backends.linux_kernel \
    --add-data="icono-agriQR.png:." \
    main.py

# Verificar resultado
if [ -f "dist/SistemaEtiquetasAgriQR.app/Contents/MacOS/SistemaEtiquetasAgriQR" ]; then
    echo "✅ ¡Compilación exitosa!"
    echo "📱 Aplicación creada: dist/SistemaEtiquetasAgriQR.app"
    
    # Obtener información del archivo
    echo ""
    echo "📊 Información del ejecutable:"
    ls -lh dist/SistemaEtiquetasAgriQR.app/Contents/MacOS/SistemaEtiquetasAgriQR
    
    # Crear DMG (opcional)
    echo ""
    read -p "❓ ¿Crear archivo DMG para distribución? (y/N): " create_dmg
    if [[ $create_dmg =~ ^[Yy]$ ]]; then
        echo "📦 Creando DMG..."
        hdiutil create -volname "AgriQR Sistema Etiquetas" \
                      -srcfolder dist \
                      -ov \
                      -format UDZO \
                      "AgriQR-macOS.dmg"
        if [ $? -eq 0 ]; then
            echo "✅ DMG creado: AgriQR-macOS.dmg"
        else
            echo "⚠️  Error creando DMG, pero la aplicación está lista"
        fi
    fi
    
    echo ""
    echo "🍎 ¡Build de macOS completado!"
    echo "📂 Archivos generados:"
    echo "   • dist/SistemaEtiquetasAgriQR.app (Aplicación)"
    if [ -f "AgriQR-macOS.dmg" ]; then
        echo "   • AgriQR-macOS.dmg (Instalador)"
    fi
    echo ""
    echo "📋 Instrucciones de instalación:"
    echo "   1. Copiar SistemaEtiquetasAgriQR.app a /Applications"
    echo "   2. Para Brother QL: pip install brother_ql"
    echo "   3. Las etiquetas se guardan en ~/Etiquetas_QR/"
    
else
    echo "❌ Error en la compilación"
    echo "🔍 Revisa los logs arriba para más detalles"
    exit 1
fi

# Limpiar entorno temporal
echo "🧹 Limpiando archivos temporales..."
deactivate
rm -rf venv_build_mac

echo ""
echo "🎉 ¡Proceso completado!"
echo "Presiona Enter para continuar..."
read