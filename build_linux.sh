#!/bin/bash
# =====================================================
# 🐧 BUILD SCRIPT PARA LINUX - AGRIQR SISTEMA ETIQUETAS
# =====================================================
# 🏢 Agrinews - Sistema Profesional de Etiquetas QR
# 📱 Compatible: Ubuntu 18.04+, Debian 10+, CentOS 7+, Fedora 30+
# =====================================================

echo "🐧 Compilando AgriQR para Linux..."
echo "================================================"

# Verificar que estamos en Linux
if [[ "$(uname)" != "Linux" ]]; then
    echo "❌ Este script debe ejecutarse en Linux"
    exit 1
fi

# Detectar distribución Linux
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$NAME
    echo "🐧 Distribución detectada: $DISTRO"
else
    echo "⚠️  No se pudo detectar la distribución Linux"
    DISTRO="Unknown Linux"
fi

# Verificar Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "📥 Instalar con:"
    echo "   Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo "   CentOS/RHEL:   sudo yum install python3 python3-pip"
    echo "   Fedora:        sudo dnf install python3 python3-pip"
    exit 1
fi

echo "🐍 Verificando versión de Python..."
python3 --version

# Verificar dependencias del sistema necesarias para tkinter
echo "🔍 Verificando dependencias del sistema..."

# Función para verificar e instalar dependencias según la distro
install_system_deps() {
    if command -v apt &> /dev/null; then
        # Ubuntu/Debian
        echo "📦 Verificando dependencias para Ubuntu/Debian..."
        sudo apt update
        sudo apt install -y python3-tk python3-dev python3-venv libusb-1.0-0-dev
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        echo "📦 Verificando dependencias para CentOS/RHEL..."
        sudo yum install -y tkinter python3-devel libusb-devel
    elif command -v dnf &> /dev/null; then
        # Fedora
        echo "📦 Verificando dependencias para Fedora..."
        sudo dnf install -y python3-tkinter python3-devel libusb-devel
    else
        echo "⚠️  Distribución no reconocida, asegúrate de tener:"
        echo "   • python3-tk (tkinter)"
        echo "   • python3-dev (headers de desarrollo)"
        echo "   • libusb-dev (soporte USB para Brother QL)"
    fi
}

# Preguntar si instalar dependencias del sistema
read -p "❓ ¿Instalar dependencias del sistema automáticamente? (y/N): " install_deps
if [[ $install_deps =~ ^[Yy]$ ]]; then
    install_system_deps
fi

# Verificar que tkinter está disponible
echo "🔍 Verificando tkinter..."
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ tkinter no está disponible"
    echo "📥 Instalar con: sudo apt install python3-tk (Ubuntu/Debian)"
    exit 1
fi

# Crear entorno virtual temporal para build
echo "📦 Creando entorno virtual de build..."
if [ -d "venv_build_linux" ]; then
    rm -rf venv_build_linux
fi
python3 -m venv venv_build_linux
source venv_build_linux/bin/activate

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

# Verificar dependencias específicas de Linux
echo "🔍 Verificando dependencias específicas..."
pip show brother_ql > /dev/null 2>&1 || pip install brother_ql

# Compilar con PyInstaller
echo "⚙️  Compilando aplicación..."
pyinstaller \
    --name "SistemaEtiquetasAgriQR" \
    --onefile \
    --icon=icono-agriQR.png \
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
if [ -f "dist/SistemaEtiquetasAgriQR" ]; then
    echo "✅ ¡Compilación exitosa!"
    echo "🐧 Ejecutable creado: dist/SistemaEtiquetasAgriQR"
    
    # Hacer ejecutable
    chmod +x dist/SistemaEtiquetasAgriQR
    
    # Obtener información del archivo
    echo ""
    echo "📊 Información del ejecutable:"
    ls -lh dist/SistemaEtiquetasAgriQR
    file dist/SistemaEtiquetasAgriQR
    
    # Crear script de instalación
    echo "📝 Creando script de instalación..."
    cat > dist/install_agriqr.sh << 'EOF'
#!/bin/bash
# Script de instalación para AgriQR en Linux

echo "🐧 Instalando AgriQR Sistema Etiquetas..."

# Crear directorio en /opt
sudo mkdir -p /opt/agriqr
sudo cp SistemaEtiquetasAgriQR /opt/agriqr/
sudo chmod +x /opt/agriqr/SistemaEtiquetasAgriQR

# Crear enlace simbólico en /usr/local/bin
sudo ln -sf /opt/agriqr/SistemaEtiquetasAgriQR /usr/local/bin/agriqr

# Crear archivo .desktop para el menú
cat > ~/.local/share/applications/agriqr.desktop << 'DESKTOP'
[Desktop Entry]
Version=1.0
Type=Application
Name=AgriQR Sistema Etiquetas
Comment=Sistema profesional de etiquetas QR para eventos
Exec=/opt/agriqr/SistemaEtiquetasAgriQR
Icon=/opt/agriqr/icono-agriQR.png
Terminal=false
StartupNotify=true
Categories=Office;
DESKTOP

# Copiar icono
if [ -f "icono-agriQR.png" ]; then
    sudo cp icono-agriQR.png /opt/agriqr/
fi

echo "✅ AgriQR instalado exitosamente!"
echo "🚀 Ejecutar con: agriqr"
echo "🖥️  O buscar 'AgriQR' en el menú de aplicaciones"
EOF

    chmod +x dist/install_agriqr.sh
    
    # Crear AppImage (si AppImageTool está disponible)
    echo ""
    read -p "❓ ¿Crear AppImage para distribución portable? (y/N): " create_appimage
    if [[ $create_appimage =~ ^[Yy]$ ]]; then
        if command -v appimagetool &> /dev/null; then
            echo "📦 Creando AppImage..."
            
            # Crear estructura AppDir
            mkdir -p AgriQR.AppDir/usr/bin
            mkdir -p AgriQR.AppDir/usr/share/icons/hicolor/256x256/apps
            mkdir -p AgriQR.AppDir/usr/share/applications
            
            # Copiar ejecutable
            cp dist/SistemaEtiquetasAgriQR AgriQR.AppDir/usr/bin/
            
            # Copiar icono
            cp icono-agriQR.png AgriQR.AppDir/usr/share/icons/hicolor/256x256/apps/agriqr.png
            cp icono-agriQR.png AgriQR.AppDir/agriqr.png
            
            # Crear AppRun
            cat > AgriQR.AppDir/AppRun << 'APPRUN'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
exec "${HERE}/usr/bin/SistemaEtiquetasAgriQR" "$@"
APPRUN
            chmod +x AgriQR.AppDir/AppRun
            
            # Crear .desktop
            cat > AgriQR.AppDir/agriqr.desktop << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=AgriQR Sistema Etiquetas
Exec=SistemaEtiquetasAgriQR
Icon=agriqr
Comment=Sistema profesional de etiquetas QR
Categories=Office;
DESKTOP
            
            # Generar AppImage
            appimagetool AgriQR.AppDir AgriQR-Linux-x86_64.AppImage
            
            if [ $? -eq 0 ]; then
                echo "✅ AppImage creado: AgriQR-Linux-x86_64.AppImage"
                chmod +x AgriQR-Linux-x86_64.AppImage
            else
                echo "⚠️  Error creando AppImage, pero el ejecutable está listo"
            fi
            
            # Limpiar AppDir temporal
            rm -rf AgriQR.AppDir
        else
            echo "⚠️  appimagetool no está instalado"
            echo "📥 Instalar desde: https://appimage.github.io/appimagetool/"
        fi
    fi
    
    echo ""
    echo "🐧 ¡Build de Linux completado!"
    echo "📂 Archivos generados:"
    echo "   • dist/SistemaEtiquetasAgriQR (Ejecutable)"
    echo "   • dist/install_agriqr.sh (Script de instalación)"
    if [ -f "AgriQR-Linux-x86_64.AppImage" ]; then
        echo "   • AgriQR-Linux-x86_64.AppImage (Portable)"
    fi
    echo ""
    echo "📋 Opciones de instalación:"
    echo "   1. Ejecutar directamente: ./dist/SistemaEtiquetasAgriQR"
    echo "   2. Instalar sistema: cd dist && sudo ./install_agriqr.sh"
    echo "   3. Portable: usar AppImage (si se creó)"
    echo ""
    echo "🖨️  Para Brother QL: sudo apt install libusb-1.0-0-dev"
    echo "📁 Las etiquetas se guardan en ~/Etiquetas_QR/"
    
else
    echo "❌ Error en la compilación"
    echo "🔍 Revisa los logs arriba para más detalles"
    exit 1
fi

# Limpiar entorno temporal
echo "🧹 Limpiando archivos temporales..."
deactivate
rm -rf venv_build_linux

echo ""
echo "🎉 ¡Proceso completado!"
echo "Presiona Enter para continuar..."
read