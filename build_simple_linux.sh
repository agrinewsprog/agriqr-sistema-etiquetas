#!/bin/bash
# Script de build simplificado para debugging

echo "🔧 Build simplificado para Linux - AgriQR"
echo "=========================================="

# Crear entorno virtual limpio
rm -rf venv_build_simple
python3 -m venv venv_build_simple
source venv_build_simple/bin/activate

# Instalar dependencias básicas
pip install --upgrade pip
pip install wheel setuptools

# Instalar Pillow desde código fuente para asegurar compatibilidad
echo "📦 Instalando Pillow desde código fuente..."
pip install --no-binary=Pillow Pillow

# Instalar otras dependencias
pip install mysql-connector-python PyMySQL qrcode[pil] brother_ql

# Verificar que todo funciona
echo "🧪 Verificando dependencias..."
python3 test_dependencies.py

if [ $? -eq 0 ]; then
    echo "✅ Dependencias OK, procediendo con PyInstaller..."
    
    pip install pyinstaller
    
    # Build simplificado con todos los imports necesarios
    pyinstaller --onefile \
        --name="AgriQR-Linux-Simple" \
        --hidden-import=PIL._tkinter_finder \
        --hidden-import=PIL.ImageTk \
        --hidden-import=tkinter \
        --collect-all=PIL \
        --collect-all=tkinter \
        main.py
    
    if [ -f "dist/AgriQR-Linux-Simple" ]; then
        echo "✅ Build exitoso: dist/AgriQR-Linux-Simple"
        chmod +x dist/AgriQR-Linux-Simple
    else
        echo "❌ Build falló"
    fi
else
    echo "❌ Dependencias fallan, no se puede continuar"
fi

deactivate