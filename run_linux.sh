#!/bin/bash
# Script para ejecutar el Sistema de Etiquetas AgriQR en Linux

echo "🌍 Iniciando Sistema de Etiquetas AgriQR para Linux..."

# Cambiar al directorio del proyecto
cd "$(dirname "$0")"

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ No se encontró el entorno virtual. Ejecutando instalación..."
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    
    echo "📦 Instalando dependencias..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Instalación completada."
fi

# Activar entorno virtual y ejecutar aplicación
echo "🚀 Activando entorno virtual y ejecutando aplicación..."
source venv/bin/activate
python3 main.py