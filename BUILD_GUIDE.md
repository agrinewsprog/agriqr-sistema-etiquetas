# 🔨 Guía de Compilación Multiplataforma - AgriQR

Esta guía detalla cómo compilar AgriQR Sistema Etiquetas en las diferentes plataformas soportadas.

## 📋 Índice

- [🪟 Windows](#-windows)
- [🍎 macOS](#-macos)
- [🐧 Linux](#-linux)
- [📦 AppImage](#-appimage-linux-portable)
- [🔧 Resolución de Problemas](#-resolución-de-problemas)

---

## 🪟 Windows

### Requisitos Previos

- Windows 7 o superior (recomendado Windows 10/11)
- Python 3.8+ instalado desde [python.org](https://python.org)
- Git (opcional) para clonar el repositorio

### Compilación

```batch
# Ejecutar el script de build
.\build_exe.bat
```

### ¿Qué hace el script?

1. **Verifica dependencias**: Python, pip
2. **Crea entorno virtual**: Aislamiento limpio
3. **Instala dependencias**: Todas las librerías necesarias
4. **Compila con PyInstaller**: Genera ejecutable optimizado
5. **Incluye recursos**: Icono, assets, configuraciones

### Resultados

- **Ejecutable**: `dist/SistemaEtiquetasAgriQR.exe`
- **Tamaño**: ~50-80 MB (incluye todas las dependencias)
- **Distribución**: Portable, no requiere instalación

### Características

- ✅ Impresión nativa con `win32print`
- ✅ Detección automática impresoras Brother QL
- ✅ Compatibilidad Windows 7-11
- ✅ Icono corporativo integrado

---

## 🍎 macOS

### Requisitos Previos

- macOS 10.14 (Mojave) o superior
- Python 3.8+ instalado desde [python.org](https://python.org) o Homebrew
- Xcode Command Line Tools: `xcode-select --install`

### Compilación

```bash
# Dar permisos de ejecución
chmod +x build_macos.sh

# Ejecutar build
./build_macos.sh
```

### ¿Qué hace el script?

1. **Verifica el sistema**: Confirma macOS y dependencias
2. **Crea entorno virtual**: `venv_build_mac`
3. **Genera icono ICNS**: Convierte PNG a formato nativo macOS
4. **Compila aplicación**: Genera `.app` bundle
5. **Opción DMG**: Crea imagen de disco para distribución

### Resultados

- **Aplicación**: `dist/SistemaEtiquetasAgriQR.app`
- **DMG (opcional)**: `AgriQR-macOS.dmg`
- **Tamaño**: ~60-100 MB

### Características

- ✅ Bundle nativo `.app`
- ✅ Icono ICNS de alta resolución
- ✅ Impresión con `brother_ql` via USB
- ✅ Integración con Finder y Dock
- ✅ Compatible con notarización Apple

### Instalación

```bash
# Mover a Applications
cp -r dist/SistemaEtiquetasAgriQR.app /Applications/

# O usar DMG
open AgriQR-macOS.dmg
# Arrastrar a Applications
```

---

## 🐧 Linux

### Requisitos Previos

- Distribución moderna: Ubuntu 18.04+, Debian 10+, CentOS 7+, Fedora 30+
- Python 3.8+ y herramientas de desarrollo

### Instalación de Dependencias

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk python3-dev libusb-1.0-0-dev
```

**CentOS/RHEL:**

```bash
sudo yum install python3 python3-pip tkinter python3-devel libusb-devel
```

**Fedora:**

```bash
sudo dnf install python3 python3-pip python3-tkinter python3-devel libusb-devel
```

### Compilación

```bash
# Dar permisos de ejecución
chmod +x build_linux.sh

# Ejecutar build
./build_linux.sh
```

### ¿Qué hace el script?

1. **Detecta distribución**: Ubuntu, Debian, CentOS, Fedora, etc.
2. **Verifica dependencias**: Python, tkinter, desarrollo
3. **Instala dependencias del sistema**: Opcional, con confirmación
4. **Crea entorno virtual**: `venv_build_linux`
5. **Compila ejecutable**: Binario nativo Linux
6. **Genera instalador**: Script de instalación sistema

### Resultados

- **Ejecutable**: `dist/SistemaEtiquetasAgriQR`
- **Instalador**: `dist/install_agriqr.sh`
- **Tamaño**: ~40-70 MB

### Opciones de Instalación

**1. Ejecución directa:**

```bash
./dist/SistemaEtiquetasAgriQR
```

**2. Instalación usuario:**

```bash
cd dist
./install_agriqr.sh
# Crea: ~/.local/bin/agriqr
```

**3. Instalación sistema:**

```bash
sudo cp dist/SistemaEtiquetasAgriQR /usr/local/bin/agriqr
```

---

## 📦 AppImage (Linux Portable)

### ¿Qué es AppImage?

AppImage es un formato de distribución portable para Linux que:

- ✅ **No requiere instalación**: Ejecuta directamente
- ✅ **Universal**: Funciona en cualquier distribución
- ✅ **Aislado**: No interfiere con el sistema
- ✅ **Portable**: Un solo archivo autocontenido

### Compilación

```bash
# Primero compilar el ejecutable base
./build_linux.sh

# Luego crear AppImage
chmod +x build_linux_appimage.sh
./build_linux_appimage.sh
```

### ¿Qué hace el script?

1. **Verifica ejecutable base**: Debe existir `dist/SistemaEtiquetasAgriQR`
2. **Descarga AppImageTool**: Si no está instalado
3. **Crea estructura AppDir**: Directorios y metadatos
4. **Configura AppRun**: Script de entrada
5. **Genera AppImage**: Archivo `.AppImage` final

### Resultados

- **AppImage**: `AgriQR-Sistema-Etiquetas-v2.0-x86_64.AppImage`
- **Instalador**: `install_appimage.sh`
- **Tamaño**: ~45-75 MB

### Uso del AppImage

**Ejecución directa:**

```bash
chmod +x AgriQR-Sistema-Etiquetas-v2.0-x86_64.AppImage
./AgriQR-Sistema-Etiquetas-v2.0-x86_64.AppImage
```

**Instalación para usuario:**

```bash
./install_appimage.sh
# Crea entrada en menú y comando 'agriqr'
```

**Distribución:**

- Solo compartir el archivo `.AppImage`
- Compatible con cualquier distribución Linux x86_64
- No requiere dependencias adicionales

---

## 🔧 Resolución de Problemas

### Problemas Comunes

#### 🪟 Windows

**Error: "Python no encontrado"**

```batch
# Solución: Instalar Python desde python.org
# Asegurar que esté en PATH
```

**Error: "No se puede imprimir"**

```batch
# Solución: Instalar drivers Brother QL oficiales
# Verificar impresora en Panel de Control
```

#### 🍎 macOS

**Error: "Permission denied"**

```bash
# Solución: Dar permisos al script
chmod +x build_macos.sh
```

**Error: "sips command not found"**

```bash
# Solución: sips está incluido en macOS
# Verificar Xcode Command Line Tools
xcode-select --install
```

**Error: "Cannot create ICNS"**

```bash
# Solución: El script continuará con PNG
# ICNS es opcional pero recomendado
```

#### 🐧 Linux

**Error: "tkinter not found"**

```bash
# Ubuntu/Debian
sudo apt install python3-tk

# CentOS/RHEL
sudo yum install tkinter

# Fedora
sudo dnf install python3-tkinter
```

**Error: "No module named '\_tkinter'"**

```bash
# Solución: Instalar python3-tk
# Verificar con: python3 -c "import tkinter"
```

**Error: "libusb not found"**

```bash
# Ubuntu/Debian
sudo apt install libusb-1.0-0-dev

# CentOS/RHEL
sudo yum install libusb-devel

# Fedora
sudo dnf install libusb-devel
```

### Logs y Depuración

Todos los scripts generan logs detallados durante la compilación:

```bash
# Ver logs en tiempo real
./build_[platform].sh

# Los errores aparecen en la consola
# Incluyen sugerencias de solución
```

### Verificación Post-Compilación

**Verificar ejecutable:**

```bash
# Windows
dist\SistemaEtiquetasAgriQR.exe --version

# macOS
dist/SistemaEtiquetasAgriQR.app/Contents/MacOS/SistemaEtiquetasAgriQR --version

# Linux
dist/SistemaEtiquetasAgriQR --version

# AppImage
./AgriQR-*.AppImage --version
```

### Contacto para Soporte

Si tienes problemas con la compilación:

1. **Revisar logs**: Los scripts muestran errores detallados
2. **Verificar dependencias**: Seguir requisitos previos exactos
3. **Contactar desarrollo**: Con logs completos del error

---

## 🚀 Automatización CI/CD

Los scripts están diseñados para integrarse en pipelines de CI/CD:

### GitHub Actions (Ejemplo)

```yaml
name: Build Multiplatform

on: [push, pull_request]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
        with:
          python-version: "3.8"
      - run: .\build_exe.bat

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
        with:
          python-version: "3.8"
      - run: |
          chmod +x build_macos.sh
          ./build_macos.sh

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
        with:
          python-version: "3.8"
      - run: |
          sudo apt update
          sudo apt install python3-tk python3-dev libusb-1.0-0-dev
          chmod +x build_linux.sh
          ./build_linux.sh
          chmod +x build_linux_appimage.sh  
          ./build_linux_appimage.sh
```

---

**🏢 Agrinews - Documentación de Build v2.0**
