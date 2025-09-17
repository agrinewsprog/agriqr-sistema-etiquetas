# 🏢 AgriQR - Sistema Profesional de Etiquetas QR# 🏢 AGRINEWS - SISTEMA ETIQUETAS QR



<div align="center">## 📋 Descripción



![AgriQR Logo](icono-agriQR.png)Sistema profesional de impresión de etiquetas QR para eventos. Genera etiquetas personalizadas con datos de MySQL y códigos QR para control de acceso.



**Sistema de control de acceso por eventos con impresión Brother QL**## � Compatibilidad Multiplataforma



[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)- ✅ **Windows 10/11** - Funcionalidad completa con impresión Brother QL

[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com)- ✅ **macOS** - Generación y guardado de etiquetas

[![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)](https://mysql.com)- ✅ **Linux** - Generación y guardado de etiquetas

[![Brother QL](https://img.shields.io/badge/Printer-Brother%20QL-green.svg)](https://brother.com)

## 🚀 Compilación de Instaladores

</div>

### 📦 Requisitos Previos

## 📋 Descripción

- Python 3.8+ instalado

Sistema profesional de impresión de etiquetas QR desarrollado para **Agrinews**. Permite la gestión automatizada de eventos con validación de usuarios en tiempo real y generación de credenciales personalizadas.- Git (opcional, para clonar)

- Drivers Brother QL (solo Windows)

### 🎯 Características Principales

### 🪟 Compilar para Windows

- **🔐 Autenticación MySQL**: Validación de usuarios contra bases de datos remotas

- **🎫 Gestión de Eventos**: Selección y control de eventos corporativos```batch

- **📱 Códigos QR**: Generación automática con datos personalizados# Ejecutar el script de build

- **🖨️ Impresión Brother QL**: Compatible con toda la serie Brother QL./build_windows.bat

- **🌍 Multiplataforma**: Windows, macOS y Linux```

- **🎨 Diseño Corporativo**: Interfaz con branding Agrinews

**Resultado:** `dist/SistemaEtiquetasAgriQR.exe`

## 🚀 Instalación Rápida

**Distribución:**

### Opción 1: Ejecutable (Recomendado)

- El .exe es portable, no requiere instalación

**Windows:**- Incluye todas las dependencias Python

```bash- Requiere drivers Brother QL para impresión

# Descargar y ejecutar

dist/SistemaEtiquetasAgriQR.exe### 🍎 Compilar para macOS

```

```bash

**macOS/Linux:**# Dar permisos al script

```bashchmod +x build_macos.sh

# Ejecutar desde código fuente

pip install -r requirements.txt# Ejecutar el script de build

python main.py./build_macos.sh

``````



### Opción 2: Compilar desde Código**Resultado:** `dist/SistemaEtiquetasAgriQR.app`



```bash**Crear DMG (opcional):**

# Clonar repositorio

git clone https://github.com/usuario/agriqr.git```bash

cd agriqrhdiutil create -volname 'Agrinews QR' -srcfolder dist -ov -format UDZO AgrinewsQR.dmg

```

# Instalar dependencias

pip install -r requirements.txt**Distribución:**



# Ejecutar aplicación- Arrastra el .app a la carpeta Applications

python main.py- No requiere instalación adicional

```- Las etiquetas se guardan en `~/Etiquetas_QR/`



## 🖨️ Compatibilidad de Impresoras### 🐧 Compilar para Linux



### ✅ Impresoras Soportadas```bash

# Dar permisos al script

| Modelo | Windows | macOS | Linux | Estado |chmod +x build_linux.sh

|--------|---------|--------|--------|---------|

| Brother QL-600 | ✅ | ✅ | ✅ | Completo |# Ejecutar el script de build

| Brother QL-700 | ✅ | ✅ | ✅ | Completo |./build_linux.sh

| Brother QL-800 | ✅ | ✅ | ✅ | Completo |```

| Brother QL-810W | ✅ | ✅ | ✅ | WiFi + USB |

| Brother QL-820NWB | ✅ | ✅ | ✅ | Red + Bluetooth |**Resultado:** `dist/SistemaEtiquetasAgriQR`



### 🔧 Configuración de Impresión**Instalación manual:**



**Windows:** Usa `win32print` (drivers nativos requeridos)```bash

**macOS/Linux:** Usa `brother_ql` (comunicación USB directa)# Hacer ejecutable

chmod +x dist/SistemaEtiquetasAgriQR

## 🗄️ Configuración de Base de Datos

# Copiar a directorio local (opcional)

El sistema conecta con dos bases MySQL:cp dist/SistemaEtiquetasAgriQR ~/bin/

# O instalar sistema-wide

```pythonsudo cp dist/SistemaEtiquetasAgriQR /usr/local/bin/

# Base de datos principal - Usuarios```

DATABASE_USERS = "agribusi_acreditacion"

**Distribución:**

# Base de datos eventos - Eventos

DATABASE_EVENTS = "agribusi_3MpR3s4"- Binario ejecutable autocontenido

```- Las etiquetas se guardan en `~/Etiquetas_QR/`



### Estrategias de Conexión## 🔧 Compilación Manual



1. **PyMySQL** (Primera opción)Si prefieres compilar manualmente sin los scripts:

2. **mysql.connector** (Fallback)

3. **Manejo automático de charset** (UTF8/Latin1)```bash

# 1. Crear entorno virtual

## 📦 Compilaciónpython -m venv venv_build

source venv_build/bin/activate  # Linux/Mac

### 🪟 Windows# o

venv_build\Scripts\activate.bat  # Windows

```batch

.\build_exe.bat# 2. Instalar dependencias

```pip install pyinstaller

**Resultado:** `dist/SistemaEtiquetasAgriQR.exe`pip install -r requirements.txt



### 🍎 macOS# 3. Compilar

pyinstaller ProgramaQR.spec

```bash

chmod +x build_macos.sh# 4. El resultado estará en dist/

./build_macos.sh```

```

**Resultado:** `dist/SistemaEtiquetasAgriQR.app`## 📁 Estructura del Proyecto



### 🐧 Linux```

programa_qr/

```bash├── main.py                 # Aplicación principal

chmod +x build_linux.sh├── requirements.txt        # Dependencias Python

./build_linux.sh├── ProgramaQR.spec        # Configuración PyInstaller

```├── build_windows.bat      # Script build Windows

**Resultado:** `dist/SistemaEtiquetasAgriQR`├── build_macos.sh         # Script build macOS

├── build_linux.sh         # Script build Linux

## 🛠️ Stack Tecnológico├── icono-agriQR.ico       # Icono Windows

├── icono-agriQR.icns      # Icono macOS (crear si necesario)

| Componente | Tecnología | Propósito |├── icono-agriQR.png       # Icono Linux (crear si necesario)

|------------|------------|-----------|└── README.md              # Este archivo

| **UI** | Tkinter | Interfaz gráfica nativa |```

| **Base de Datos** | MySQL + PyMySQL | Conexión robusta |

| **QR** | qrcode + PIL | Generación códigos |## ⚙️ Configuración de Base de Datos

| **Impresión Windows** | win32print | Drivers nativos |

| **Impresión Mac/Linux** | brother_ql | USB directo |La aplicación se conecta a dos bases de datos MySQL:

| **Empaquetado** | PyInstaller | Ejecutables |

- `agribusi_acreditacion` - Datos de usuarios

## 📁 Estructura del Proyecto- `agribusi_3MpR3s4` - Datos de eventos



```Configura las credenciales en el código antes de compilar.

agriqr/

├── 📄 main.py                     # Aplicación principal## 🖨️ Hardware Soportado

├── 📄 requirements.txt            # Dependencias Python

├── 📄 ProgramaQR.spec            # Config PyInstaller### Windows

├── 🔨 build_exe.bat              # Build Windows

├── 🖼️ icono-agriQR.ico           # Icono Windows- ✅ Impresoras Brother QL-600/700/800 (con drivers)

├── 🖼️ icono-agriQR.png           # Icono multiplataforma- ✅ Escáneres USB NetumScan

├── 📊 setup.iss                  # Inno Setup installer- ✅ Cualquier escáner que emule teclado

├── 📚 README.md                  # Documentación

├── 🗂️ dist/                      # Ejecutables### macOS/Linux

│   └── SistemaEtiquetasAgriQR.exe

└── 🚫 .gitignore                 # Archivos ignorados- ✅ Escáneres USB NetumScan

```- ✅ Cualquier escáner que emule teclado

- 💾 Guardado de etiquetas (impresión manual)

## 🔧 Desarrollo

## 🐛 Solución de Problemas

### Requisitos de Desarrollo

### Windows

```bash

# Clonar repo- **Error impresión:** Verificar drivers Brother QL instalados

git clone https://github.com/usuario/agriqr.git- **Error MySQL:** Verificar conectividad de red y credenciales



# Entorno virtual### macOS

python -m venv venv

source venv/bin/activate  # Linux/Mac- **Error fuentes:** El sistema usa fuentes del sistema automáticamente

# venv\Scripts\activate   # Windows- **Error permisos:** Dar permisos con `chmod +x`



# Dependencias### Linux

pip install -r requirements.txt

- **Error tkinter:** `sudo apt install python3-tk` (Ubuntu/Debian)

# Herramientas de build- **Error fuentes:** Se usan fuentes del sistema disponibles

pip install pyinstaller- **Error permisos:** Ejecutar con `chmod +x`

```

## 📞 Soporte

### Testing

Para soporte técnico o reportar errores, contacta al equipo de desarrollo.

```bash

# Verificar sintaxis---

python -m py_compile main.py

🏢 **Agrinews** - Sistema desarrollado para gestión profesional de eventos

# Ejecutar aplicación

python main.py## Características Principales ✨



# Compilar test### 🎯 Funcionalidades Core

pyinstaller ProgramaQR.spec

```- **Validación de Usuarios**: Autenticación contra base de datos MySQL

- **Gestión de Eventos**: Selección y validación de eventos desde BD

## 🐛 Solución de Problemas- **Generación QR**: Códigos QR únicos con información del usuario y evento

- **Impresión Directa**: Compatible con impresoras Brother QL series

### Errores Comunes- **Interfaz Profesional**: Diseño corporativo con colores Agrinews



**❌ Error MySQL:**### 🔒 Seguridad y Validación

```

Fix: Verificar conectividad y credenciales- Conexión segura a bases de datos MySQL remotas

```- Validación de credenciales de usuario

- Verificación de existencia de eventos

**❌ Impresora no detectada:**- Múltiples estrategias de conexión para máxima confiabilidad

```

Windows: Instalar drivers Brother oficiales### 🎨 Diseño Corporativo

Mac/Linux: pip install brother_ql

```- Colores oficiales Agrinews: Verde (#39C43C) y Gris Oscuro (#373735)

- Iconografía corporativa integrada

**❌ Error de fuentes:**- Interfaz intuitiva y profesional

```- Mensajes de estado y retroalimentación visual

Se usan fuentes del sistema automáticamente

```## Instalación y Uso 🚀



### Diagnóstico### Opción 1: Ejecutable (Recomendado)



El sistema incluye logs detallados en consola y detección automática de problemas.1. Descargar `SistemaEtiquetasAgriQR.exe` de la carpeta `dist/`

2. Ejecutar directamente (no requiere instalación)

## 📊 Métricas del Proyecto3. El sistema incluye todas las dependencias necesarias



- **Líneas de código:** ~1,800### Opción 2: Desde Código Fuente

- **Dependencias:** 8 principales

- **Plataformas:** 3 (Windows/Mac/Linux)```bash

- **Bases de datos:** 2 MySQL# Instalar dependencias

- **Impresoras:** 5+ modelos Brother QLpip install -r requirements.txt



## 🤝 Contribución# Ejecutar aplicación

python main.py

Este es un proyecto corporativo privado para **Agrinews**. Para modificaciones contactar al equipo de desarrollo.```



## 📞 Soporte## Requisitos del Sistema 📋



- **Desarrollador:** Sistema AgriQR### Hardware Mínimo

- **Empresa:** Agrinews  

- **Versión:** 2.0 Multiplataforma- **SO**: Windows 7 o superior

- **RAM**: 4 GB mínimo

## 📜 Licencia- **Espacio**: 100 MB libres

- **Impresora**: Brother QL series (QL-700, QL-800, QL-820NWB, etc.)

**Uso Corporativo Exclusivo** - Agrinews

### Conectividad

Todos los derechos reservados. Prohibida la distribución externa.

- **Internet**: Conexión estable para acceso a bases de datos

---- **Impresora**: USB o Red según modelo



<div align="center">### Software



**🏢 Desarrollado para Agrinews - Control Profesional de Eventos**- **Windows**: 7/8/10/11 (64-bit recomendado)

- **Drivers**: Brother QL instalados y configurados

[![Agrinews](https://img.shields.io/badge/Powered%20by-Agrinews-success.svg)](https://agrinews.com)

## Configuración de Impresora 🖨️

</div>
### Impresoras Brother QL Compatibles

- Brother QL-700
- Brother QL-800
- Brother QL-810W
- Brother QL-820NWB
- Brother QL-1110NWB

### Configuración

1. Instalar drivers oficiales de Brother
2. Conectar impresora (USB/Red)
3. Configurar como impresora predeterminada
4. Verificar con impresión de prueba

### Etiquetas Recomendadas

- **Tamaño**: 62mm x 29mm (DK-11209)
- **Tipo**: Papel térmico
- **Cantidad**: Rollo continuo

## Resolución de Problemas 🔧

### Script de Diagnóstico

Incluido `diagnostico_sistema.py` para verificar:

- Dependencias del sistema
- Conectividad de bases de datos
- Estado de impresoras
- Configuración general

```bash
python diagnostico_sistema.py
```

### Problemas Comunes

#### ❌ Error de Conexión MySQL

**Síntomas**: "No localization support for language 'eng'"
**Solución**: El ejecutable incluye múltiples estrategias de conexión que se activan automáticamente

#### ❌ Impresora No Detectada

**Síntomas**: No aparece en lista de impresoras
**Soluciones**:

1. Reinstalar drivers Brother
2. Verificar conexión USB/Red
3. Reiniciar servicio de impresión Windows
4. Configurar como predeterminada

#### ❌ Usuario No Válido

**Síntomas**: "Usuario no encontrado"
**Soluciones**:

1. Verificar credenciales exactas
2. Confirmar que usuario existe en BD
3. Revisar conexión a internet

#### ❌ No Se Cargan Eventos

**Síntomas**: Lista vacía o error al cargar
**Soluciones**:

1. Verificar conexión a internet
2. Ejecutar diagnóstico del sistema
3. Contactar administrador BD

## Bases de Datos 🗄️

### Estructura

- **BD Principal**: `agribusi_acreditacion`

  - Tabla: `usuarios`
  - Función: Validación de credenciales

- **BD Eventos**: `agribusi_3MpR3s4`
  - Tabla: `Eventos`
  - Función: Gestión y selección de eventos

### Conexión

- **Servidor**: MySQL remoto seguro
- **Estrategias**: Múltiples fallbacks automáticos
- **Timeout**: 10 segundos configurables
- **Charset**: UTF8/Latin1 automático

## Desarrollo y Compilación 👨‍💻

### Estructura del Proyecto

```
programa_qr/
├── main.py                    # Aplicación principal
├── ProgramaQR.spec           # Configuración PyInstaller
├── build_exe.bat            # Script de compilación
├── requirements.txt         # Dependencias Python
├── diagnostico_sistema.py   # Herramienta diagnóstico
├── icono-agriQR.ico        # Icono corporativo
└── dist/                   # Ejecutables compilados
    └── SistemaEtiquetasAgriQR.exe
```

### Compilar Nueva Versión

```bash
# Instalar dependencias de compilación
pip install pyinstaller

# Compilar
.\build_exe.bat
```

### Dependencias Principales

- `mysql-connector-python`: Conexión MySQL
- `pymysql`: Alternativa MySQL
- `Pillow`: Procesamiento imágenes
- `brother_ql`: Control impresoras
- `qrcode`: Generación códigos QR
- `tkinter`: Interfaz gráfica
- `pywin32`: Integración Windows

## Soporte Técnico 📞

### Contacto

- **Desarrollador**: Sistema AgriQR
- **Empresa**: Agrinews
- **Versión**: 2.0 Profesional

### Logs y Diagnóstico

El sistema genera logs automáticos en:

- Consola de aplicación (tiempo real)
- Archivos de diagnóstico (`diagnostico_agriqr_YYYYMMDD_HHMMSS.txt`)

### Reportar Problemas

Incluir en el reporte:

1. Archivo de diagnóstico
2. Descripción del problema
3. Pasos para reproducir
4. Configuración del sistema
5. Modelo de impresora

## Historial de Versiones 📝

### v2.0 (Actual)

- ✅ Diseño corporativo Agrinews
- ✅ Múltiples estrategias conexión MySQL
- ✅ Interfaz profesional renovada
- ✅ Sistema diagnóstico integrado
- ✅ Compilación optimizada
- ✅ Icono corporativo

### v1.0

- ✅ Funcionalidad básica
- ✅ Conexión MySQL simple
- ✅ Impresión Brother QL
- ✅ Generación QR

## Licencia y Uso 📜

**Uso Corporativo Exclusivo**

- Desarrollado específicamente para Agrinews
- Prohibida distribución externa
- Todos los derechos reservados

---

**© 2024 Agrinews - Sistema AgriQR v2.0**
