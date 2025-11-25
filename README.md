# 🏢 AgriQR - Sistema Profesional de Etiquetas QR# 🏢 AgriQR - Sistema Profesional de Etiquetas QR# 🏢 AGRINEWS - SISTEMA ETIQUETAS QR

<div align="center"><div align="center">## 📋 Descripción

![AgriQR Logo](icono-agriQR.png)![AgriQR Logo](icono-agriQR.png)Sistema profesional de impresión de etiquetas QR para eventos. Genera etiquetas personalizadas con datos de MySQL y códigos QR para control de acceso.

**Sistema de control de acceso por eventos con impresión Brother QL\*\***Sistema de control de acceso por eventos con impresión Brother QL\*\*## � Compatibilidad Multiplataforma

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)- ✅ **Windows 10/11** - Funcionalidad completa con impresión Brother QL

[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com)

[![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)](https://mysql.com)[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com)- ✅ **macOS** - Generación y guardado de etiquetas

[![Brother QL](https://img.shields.io/badge/Printer-Brother%20QL-green.svg)](https://brother.com)

[![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)](https://mysql.com)- ✅ **Linux** - Generación y guardado de etiquetas

</div>

[![Brother QL](https://img.shields.io/badge/Printer-Brother%20QL-green.svg)](https://brother.com)

## 📋 Descripción

## 🚀 Compilación de Instaladores

Sistema profesional de impresión de etiquetas QR desarrollado para **Agrinews**. Permite la gestión automatizada de eventos con validación de usuarios en tiempo real y generación de credenciales personalizadas.

</div>

### 🎯 Características Principales

### 📦 Requisitos Previos

- **🔐 Autenticación MySQL**: Validación de usuarios contra bases de datos remotas

- **🎫 Gestión de Eventos**: Selección y control de eventos corporativos## 📋 Descripción

- **📱 Códigos QR**: Generación automática con datos personalizados

- **🖨️ Impresión Brother QL**: Compatible con toda la serie Brother QL- Python 3.8+ instalado

- **🌍 Multiplataforma**: Windows, macOS y Linux

- **🎨 Diseño Corporativo**: Interfaz con branding AgrinewsSistema profesional de impresión de etiquetas QR desarrollado para **Agrinews**. Permite la gestión automatizada de eventos con validación de usuarios en tiempo real y generación de credenciales personalizadas.- Git (opcional, para clonar)

## 🚀 Compilación Multiplataforma- Drivers Brother QL (solo Windows)

### 🪟 Windows### 🎯 Características Principales

```batch### 🪟 Compilar para Windows

# Ejecutar script de build

.\build_exe.bat- **🔐 Autenticación MySQL**: Validación de usuarios contra bases de datos remotas

```

**Resultado:** `dist/SistemaEtiquetasAgriQR.exe`- **🎫 Gestión de Eventos**: Selección y control de eventos corporativos```batch

### 🍎 macOS- **📱 Códigos QR**: Generación automática con datos personalizados# Ejecutar el script de build

````bash- **🖨️ Impresión Brother QL**: Compatible con toda la serie Brother QL./build_windows.bat

# Dar permisos y ejecutar

chmod +x build_macos.sh- **🌍 Multiplataforma**: Windows, macOS y Linux```

./build_macos.sh

```- **🎨 Diseño Corporativo**: Interfaz con branding Agrinews

**Resultado:** `dist/SistemaEtiquetasAgriQR.app` + opcional DMG

**Resultado:** `dist/SistemaEtiquetasAgriQR.exe`

### 🐧 Linux

## 🚀 Instalación Rápida

```bash

# Build estándar**Distribución:**

chmod +x build_linux.sh

./build_linux.sh### Opción 1: Ejecutable (Recomendado)



# Build AppImage (portable)- El .exe es portable, no requiere instalación

chmod +x build_linux_appimage.sh

./build_linux_appimage.sh**Windows:**- Incluye todas las dependencias Python

````

**Resultado:** Ejecutable nativo + AppImage portable```bash- Requiere drivers Brother QL para impresión

## 🖨️ Compatibilidad de Impresoras# Descargar y ejecutar

### ✅ Impresoras Soportadasdist/SistemaEtiquetasAgriQR.exe### 🍎 Compilar para macOS

| Modelo | Windows | macOS | Linux | Estado |```

|--------|---------|--------|--------|---------|

| Brother QL-600 | ✅ | ✅ | ✅ | Completo |````bash

| Brother QL-700 | ✅ | ✅ | ✅ | Completo |

| Brother QL-800 | ✅ | ✅ | ✅ | Completo |**macOS/Linux:**# Dar permisos al script

| Brother QL-810W | ✅ | ✅ | ✅ | WiFi + USB |

| Brother QL-820NWB | ✅ | ✅ | ✅ | Red + Bluetooth |```bashchmod +x build_macos.sh

### 🔧 Configuración de Impresión# Ejecutar desde código fuente

- **Windows:** Usa `win32print` (drivers nativos requeridos)pip install -r requirements.txt# Ejecutar el script de build

- **macOS/Linux:** Usa `brother_ql` (comunicación USB directa)

python main.py./build_macos.sh

## 🗄️ Configuración de Base de Datos

`````

El sistema conecta con dos bases MySQL:

### Opción 2: Compilar desde Código**Resultado:** `dist/SistemaEtiquetasAgriQR.app`

```python

# Base de datos principal - Usuarios````bash**Crear DMG (opcional):**

DATABASE_USERS = "agribusi_acreditacion"

# Clonar repositorio

# Base de datos eventos - Eventos

DATABASE_EVENTS = "agribusi_3MpR3s4"git clone https://github.com/usuario/agriqr.git```bash

```

cd agriqrhdiutil create -volname 'Agrinews QR' -srcfolder dist -ov -format UDZO AgrinewsQR.dmg

### Estrategias de Conexión

`````

1. **PyMySQL** (Primera opción)

2. **mysql.connector** (Fallback)# Instalar dependencias

3. **Manejo automático de charset** (UTF8/Latin1)

pip install -r requirements.txt**Distribución:**

## 🛠️ Stack Tecnológico

# Ejecutar aplicación- Arrastra el .app a la carpeta Applications

| Componente | Tecnología | Propósito |

|------------|------------|-----------|python main.py- No requiere instalación adicional

| **UI** | Tkinter | Interfaz gráfica nativa |

| **Base de Datos** | MySQL + PyMySQL | Conexión robusta |```- Las etiquetas se guardan en `~/Etiquetas_QR/`

| **QR** | qrcode + PIL | Generación códigos |

| **Impresión Windows** | win32print | Drivers nativos |## 🖨️ Compatibilidad de Impresoras### 🐧 Compilar para Linux

| **Impresión Mac/Linux** | brother_ql | USB directo |

| **Empaquetado** | PyInstaller | Ejecutables |### ✅ Impresoras Soportadas```bash

## 📁 Estructura del Proyecto# Dar permisos al script

````| Modelo | Windows | macOS | Linux | Estado |chmod +x build_linux.sh

agriqr-sistema-etiquetas/

├── 📄 main.py                       # Aplicación principal|--------|---------|--------|--------|---------|

├── 📄 requirements.txt              # Dependencias Python

├── 📄 ProgramaQR.spec              # Config PyInstaller| Brother QL-600 | ✅ | ✅ | ✅ | Completo |# Ejecutar el script de build

├── 🔨 build_exe.bat                # Build Windows

├── 🔨 build_macos.sh               # Build macOS| Brother QL-700 | ✅ | ✅ | ✅ | Completo |./build_linux.sh

├── 🔨 build_linux.sh               # Build Linux

├── 🔨 build_linux_appimage.sh      # Build AppImage portable| Brother QL-800 | ✅ | ✅ | ✅ | Completo |```

├── 🖼️ icono-agriQR.ico             # Icono Windows

├── 🖼️ icono-agriQR.png             # Icono multiplataforma| Brother QL-810W | ✅ | ✅ | ✅ | WiFi + USB |

├── 📊 setup.iss                    # Inno Setup installer

├── 📚 README.md                    # Documentación| Brother QL-820NWB | ✅ | ✅ | ✅ | Red + Bluetooth |**Resultado:** `dist/SistemaEtiquetasAgriQR`

├── 🗂️ dist/                        # Ejecutables (gitignored)

└── 🚫 .gitignore                   # Archivos ignorados### 🔧 Configuración de Impresión**Instalación manual:**

````

**Windows:** Usa `win32print` (drivers nativos requeridos)```bash

## 🚀 Instalación Rápida

**macOS/Linux:** Usa `brother_ql` (comunicación USB directa)# Hacer ejecutable

### Opción 1: Ejecutables Precompilados

chmod +x dist/SistemaEtiquetasAgriQR

**Windows:**

```bash## 🗄️ Configuración de Base de Datos

# Descargar desde Releases y ejecutar

dist/SistemaEtiquetasAgriQR.exe# Copiar a directorio local (opcional)

```

El sistema conecta con dos bases MySQL:cp dist/SistemaEtiquetasAgriQR ~/bin/

**macOS:**

`````bash# O instalar sistema-wide

# Descargar .app o .dmg desde Releases

# Arrastrar a Applications/````pythonsudo cp dist/SistemaEtiquetasAgriQR /usr/local/bin/

`````

# Base de datos principal - Usuarios```

**Linux:**

````bashDATABASE_USERS = "agribusi_acreditacion"

# Descargar AppImage desde Releases

chmod +x AgriQR-*.AppImage**Distribución:**

./AgriQR-*.AppImage

```# Base de datos eventos - Eventos



### Opción 2: Compilar desde CódigoDATABASE_EVENTS = "agribusi_3MpR3s4"- Binario ejecutable autocontenido



```bash```- Las etiquetas se guardan en `~/Etiquetas_QR/`

# Clonar repositorio

git clone https://github.com/agrinewsprog/agriqr-sistema-etiquetas.git

cd agriqr-sistema-etiquetas

### Estrategias de Conexión## 🔧 Compilación Manual

# Instalar dependencias

pip install -r requirements.txt



# Ejecutar aplicación1. **PyMySQL** (Primera opción)Si prefieres compilar manualmente sin los scripts:

python main.py

2. **mysql.connector** (Fallback)

# O compilar para tu plataforma

./build_[windows|macos|linux].sh3. **Manejo automático de charset** (UTF8/Latin1)```bash

````

# 1. Crear entorno virtual

## 🔧 Desarrollo

## 📦 Compilaciónpython -m venv venv_build

### Requisitos de Desarrollo

source venv_build/bin/activate # Linux/Mac

````bash

# Entorno virtual### 🪟 Windows# o

python -m venv venv

source venv/bin/activate  # Linux/Macvenv_build\Scripts\activate.bat  # Windows

# venv\Scripts\activate   # Windows

```batch

# Dependencias

pip install -r requirements.txt.\build_exe.bat# 2. Instalar dependencias



# Herramientas de build```pip install pyinstaller

pip install pyinstaller

```**Resultado:** `dist/SistemaEtiquetasAgriQR.exe`pip install -r requirements.txt



### Testing Local



```bash### 🍎 macOS# 3. Compilar

# Verificar sintaxis

python -m py_compile main.pypyinstaller ProgramaQR.spec



# Ejecutar aplicación```bash

python main.py

chmod +x build_macos.sh# 4. El resultado estará en dist/

# Test de compilación

pyinstaller ProgramaQR.spec./build_macos.sh```

````

````````

## 🐛 Solución de Problemas

**Resultado:** `dist/SistemaEtiquetasAgriQR.app`## 📁 Estructura del Proyecto

### Errores Comunes

### 🐧 Linux```

**❌ Error MySQL:**

```programa_qr/

Fix: Verificar conectividad y credenciales

```````bash├── main.py                 # Aplicación principal



**❌ Impresora no detectada:**chmod +x build_linux.sh├── requirements.txt        # Dependencias Python

```

Windows: Instalar drivers Brother oficiales./build_linux.sh├── ProgramaQR.spec        # Configuración PyInstaller

Mac/Linux: pip install brother_ql

``````├── build_windows.bat      # Script build Windows



**❌ Error de fuentes:****Resultado:** `dist/SistemaEtiquetasAgriQR`├── build_macos.sh         # Script build macOS

```

Se usan fuentes del sistema automáticamente├── build_linux.sh         # Script build Linux

```

## 🛠️ Stack Tecnológico├── icono-agriQR.ico       # Icono Windows

**❌ Error tkinter (Linux):**

```bash├── icono-agriQR.icns      # Icono macOS (crear si necesario)

# Ubuntu/Debian

sudo apt install python3-tk| Componente | Tecnología | Propósito |├── icono-agriQR.png       # Icono Linux (crear si necesario)



# CentOS/RHEL  |------------|------------|-----------|└── README.md              # Este archivo

sudo yum install tkinter

| **UI** | Tkinter | Interfaz gráfica nativa |```

# Fedora

sudo dnf install python3-tkinter| **Base de Datos** | MySQL + PyMySQL | Conexión robusta |

```

| **QR** | qrcode + PIL | Generación códigos |## ⚙️ Configuración de Base de Datos

### Diagnóstico

| **Impresión Windows** | win32print | Drivers nativos |

El sistema incluye logs detallados en consola y detección automática de problemas.

| **Impresión Mac/Linux** | brother_ql | USB directo |La aplicación se conecta a dos bases de datos MySQL:

## 📦 Distribución

| **Empaquetado** | PyInstaller | Ejecutables |

### Formatos por Plataforma

- `agribusi_acreditacion` - Datos de usuarios

| Plataforma | Formato | Descripción |

|------------|---------|-------------|## 📁 Estructura del Proyecto- `agribusi_3MpR3s4` - Datos de eventos

| **Windows** | `.exe` | Ejecutable portable |

| **Windows** | `.msi` | Instalador Inno Setup |

| **macOS** | `.app` | Aplicación nativa |

| **macOS** | `.dmg` | Imagen de disco |```Configura las credenciales en el código antes de compilar.

| **Linux** | `binario` | Ejecutable nativo |

| **Linux** | `.AppImage` | Portable universal |agriqr/



### Deployment├── 📄 main.py                     # Aplicación principal## 🖨️ Hardware Soportado



Los scripts de build generan automáticamente:├── 📄 requirements.txt            # Dependencias Python



- ✅ Ejecutables optimizados├── 📄 ProgramaQR.spec            # Config PyInstaller### Windows

- ✅ Instaladores nativos (opcionales)

- ✅ Documentación de instalación├── 🔨 build_exe.bat              # Build Windows

- ✅ Scripts de deployment

├── 🖼️ icono-agriQR.ico           # Icono Windows- ✅ Impresoras Brother QL-600/700/800 (con drivers)

## 📊 Métricas del Proyecto

├── 🖼️ icono-agriQR.png           # Icono multiplataforma- ✅ Escáneres USB NetumScan

- **Líneas de código:** ~1,800

- **Dependencias:** 8 principales + 4 de build├── 📊 setup.iss                  # Inno Setup installer- ✅ Cualquier escáner que emule teclado

- **Plataformas:** 3 (Windows/Mac/Linux)

- **Bases de datos:** 2 MySQL├── 📚 README.md                  # Documentación

- **Impresoras:** 5+ modelos Brother QL

- **Formatos distribución:** 6 diferentes├── 🗂️ dist/                      # Ejecutables### macOS/Linux



## 🤝 Contribución│   └── SistemaEtiquetasAgriQR.exe



Este es un proyecto corporativo privado para **Agrinews**. Para modificaciones contactar al equipo de desarrollo.└── 🚫 .gitignore                 # Archivos ignorados- ✅ Escáneres USB NetumScan



### Workflow de Desarrollo```- ✅ Cualquier escáner que emule teclado



1. Fork del repositorio- 💾 Guardado de etiquetas (impresión manual)

2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`

3. Commit cambios: `git commit -m 'Add nueva funcionalidad'`## 🔧 Desarrollo

4. Push a la rama: `git push origin feature/nueva-funcionalidad`

5. Crear Pull Request## 🐛 Solución de Problemas



## 📞 Soporte### Requisitos de Desarrollo



- **Desarrollador:** Sistema AgriQR### Windows

- **Empresa:** Agrinews

- **Versión:** 2.0 Multiplataforma```bash

- **GitHub:** [agrinewsprog/agriqr-sistema-etiquetas](https://github.com/agrinewsprog/agriqr-sistema-etiquetas)

# Clonar repo- **Error impresión:** Verificar drivers Brother QL instalados

## 📜 Licencia

git clone https://github.com/usuario/agriqr.git- **Error MySQL:** Verificar conectividad de red y credenciales

**Uso Corporativo Exclusivo** - Agrinews



Todos los derechos reservados. Prohibida la distribución externa.

# Entorno virtual### macOS

## 🏷️ Changelog

python -m venv venv

### v2.0 (Actual)

- ✅ Compatibilidad multiplataforma completasource venv/bin/activate  # Linux/Mac- **Error fuentes:** El sistema usa fuentes del sistema automáticamente

- ✅ Scripts de build automatizados

- ✅ Soporte Brother QL universal# venv\Scripts\activate   # Windows- **Error permisos:** Dar permisos con `chmod +x`

- ✅ Interface corporativa Agrinews

- ✅ Dual database MySQL con fallbacks

- ✅ AppImage para distribución Linux

- ✅ Documentación profesional# Dependencias### Linux



### v1.0pip install -r requirements.txt

- ✅ Funcionalidad básica Windows

- ✅ Conexión MySQL simple- **Error tkinter:** `sudo apt install python3-tk` (Ubuntu/Debian)

- ✅ Impresión Brother QL básica

- ✅ Generación QR# Herramientas de build- **Error fuentes:** Se usan fuentes del sistema disponibles



---pip install pyinstaller- **Error permisos:** Ejecutar con `chmod +x`



<div align="center">````



**🏢 Desarrollado para Agrinews - Control Profesional de Eventos**## 📞 Soporte



[![Agrinews](https://img.shields.io/badge/Powered%20by-Agrinews-success.svg)](https://agrinews.com)### Testing



</div>Para soporte técnico o reportar errores, contacta al equipo de desarrollo.

````bash

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

````````

Fix: Verificar conectividad y credenciales- Conexión segura a bases de datos MySQL remotas

```- Validación de credenciales de usuario

- Verificación de existencia de eventos

**❌ Impresora no detectada:**- Múltiples estrategias de conexión para máxima confiabilidad

```

Windows: Instalar drivers Brother oficiales### 🎨 Diseño Corporativo

Mac/Linux: pip install brother_ql

````- Colores oficiales Agrinews: Verde (#39C43C) y Gris Oscuro (#373735)

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
````

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
