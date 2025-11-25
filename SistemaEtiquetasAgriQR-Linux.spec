# -*- mode: python ; coding: utf-8 -*-

# =====================================================
# 🐧 SPEC FILE PARA LINUX - AGRIQR SISTEMA ETIQUETAS
# =====================================================

import sys
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Detectar imports automáticamente
hiddenimports = []

# PIL/Pillow - imports necesarios para ImageTk
pil_imports = [
    'PIL._tkinter_finder',
    'PIL.ImageTk',
    'PIL.Image', 
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'PIL._imaging',
    'PIL._imagingft',
    'PIL._imagingmath'
]
hiddenimports.extend(pil_imports)

# Tkinter
tk_imports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.simpledialog',
    'tkinter.filedialog'
]
hiddenimports.extend(tk_imports)

# MySQL
mysql_imports = [
    'mysql.connector',
    'mysql.connector.locales.eng',
    'mysql.connector.catch23',
    'pymysql',
    'pymysql.cursors'
]
hiddenimports.extend(mysql_imports)

# Brother QL
brother_imports = [
    'brother_ql',
    'brother_ql.backends',
    'brother_ql.backends.pyusb', 
    'brother_ql.backends.linux_kernel',
    'brother_ql.conversion',
    'brother_ql.raster'
]
hiddenimports.extend(brother_imports)

# QR Code
qr_imports = [
    'qrcode',
    'qrcode.image.pil'
]
hiddenimports.extend(qr_imports)

# Otros
other_imports = [
    'io',
    'csv',
    'datetime',
    'platform',
    'subprocess',
    'tempfile'
]
hiddenimports.extend(other_imports)

# Recopilar submódulos
hiddenimports.extend(collect_submodules('PIL'))
hiddenimports.extend(collect_submodules('tkinter'))

# Datos adicionales
datas = []

# Agregar datos de PIL si existen
try:
    datas.extend(collect_data_files('PIL', include_py_files=False))
except:
    pass

# Agregar icono
if os.path.exists('icono-agriQR.png'):
    datas.append(('icono-agriQR.png', '.'))

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SistemaEtiquetasAgriQR-Linux',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icono-agriQR.png'
)