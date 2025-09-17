# -*- mode: python ; coding: utf-8 -*-
# ====================================================
# 🌍 CONFIGURACIÓN MULTIPLATAFORMA PYINSTALLER
# ====================================================

import platform
import os

# Detectar sistema operativo
current_os = platform.system()
is_windows = current_os == "Windows"
is_macos = current_os == "Darwin"
is_linux = current_os == "Linux"

# Configuración específica por OS
if is_windows:
    app_name = 'SistemaEtiquetasAgriQR'
    icon_file = 'icono-agriQR.ico'
    console_mode = False
    additional_imports = ['win32print', 'win32ui']
elif is_macos:
    app_name = 'SistemaEtiquetasAgriQR'
    icon_file = 'icono-agriQR.icns'  # Crear versión .icns para Mac
    console_mode = False
    additional_imports = []
else:  # Linux
    app_name = 'SistemaEtiquetasAgriQR'
    icon_file = 'icono-agriQR.png'   # Usar PNG para Linux
    console_mode = False
    additional_imports = []

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'mysql.connector',
        'mysql.connector.locales',
        'mysql.connector.locales.eng',
        'mysql.connector.conversion',
        'mysql.connector.constants',
        'mysql.connector.errorcode',
        'mysql.connector.protocol',
        'mysql.connector.cursor',
        'mysql.connector.connection',
        'mysql.connector.errors',
        'mysql.connector.authentication',
        'mysql.connector.charsets',
        'mysql.connector.abstracts',
        'mysql.connector.catch23',
        'mysql.connector.utils',
        'mysql.connector.custom_types',
        'mysql.connector.optionfiles',
        'mysql.connector.pooling',
        'pymysql',
        'pymysql.cursors',
        'pymysql.connections',
        'platform'
    ] + additional_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=console_mode,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file if os.path.exists(icon_file) else None,
)
