#!/bin/bash
# =====================================================
# 📦 BUILD APPIMAGE PARA LINUX - AGRIQR SISTEMA ETIQUETAS
# =====================================================
# 🏢 Agrinews - Crear AppImage portable para distribución
# 📱 Compatible: Cualquier distribución Linux x86_64
# =====================================================

echo "📦 Creando AppImage de AgriQR para Linux..."
echo "================================================"

# Verificar que el ejecutable existe
if [ ! -f "dist/SistemaEtiquetasAgriQR" ]; then
    echo "❌ No se encontró dist/SistemaEtiquetasAgriQR"
    echo "🔧 Ejecuta primero: ./build_linux.sh"
    exit 1
fi

# Descargar AppImageTool si no existe
if ! command -v appimagetool &> /dev/null; then
    echo "📥 Descargando AppImageTool..."
    wget -O appimagetool https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool
    APPIMAGETOOL_CMD="./appimagetool"
else
    APPIMAGETOOL_CMD="appimagetool"
fi

# Limpiar AppDir anterior
if [ -d "AgriQR.AppDir" ]; then
    rm -rf AgriQR.AppDir
fi

echo "🏗️  Creando estructura AppDir..."

# Crear estructura de directorios
mkdir -p AgriQR.AppDir/usr/bin
mkdir -p AgriQR.AppDir/usr/lib
mkdir -p AgriQR.AppDir/usr/share/icons/hicolor/256x256/apps
mkdir -p AgriQR.AppDir/usr/share/applications

# Copiar ejecutable principal
echo "📄 Copiando ejecutable..."
cp dist/SistemaEtiquetasAgriQR AgriQR.AppDir/usr/bin/

# Copiar icono
echo "🎨 Copiando recursos..."
cp icono-agriQR.png AgriQR.AppDir/usr/share/icons/hicolor/256x256/apps/agriqr.png
cp icono-agriQR.png AgriQR.AppDir/agriqr.png

# Crear archivo .desktop
echo "📝 Creando archivo .desktop..."
cat > AgriQR.AppDir/agriqr.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=AgriQR Sistema Etiquetas
Comment=Sistema profesional de etiquetas QR para eventos - Agrinews
Exec=SistemaEtiquetasAgriQR
Icon=agriqr
Categories=Office;Business;
Keywords=QR;etiquetas;eventos;impresion;brother;mysql;
Terminal=false
StartupNotify=true
MimeType=text/plain;
Version=2.0
EOF

# Copiar .desktop a usr/share/applications también
cp AgriQR.AppDir/agriqr.desktop AgriQR.AppDir/usr/share/applications/

# Crear AppRun script
echo "🔧 Creando AppRun..."
cat > AgriQR.AppDir/AppRun << 'EOF'
#!/bin/bash

# AppRun script para AgriQR Sistema Etiquetas
# Configura el entorno y ejecuta la aplicación

HERE="$(dirname "$(readlink -f "${0}")")"

# Configurar variables de entorno
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"

# Configurar Python path si es necesario
export PYTHONPATH="${HERE}/usr/lib/python:${PYTHONPATH}"

# Configurar directorio de etiquetas en el home del usuario
export AGRIQR_ETIQUETAS_DIR="${HOME}/Etiquetas_QR"
mkdir -p "${AGRIQR_ETIQUETAS_DIR}"

# Mostrar información de inicio (solo en modo debug)
if [ "$AGRIQR_DEBUG" = "1" ]; then
    echo "🏢 AgriQR Sistema Etiquetas - Agrinews"
    echo "📂 Directorio de etiquetas: ${AGRIQR_ETIQUETAS_DIR}"
    echo "🖥️  Ejecutando desde: ${HERE}"
fi

# Ejecutar la aplicación principal
exec "${HERE}/usr/bin/SistemaEtiquetasAgriQR" "$@"
EOF

chmod +x AgriQR.AppDir/AppRun

# Crear archivo de información
echo "📋 Creando metadatos..."
cat > AgriQR.AppDir/.DirIcon << 'EOF'
icono-agriQR.png
EOF

# Verificar estructura
echo "🔍 Verificando estructura AppDir..."
echo "Contenido de AgriQR.AppDir:"
find AgriQR.AppDir -type f | sort

# Crear AppImage
echo ""
echo "⚙️  Generando AppImage..."
$APPIMAGETOOL_CMD AgriQR.AppDir AgriQR-Sistema-Etiquetas-v2.0-x86_64.AppImage

# Verificar resultado
if [ -f "AgriQR-Sistema-Etiquetas-v2.0-x86_64.AppImage" ]; then
    echo ""
    echo "✅ ¡AppImage creado exitosamente!"
    echo "📦 Archivo: AgriQR-Sistema-Etiquetas-v2.0-x86_64.AppImage"
    
    # Hacer ejecutable
    chmod +x AgriQR-Sistema-Etiquetas-v2.0-x86_64.AppImage
    
    # Mostrar información del archivo
    echo ""
    echo "📊 Información del AppImage:"
    ls -lh AgriQR-Sistema-Etiquetas-v2.0-x86_64.AppImage
    
    # Crear script de instalación para AppImage
    cat > install_appimage.sh << 'INSTALL'
#!/bin/bash
# Script de instalación para AgriQR AppImage

APPIMAGE_FILE="AgriQR-Sistema-Etiquetas-v2.0-x86_64.AppImage"

if [ ! -f "$APPIMAGE_FILE" ]; then
    echo "❌ No se encontró $APPIMAGE_FILE"
    exit 1
fi

echo "📦 Instalando AgriQR AppImage..."

# Crear directorio de aplicaciones local
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications

# Copiar AppImage
cp "$APPIMAGE_FILE" ~/.local/bin/agriqr.appimage
chmod +x ~/.local/bin/agriqr.appimage

# Crear wrapper script
cat > ~/.local/bin/agriqr << 'WRAPPER'
#!/bin/bash
exec ~/.local/bin/agriqr.appimage "$@"
WRAPPER
chmod +x ~/.local/bin/agriqr

# Crear entrada de menú
cat > ~/.local/share/applications/agriqr.desktop << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=AgriQR Sistema Etiquetas
Comment=Sistema profesional de etiquetas QR - Agrinews
Exec=agriqr
Icon=agriqr
Categories=Office;Business;
Terminal=false
DESKTOP

echo "✅ AgriQR AppImage instalado!"
echo "🚀 Ejecutar con: agriqr"
echo "🗑️  Desinstalar: rm ~/.local/bin/agriqr*"
INSTALL
    
    chmod +x install_appimage.sh
    
    echo ""
    echo "🎯 Instrucciones de uso:"
    echo "   1. Ejecutar directamente: ./AgriQR-Sistema-Etiquetas-v2.0-x86_64.AppImage"
    echo "   2. Instalar para usuario: ./install_appimage.sh"
    echo "   3. Distribuir: Solo compartir el archivo .AppImage"
    echo ""
    echo "✨ Ventajas del AppImage:"
    echo "   • 📱 Portable - No requiere instalación"
    echo "   • 🌍 Universal - Funciona en cualquier distribución"
    echo "   • 🔒 Aislado - No interfiere con el sistema"
    echo "   • ⚡ Rápido - Ejecuta inmediatamente"
    
else
    echo "❌ Error creando AppImage"
    echo "🔍 Verifica que appimagetool funcione correctamente"
    exit 1
fi

# Limpiar archivos temporales
echo ""
echo "🧹 Limpiando archivos temporales..."
rm -rf AgriQR.AppDir

if [ -f "./appimagetool" ]; then
    rm ./appimagetool
fi

echo ""
echo "🎉 ¡AppImage listo para distribución!"
echo "📁 Archivos generados:"
echo "   • AgriQR-Sistema-Etiquetas-v2.0-x86_64.AppImage"
echo "   • install_appimage.sh"