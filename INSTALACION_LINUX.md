# 🐧 Guía de Instalación para Linux

## Sistema de Etiquetas AgriQR - Versión Linux

### 📋 Prerrequisitos del Sistema

Antes de instalar, asegúrate de tener instalados los siguientes paquetes del sistema:

```bash
# Actualizar repositorios
sudo apt-get update

# Instalar dependencias del sistema
sudo apt-get install -y python3-tk python3-dev python3-pil.imagetk
sudo apt-get install -y python3-pil libjpeg-dev zlib1g-dev libfreetype-dev
sudo apt-get install -y python3-pip
```

### 🚀 Instalación Rápida

1. **Ejecutar el script automático:**
   ```bash
   ./run_linux.sh
   ```
   
   Este script se encargará de:
   - Crear el entorno virtual si no existe
   - Instalar todas las dependencias de Python
   - Ejecutar la aplicación

### 🛠️ Instalación Manual

Si prefieres instalar manualmente:

```bash
# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Actualizar pip
pip install --upgrade pip

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
python3 main.py
```

### 🖨️ Configuración de Impresora (Opcional)

#### Para Impresión Automática con Brother QL:

1. **Conectar la impresora Brother QL por USB**

2. **Verificar que se detecta:**
   ```bash
   lsusb | grep Brother
   ```

3. **Instalar driver oficial Brother (recomendado):**
   - Descargar desde: https://support.brother.com
   - Buscar tu modelo (QL-600, QL-700, QL-800)
   - Instalar el driver .deb

4. **Configurar en CUPS:**
   ```bash
   # Abrir interfaz web de CUPS
   firefox http://localhost:631
   
   # O usar línea de comandos
   sudo lpadmin -p BrotherQL -E -v usb://Brother/QL-700 -m brother_ql_700.ppd
   ```

#### Verificar Configuración:
```bash
# Listar impresoras disponibles
lpstat -p

# Imprimir página de prueba
echo "Prueba" | lp -d BrotherQL
```

### ⚡ Ejecución Diaria

Una vez instalado, solo necesitas:

```bash
./run_linux.sh
```

O manualmente:
```bash
source venv/bin/activate && python3 main.py
```

### 📁 Ubicación de Archivos

- **Etiquetas generadas:** `~/Etiquetas_QR/`
- **Logs de acceso:** `log_accesos.csv` (en directorio del programa)
- **Logs de impresión:** `log_impresiones.csv` (en directorio del programa)

### 🔧 Solución de Problemas

#### Error: "No module named 'mysql'"
```bash
# Asegúrate de activar el entorno virtual
source venv/bin/activate
python3 main.py
```

#### Error: "cannot import name 'ImageTk'"
```bash
# Instalar dependencias del sistema
sudo apt-get install python3-pil.imagetk python3-tk
```

#### La impresora no funciona
- En Linux, las etiquetas se guardan automáticamente en `~/Etiquetas_QR/`
- Puedes imprimirlas manualmente desde ahí
- O configurar CUPS para impresión automática

### 🆘 Soporte

Si tienes problemas:

1. **Verificar logs en la aplicación**
2. **Revisar archivos en `~/Etiquetas_QR/INSTRUCCIONES_IMPRESION.txt`**
3. **Contactar soporte técnico**

### 🔄 Actualización

Para actualizar el sistema:

```bash
# Activar entorno virtual
source venv/bin/activate

# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Ejecutar versión actualizada
python3 main.py
```

---

**Nota:** En Linux, el sistema está optimizado para guardar las etiquetas como archivos PNG y PDF de alta calidad, listos para imprimir. La impresión directa es opcional y requiere configuración adicional.