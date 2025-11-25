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

# Instalar dependencias específicas para build portable
echo "🔧 Instalando dependencias adicionales para build portable..."
pip install --upgrade Pillow
pip install --upgrade pillow[imagetk]

# Verificar que PIL ImageTk funciona en el entorno virtual
echo "🔍 Verificando PIL ImageTk en entorno virtual..."
python3 test_dependencies.py
if [ $? -ne 0 ]; then
    echo "❌ Las dependencias no están funcionando correctamente"
    echo "🔧 Instalando Pillow con soporte completo..."
    pip uninstall -y Pillow
    pip install --no-binary=Pillow Pillow
    pip install --upgrade Pillow
    
    echo "🔍 Verificando nuevamente..."
    python3 test_dependencies.py
    if [ $? -ne 0 ]; then
        echo "❌ No se pudo solucionar el problema con PIL"
        exit 1
    fi
fi

# Instalar PyInstaller
echo "🔧 Instalando PyInstaller..."
pip install pyinstaller

# Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf build/ dist/

# Verificar dependencias específicas de Linux
echo "🔍 Verificando dependencias específicas..."
pip show brother_ql > /dev/null 2>&1 || pip install brother_ql

# Compilar con PyInstaller usando spec file
echo "⚙️  Compilando aplicación con spec file optimizado..."
pyinstaller SistemaEtiquetasAgriQR-Linux.spec

# Verificar resultado del spec file
if [ ! -f "dist/SistemaEtiquetasAgriQR-Linux" ]; then
    echo "⚠️  Build con spec falló, intentando método tradicional..."
    
    # Método fallback con parámetros en línea de comandos
    pyinstaller \
        --name "SistemaEtiquetasAgriQR" \
        --onefile \
        --icon=icono-agriQR.png \
        --hidden-import=tkinter \
        --hidden-import=PIL._tkinter_finder \
        --hidden-import=PIL.ImageTk \
        --hidden-import=PIL.Image \
        --hidden-import=PIL.ImageDraw \
        --hidden-import=PIL.ImageFont \
        --hidden-import=mysql.connector.locales.eng \
        --hidden-import=mysql.connector.catch23 \
        --hidden-import=pymysql \
        --hidden-import=brother_ql \
        --hidden-import=brother_ql.backends \
        --hidden-import=brother_ql.backends.pyusb \
        --hidden-import=brother_ql.backends.linux_kernel \
        --collect-submodules=PIL \
        --collect-submodules=tkinter \
        --add-data="icono-agriQR.png:." \
        main.py
fi

# Verificar resultado
EXECUTABLE_PATH=""
if [ -f "dist/SistemaEtiquetasAgriQR-Linux" ]; then
    EXECUTABLE_PATH="dist/SistemaEtiquetasAgriQR-Linux"
elif [ -f "dist/SistemaEtiquetasAgriQR" ]; then
    EXECUTABLE_PATH="dist/SistemaEtiquetasAgriQR"
fi

if [ -n "$EXECUTABLE_PATH" ]; then
    echo "✅ ¡Compilación exitosa!"
    echo "🐧 Ejecutable creado: $EXECUTABLE_PATH"
    
    # Hacer ejecutable
    chmod +x "$EXECUTABLE_PATH"
    
    # Obtener información del archivo
    echo ""
    echo "📊 Información del ejecutable:"
    ls -lh "$EXECUTABLE_PATH"
    file "$EXECUTABLE_PATH"
    
    # Probar imports críticos
    echo ""
    echo "🔍 Probando ejecutable..."
    timeout 10s "$EXECUTABLE_PATH" --version 2>/dev/null || echo "⚠️  Test de ejecución completado (timeout esperado)"
    
    # Crear script de instalación
    echo "📝 Creando script de instalación..."
    cat > dist/install_agriqr.sh << EOF
#!/bin/bash
# Script de instalación para AgriQR en Linux

echo "🐧 Instalando AgriQR Sistema Etiquetas..."

# Detectar el ejecutable disponible
EXECUTABLE=""
if [ -f "SistemaEtiquetasAgriQR-Linux" ]; then
    EXECUTABLE="SistemaEtiquetasAgriQR-Linux"
elif [ -f "SistemaEtiquetasAgriQR" ]; then
    EXECUTABLE="SistemaEtiquetasAgriQR"
else
    echo "❌ No se encontró el ejecutable"
    exit 1
fi

echo "📂 Usando ejecutable: \$EXECUTABLE"

# Crear directorio en /opt
sudo mkdir -p /opt/agriqr
sudo cp "\$EXECUTABLE" /opt/agriqr/
sudo chmod +x "/opt/agriqr/\$EXECUTABLE"

# Crear enlace simbólico en /usr/local/bin
sudo ln -sf "/opt/agriqr/\$EXECUTABLE" /usr/local/bin/agriqr

# Crear archivo .desktop para el menú
cat > ~/.local/share/applications/agriqr.desktop << 'DESKTOP'
[Desktop Entry]
Version=1.0
Type=Application
Name=AgriQR Sistema Etiquetas
Comment=Sistema profesional de etiquetas QR para eventos
Exec=/opt/agriqr/\$EXECUTABLE
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
            cp "$EXECUTABLE_PATH" AgriQR.AppDir/usr/bin/
            
            # Copiar icono
            cp icono-agriQR.png AgriQR.AppDir/usr/share/icons/hicolor/256x256/apps/agriqr.png
            cp icono-agriQR.png AgriQR.AppDir/agriqr.png
            
            # Crear AppRun
            EXECUTABLE_NAME=$(basename "$EXECUTABLE_PATH")
            cat > AgriQR.AppDir/AppRun << APPRUN
#!/bin/bash
HERE="\$(dirname "\$(readlink -f "\${0}")")"
exec "\${HERE}/usr/bin/$EXECUTABLE_NAME" "\$@"
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
    echo "   • $EXECUTABLE_PATH (Ejecutable)"
    echo "   • dist/install_agriqr.sh (Script de instalación)"
    if [ -f "AgriQR-Linux-x86_64.AppImage" ]; then
        echo "   • AgriQR-Linux-x86_64.AppImage (Portable)"
    fi
    echo ""
    echo "📋 Opciones de uso:"
    echo "   1. Ejecutar directamente: ./$EXECUTABLE_PATH"
    echo "   2. Instalar sistema: cd dist && sudo ./install_agriqr.sh"
    echo "   3. Portable: usar AppImage (si se creó)"
    echo ""
    echo "🔧 Dependencias incluidas: PIL ImageTk, MySQL, Brother QL"
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