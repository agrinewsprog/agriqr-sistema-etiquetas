"""
🏢 SISTEMA PROFESIONAL DE IMPRESIÓN DE ETIQUETAS QR
📋 Control de Acceso por Eventos - Brother QL Series
🔧 Stack: Tkinter, Pillow, qrcode, win32print, mysql-connector-python

Desarrollado para gestión profesional de eventos con validación de accesos
y control de impresión de credenciales personalizadas.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import qrcode
import mysql.connector
import csv
import io
from datetime import datetime
from PIL import ImageDraw, ImageFont
import sys
import os
import platform

# =====================================================
# 🌍 DETECCIÓN DE SISTEMA OPERATIVO
# =====================================================
CURRENT_OS = platform.system()
IS_WINDOWS = CURRENT_OS == "Windows"
IS_MACOS = CURRENT_OS == "Darwin"
IS_LINUX = CURRENT_OS == "Linux"

# Importaciones condicionales para Windows
if IS_WINDOWS:
    try:
        import win32print
        PRINTING_AVAILABLE = True
    except ImportError:
        PRINTING_AVAILABLE = False
        print("⚠️  win32print no disponible. Funcionalidad de impresión limitada.")
else:
    PRINTING_AVAILABLE = False
    print(f"🌍 Sistema detectado: {CURRENT_OS}")
    print("📱 Modo multiplataforma: Impresión deshabilitada, guardado de etiquetas habilitado")

# Importaciones condicionales para MySQL
try:
    import pymysql
    PYMYSQL_AVAILABLE = True
    print("✅ PyMySQL disponible para conexiones MySQL")
except ImportError:
    PYMYSQL_AVAILABLE = False
    print("📌 PyMySQL no disponible, usando solo mysql.connector")

# Importaciones condicionales para Brother QL (Mac/Linux)
if not IS_WINDOWS:
    try:
        import brother_ql
        BROTHER_QL_AVAILABLE = True
        print("✅ brother_ql disponible para impresión directa")
    except ImportError:
        BROTHER_QL_AVAILABLE = False
        print("⚠️ brother_ql no disponible. Instalar con: pip install brother_ql")

# =====================================================
# 🔤 SISTEMA DE FUENTES MULTIPLATAFORMA
# =====================================================
def get_font_path(font_name, is_bold=False):
    """Obtiene la ruta de fuente según el sistema operativo"""
    if IS_WINDOWS:
        # Windows: mantener exactamente como está funcionando
        if is_bold:
            return 'C:/Windows/Fonts/arialbd.ttf'
        else:
            return 'C:/Windows/Fonts/arial.ttf'
    elif IS_MACOS:
        # macOS: fuentes del sistema
        if font_name.lower() == 'arial':
            return '/System/Library/Fonts/Arial.ttf'
        else:
            return '/System/Library/Fonts/Helvetica.ttc'
    else:  # Linux
        # Linux: buscar fuentes comunes
        common_fonts = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            '/usr/share/fonts/TTF/arial.ttf',
            '/System/Fonts/arial.ttf'
        ]
        for font_path in common_fonts:
            if os.path.exists(font_path):
                return font_path
        return None

def load_fonts():
    """Carga las fuentes según el sistema operativo"""
    try:
        if IS_WINDOWS:
            # Windows: código exacto original que funciona
            font_name = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 95)
            font_empresa = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 60)
            font_dias = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 60)
            font_entrada_evento = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 45)
        else:
            # Mac/Linux: fuentes alternativas
            font_path = get_font_path('arial')
            if font_path and os.path.exists(font_path):
                font_name = ImageFont.truetype(font_path, 95)
                font_empresa = ImageFont.truetype(font_path, 60)
                font_dias = ImageFont.truetype(font_path, 60)
                font_entrada_evento = ImageFont.truetype(font_path, 45)
            else:
                # Fallback a fuente por defecto
                font_name = font_empresa = font_dias = font_entrada_evento = ImageFont.load_default()
                
        return font_name, font_empresa, font_dias, font_entrada_evento
    except Exception as e:
        print(f"⚠️  Error cargando fuentes: {e}")
        # Fallback universal
        default_font = ImageFont.load_default()
        return default_font, default_font, default_font, default_font

# =====================================================
# 🎨 CONFIGURACIÓN DE TEMA PROFESIONAL
# =====================================================
class ColoresTema:
    # Paleta corporativa moderna
    PRIMARY = "#2C3E50"      # Azul oscuro profesional
    SECONDARY = "#3498DB"    # Azul brillante
    SUCCESS = "#27AE60"      # Verde éxito
    DANGER = "#E74C3C"       # Rojo error
    WARNING = "#F39C12"      # Naranja advertencia
    INFO = "#17A2B8"         # Azul información
    
    # Neutrales
    LIGHT = "#ECF0F1"        # Gris claro
    DARK = "#2C3E50"         # Oscuro
    WHITE = "#FFFFFF"        # Blanco
    GRAY = "#7F8C8D"         # Gris medio
    
    # Gradientes y efectos
    HOVER = "#34495E"        # Hover efecto
    BORDER = "#BDC3C7"       # Bordes sutiles

# =====================================================
# 📊 CONFIGURACIÓN PROFESIONAL
# =====================================================

# CONFIGURACIÓN
DB_CONFIG = {
    'host': '148.113.211.234',
    'user': 'agribusi_acr3D1t',  # Prueba con root temporalmente
    'password': 'tTe}1*d$Kz*R',  # Cambia por la contraseña de root
    'database': 'agribusi_acreditacion',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci',
    'use_unicode': True,
    'autocommit': True,
    'connect_timeout': 10,
    'sql_mode': '',
    'init_command': "SET sql_mode=''"
}

# CONFIGURACIÓN BASE DE DATOS DE EVENTOS
DB_CONFIG_EVENTOS = {
    'host': '148.113.211.234',
    'user': 'agribusi_acr3D1t',
    'password': 'tTe}1*d$Kz*R',
    'database': 'agribusi_3MpR3s4',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci',
    'use_unicode': True,
    'autocommit': True,
    'connect_timeout': 10,
    'sql_mode': '',
    'init_command': "SET sql_mode=''"
}

PRINTER_IDENTIFIER = 'QL-800'  # Nombre del driver instalado en Windows
LABEL_TYPE = 'DK-11201'        # 29x90 mm
AUTO_MODE = True               # Cambia a False para modo manual
LOG_FILE = 'log_impresiones.csv'
ACCESOS_LOG_FILE = 'log_accesos.csv'  # Nuevo archivo para log de accesos

# Variables globales para eventos seleccionados
EVENTOS_ACTIVOS = []  # Lista de IDs de eventos activos

def validar_usuario_evento(usuario_data, eventos_activos):
    """Valida si el usuario pertenece a alguno de los eventos activos."""
    evento_usuario = usuario_data.get('Evento')
    if not evento_usuario or not eventos_activos:
        return False, "No hay eventos activos seleccionados"
    
    # Convertir evento_usuario a entero si es string
    try:
        evento_usuario_id = int(evento_usuario)
    except (ValueError, TypeError):
        return False, f"ID de evento inválido: {evento_usuario}"
    
    if evento_usuario_id in eventos_activos:
        return True, "Acceso autorizado"
    else:
        return False, f"Usuario no autorizado para eventos activos. Su evento: {evento_usuario_id}"

def log_acceso(datos, autorizado, razon=""):
    """Registra los accesos (autorizados y no autorizados)."""
    try:
        with open(ACCESOS_LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                datos.get('idUsuario', ''),
                datos.get('Nombrecompleto', ''),
                datos.get('Empresa', ''),
                datos.get('Evento', ''),
                "AUTORIZADO" if autorizado else "DENEGADO",
                razon,
                ','.join(map(str, EVENTOS_ACTIVOS))  # Eventos activos en ese momento
            ])
    except Exception as e:
        print(f"Error al escribir log de acceso: {e}")

def buscar_asistente(id_asistente):
    """Busca un asistente en la base de datos con conexión robusta."""
    try:
        print(f"🔍 Buscando asistente ID: {id_asistente}...")
        
        # Intentar con PyMySQL primero
        try:
            import pymysql
            conn = pymysql.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database'],
                connect_timeout=10
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asistentes WHERE idUsuario=%s", (id_asistente,))
            fila = cursor.fetchone()
            
            if fila:
                cursor.execute("DESCRIBE asistentes")
                columnas = [desc[0] for desc in cursor.fetchall()]
                row = {columnas[i]: fila[i] for i in range(min(len(fila), len(columnas)))}
            else:
                row = None
                
            cursor.close()
            conn.close()
            
            if row:
                print(f"✅ Asistente encontrado con PyMySQL")
            else:
                print(f"⚠️ Asistente no encontrado")
            return row
            
        except ImportError:
            print("📌 PyMySQL no disponible, usando mysql.connector con charset latin1...")
            # Si no está disponible PyMySQL, usar mysql.connector básico
            conn = mysql.connector.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database'],
                charset='latin1'
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asistentes WHERE idUsuario=%s", (id_asistente,))
            fila = cursor.fetchone()
            
            if fila:
                cursor.execute("DESCRIBE asistentes")
                columnas = [desc[0] for desc in cursor.fetchall()]
                row = {columnas[i]: fila[i] for i in range(min(len(fila), len(columnas)))}
            else:
                row = None
                
            cursor.close()
            conn.close()
            
            if row:
                print(f"✅ Asistente encontrado con mysql.connector")
            else:
                print(f"⚠️ Asistente no encontrado")
            return row
            
    except Exception as e:
        print(f"❌ Error al buscar asistente: {e}")
        return None

def obtener_nombre_evento(evento_id, eventos_cargados=None):
    """Obtiene el nombre del evento desde los eventos cargados en memoria."""
    if not evento_id:
        return "Evento no especificado"
    
    try:
        evento_id = int(evento_id)
    except (ValueError, TypeError):
        return "Evento no especificado"
    
    # Si no se pasan eventos, intentar obtener los eventos activos
    if eventos_cargados is None:
        # Esta función será llamada desde el contexto de la clase, 
        # por lo que necesitamos una instancia para obtener los eventos
        return f"Evento ID: {evento_id}"
    
    # Buscar en los eventos cargados
    for evento in eventos_cargados:
        if evento.get('id') == evento_id:
            return evento.get('Nombre', f"Evento ID: {evento_id}")
    
    return f"Evento ID: {evento_id}"

def marcar_comida(id_usuario):
    """Marca comida = 1 en la tabla de asistentes para el usuario especificado."""
    try:
        print(f"🍽️ Marcando comida para usuario ID: {id_usuario}...")
        
        # Intentar en ambas bases de datos
        for config_name, config in [("principal", DB_CONFIG), ("eventos", DB_CONFIG_EVENTOS)]:
            try:
                # Intentar con PyMySQL primero
                try:
                    import pymysql
                    conn = pymysql.connect(
                        host=config['host'],
                        user=config['user'],
                        password=config['password'],
                        database=config['database'],
                        connect_timeout=10
                    )
                    
                    cursor = conn.cursor()
                    cursor.execute("UPDATE asistentes SET comida = 1 WHERE idUsuario = %s", (id_usuario,))
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        print(f"✅ Comida marcada exitosamente para usuario {id_usuario} en base {config_name}")
                        cursor.close()
                        conn.close()
                        return True
                    else:
                        print(f"🔍 Usuario {id_usuario} no encontrado en base {config_name}")
                        
                    cursor.close()
                    conn.close()
                    
                except ImportError:
                    print(f"📌 PyMySQL no disponible, usando mysql.connector en base {config_name}...")
                    # Fallback con mysql.connector
                    import mysql.connector
                    conn = mysql.connector.connect(
                        host=config['host'],
                        user=config['user'],
                        password=config['password'],
                        database=config['database'],
                        charset='latin1'
                    )
                    
                    cursor = conn.cursor()
                    cursor.execute("UPDATE asistentes SET comida = 1 WHERE idUsuario = %s", (id_usuario,))
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        print(f"✅ Comida marcada exitosamente para usuario {id_usuario} en base {config_name}")
                        cursor.close()
                        conn.close()
                        return True
                    else:
                        print(f"🔍 Usuario {id_usuario} no encontrado en base {config_name}")
                        
                    cursor.close()
                    conn.close()
                    
            except Exception as e:
                print(f"❌ Error conectando a base {config_name}: {e}")
                continue
        
        # Si llegamos aquí, no se encontró en ninguna base
        print(f"⚠️ Usuario {id_usuario} no encontrado en ninguna base de datos")
        return False
            
    except Exception as e:
        print(f"❌ Error al marcar comida para usuario {id_usuario}: {e}")
        return False

def generar_etiqueta(datos, nombre_evento=None):
    from PIL import Image, ImageDraw, ImageFont
    import qrcode

    nombre = datos['Nombrecompleto']
    apellidos = datos['apellidos']
    empresa = datos['Empresa']
    dias = datos['Dia']
    id_usuario = datos['idUsuario']
    tipo_entrada = datos.get('entrada', 'General')  # Campo entrada
    
    # Si no se pasa el nombre del evento, usar valor por defecto
    if nombre_evento is None:
        nombre_evento = "Evento no especificado"

    PRINT_WIDTH = 696   # ancho físico (62 mm a 300 dpi)
    LARGO = 1200        # largo etiqueta
    W, H = LARGO, PRINT_WIDTH
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)

    # Cargar fuentes según el sistema operativo
    font_name, font_empresa, font_dias, font_entrada_evento = load_fonts()

    pad = 25
    qr_ancho = int(W * 0.40)
    texto_w = W - qr_ancho - (pad * 3)
    texto_x = pad
    y_pos = pad

    def wrap(text, font, max_w):
        palabras, lineas, actual = text.split(), [], ""
        for p in palabras:
            prueba = (actual + " " + p).strip()
            if draw.textlength(prueba, font=font) <= max_w:
                actual = prueba
            else:
                if actual: lineas.append(actual)
                actual = p
        if actual: lineas.append(actual)
        return lineas

    # NOMBRE
    for linea in wrap(nombre + " " + apellidos, font_name, texto_w)[:2]:
        draw.text((texto_x, y_pos), linea, font=font_name, fill='black')
        y_pos += 110  # más separación

    # EMPRESA
    for linea in wrap(empresa, font_empresa, texto_w)[:3]:
        draw.text((texto_x, y_pos), linea, font=font_empresa, fill='black')
        y_pos += 90  # más separación

    # TIPO DE ENTRADA
    draw.text((texto_x, y_pos), f"{tipo_entrada}", font=font_entrada_evento, fill='black')
    y_pos += 60  # espaciado reducido para fuente más pequeña

    # EVENTO
    for linea in wrap(f" - {nombre_evento}", font_entrada_evento, texto_w)[:2]:
        draw.text((texto_x, y_pos), linea, font=font_entrada_evento, fill='black')
        y_pos += 60  # espaciado reducido para fuente más pequeña

    # DÍAS
    draw.text((texto_x, y_pos), f"{dias}", font=font_dias, fill='black')

    # QR (más pequeño: 75% del alto disponible)
    qr_size = int((H - pad*2) * 0.75)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10, border=2
    )
    qr.add_data(str(id_usuario))
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").resize((qr_size, qr_size))

    qr_x = W - qr_ancho + (qr_ancho - qr_size)//2 - pad
    qr_y = (H - qr_size)//2
    img.paste(qr_img, (qr_x, qr_y))

    return img



def imprimir_etiqueta(img):
    """Imprime en Brother QL en TODAS las plataformas"""
    try:
        # Intentar impresión Brother QL en cualquier sistema operativo
        if IS_WINDOWS:
            # Windows: usar win32print
            return imprimir_etiqueta_windows(img)
        else:
            # Mac/Linux: usar brother_ql directamente
            return imprimir_etiqueta_brother_ql(img)
            
    except Exception as e:
        print(f"❌ Error de impresión: {e}")
        # Solo como último recurso, guardar archivo
        print("⚠️ Impresión falló, guardando archivo como backup...")
        return guardar_etiqueta_archivo(img)

def imprimir_etiqueta_brother_ql(img):
    """Imprime usando diferentes estrategias para Linux/Mac"""
    try:
        print("🖨️ Intentando impresión en Linux...")
        
        # Estrategia 1: CUPS (Common Unix Printing System) - más confiable en Linux
        if imprimir_con_cups(img):
            return True
        
        # Estrategia 2: lp command directo
        if imprimir_con_lp(img):
            return True
        
        # Estrategia 3: brother_ql como último recurso (con manejo de errores)
        try:
            print("🔄 Intentando con brother_ql (puede fallar)...")
            return imprimir_con_brother_ql_legacy(img)
        except Exception as e:
            print(f"brother_ql falló como esperado: {e}")
            
        # Si todo falla, guardar archivo (ya es lo que hacía antes)
        raise Exception("Todas las estrategias de impresión fallaron. Guardando como archivo.")
        
    except Exception as e:
        raise Exception(f"Error en impresión Linux: {str(e)}")

def imprimir_con_cups(img):
    """Intenta imprimir usando CUPS (sistema de impresión estándar Linux)"""
    try:
        import subprocess
        import tempfile
        import os
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            
        # Guardar imagen en archivo temporal
        img.save(tmp_path, "PNG", dpi=(300, 300))
        
        # Buscar impresoras Brother QL disponibles
        try:
            result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True, timeout=5)
            impresoras_disponibles = result.stdout
            
            # Buscar impresoras Brother
            impresoras_brother = []
            for linea in impresoras_disponibles.split('\n'):
                if 'Brother' in linea and ('QL-' in linea or 'ql-' in linea):
                    # Extraer nombre de impresora
                    partes = linea.split()
                    if len(partes) >= 2:
                        impresoras_brother.append(partes[1])
            
            if not impresoras_brother:
                print("🔍 No se encontraron impresoras Brother QL en CUPS")
                return False
            
            # Intentar imprimir en la primera impresora Brother encontrada
            impresora = impresoras_brother[0]
            print(f"🖨️ Imprimiendo en: {impresora}")
            
            # Comando lp con parámetros específicos para etiquetas
            cmd = [
                'lp',
                '-d', impresora,
                '-o', 'media=Custom.62x29mm',  # Tamaño de etiqueta Brother
                '-o', 'fit-to-page',
                '-o', 'orientation-requested=3',  # Paisaje
                tmp_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            # Limpiar archivo temporal
            try:
                os.unlink(tmp_path)
            except:
                pass
            
            if result.returncode == 0:
                print("✅ ¡Impresión enviada exitosamente con CUPS!")
                return True
            else:
                print(f"❌ Error CUPS: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏱️ Timeout ejecutando comandos CUPS")
            return False
        except Exception as e:
            print(f"❌ Error ejecutando CUPS: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error configurando CUPS: {e}")
        return False

def imprimir_con_lp(img):
    """Intenta imprimir usando comando lp directo"""
    try:
        import subprocess
        import tempfile
        import os
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            
        # Guardar imagen optimizada para impresión
        img.save(tmp_path, "PNG", dpi=(300, 300), optimize=True)
        
        # Intentar imprimir con lp genérico
        try:
            cmd = ['lp', '-o', 'fit-to-page', tmp_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            # Limpiar archivo temporal
            try:
                os.unlink(tmp_path)
            except:
                pass
            
            if result.returncode == 0:
                print("✅ ¡Impresión enviada exitosamente con lp!")
                return True
            else:
                print(f"❌ Error lp: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏱️ Timeout ejecutando lp")
            return False
        except Exception as e:
            print(f"❌ Error ejecutando lp: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error configurando lp: {e}")
        return False

def imprimir_con_brother_ql_legacy(img):
    """Método brother_ql original (puede fallar con Pillow nuevo)"""
    try:
        from brother_ql import BrotherQLRaster, create_label
        from brother_ql.backends import backend_factory, guess_backend
        
        # Detectar impresora Brother QL
        backend = guess_backend("usb://")
        if not backend:
            return False
        
        # Crear raster
        qlr = BrotherQLRaster('QL-700')
        
        # Convertir imagen a formato Brother QL
        instructions = create_label(qlr, img, '62')
        
        # Enviar a impresora
        backend.write(instructions)
        backend.dispose()
        
        print("✅ ¡Impresión enviada exitosamente con brother_ql!")
        return True
        
    except Exception as e:
        print(f"brother_ql legacy falló: {e}")
        return False

def imprimir_etiqueta_windows(img):
    """Imprime usando win32print (método Windows nativo más confiable)."""
    try:
        import win32print
        import win32ui
        from PIL import ImageWin
        import tempfile
        import os
        
        # Buscar impresoras Brother instaladas
        impresoras = []
        for printer_info in win32print.EnumPrinters(2):
            nombre = printer_info[2]
            if 'Brother' in nombre and ('QL-600' in nombre or 'QL-700' in nombre or 'QL-800' in nombre):
                impresoras.append(nombre)
        
        if not impresoras:
            raise Exception("No se encontró ninguna impresora Brother QL instalada en Windows. Instala el driver oficial.")
        
        nombre_impresora = impresoras[0]
        print(f"Usando impresora: {nombre_impresora}")
        
        # Crear contexto de impresión
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(nombre_impresora)
        
        # Obtener resolución de la impresora
        horz_res = hDC.GetDeviceCaps(8)  # HORZRES 
        vert_res = hDC.GetDeviceCaps(10) # VERTRES 
        print(f"Resolución impresora: {horz_res}x{vert_res} píxeles")
        
        # Preparar imagen para impresión
        dib = ImageWin.Dib(img)
        
        # Iniciar documento
        hDC.StartDoc("Etiqueta QR")
        hDC.StartPage()
        
        # Calcular tamaño manteniendo proporciones
        img_width, img_height = img.size
        scale_x = horz_res / img_width
        scale_y = vert_res / img_height
        scale = min(scale_x, scale_y)
        
        final_width = int(img_width * scale)
        final_height = int(img_height * scale)
        
        # Centrar en el papel
        x_offset = (horz_res - final_width) // 2
        y_offset = (vert_res - final_height) // 2
        
        # Imprimir manteniendo proporciones
        dib.draw(hDC.GetHandleOutput(), (x_offset, y_offset, x_offset + final_width, y_offset + final_height))
        
        hDC.EndPage()
        hDC.EndDoc()
        
        print("¡Impresión enviada exitosamente!")
        
    except ImportError:
        raise Exception("Instala pywin32: pip install pywin32")
    except Exception as e:
        print(f"Error en impresión: {e}")
        raise Exception(f"Error al imprimir: {str(e)}")

def guardar_etiqueta_archivo(img):
    """Guarda la etiqueta como archivo para Mac/Linux - SIMULA IMPRESIÓN"""
    try:
        # Crear directorio de etiquetas si no existe
        etiquetas_dir = os.path.join(os.path.expanduser("~"), "Etiquetas_QR")
        if not os.path.exists(etiquetas_dir):
            os.makedirs(etiquetas_dir)
        
        # Generar nombre único con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"etiqueta_qr_{timestamp}.png"
        filepath = os.path.join(etiquetas_dir, filename)
        
        # Guardar imagen con alta calidad
        img.save(filepath, "PNG", dpi=(300, 300), optimize=True)
        
        print(f"✅ Etiqueta 'impresa' (guardada) en: {filepath}")
        
        # Crear también una versión PDF si es posible
        try:
            pdf_path = filepath.replace('.png', '.pdf')
            img_rgb = img.convert('RGB')
            img_rgb.save(pdf_path, "PDF", dpi=(300, 300))
            print(f"📄 También guardada como PDF: {pdf_path}")
        except Exception as pdf_error:
            print(f"⚠️ No se pudo crear PDF: {pdf_error}")
        
        # Crear archivo de instrucciones si no existe
        instrucciones_path = os.path.join(etiquetas_dir, "INSTRUCCIONES_IMPRESION.txt")
        if not os.path.exists(instrucciones_path):
            with open(instrucciones_path, 'w', encoding='utf-8') as f:
                f.write("""🖨️ INSTRUCCIONES PARA IMPRIMIR ETIQUETAS EN LINUX

Las etiquetas se guardan aquí porque la impresión directa en Linux puede requerir configuración adicional.

PARA IMPRIMIR:
1. Conecta tu impresora Brother QL (QL-600, QL-700, QL-800)
2. Instala el driver oficial de Brother si no lo has hecho
3. Abre el archivo PNG o PDF con el visor de imágenes
4. Imprime con estas configuraciones:
   - Tamaño: 62mm x 29mm (o tamaño personalizado)
   - Orientación: Horizontal (paisaje)
   - Ajustar a página: SÍ
   - Sin márgenes

CONFIGURACIÓN CUPS (OPCIONAL):
Para impresión automática, configura tu impresora en CUPS:
1. Abre http://localhost:631 en tu navegador
2. Añade tu impresora Brother QL
3. Configura el tamaño de papel a 62x29mm

ALTERNATIVA:
Usa el comando: lp -d NombreImpresora -o fit-to-page archivo.png
""")
            print(f"📝 Instrucciones creadas en: {instrucciones_path}")
        
        return filepath
        
    except Exception as e:
        print(f"Error guardando etiqueta: {e}")
        raise Exception(f"Error al imprimir etiqueta: {str(e)}")

def log_impresion(datos):
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            datos.get('idUsuario'),
            datos.get('Nombrecompleto'),
            datos.get('apellidos'),
            datos.get('Empresa'),
            datos.get('Evento', ''),
            datos.get('Dia')
        ])

# =====================================================
# 🏢 CLASE PRINCIPAL - INTERFAZ PROFESIONAL
# =====================================================
class SistemaEtiquetasProfesional(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configurar_ventana_principal()
        self.configurar_tema()
        self.auto_mode = tk.BooleanVar(value=AUTO_MODE)
        self.datos_actual = None
        self.img_etiqueta = None
        self.log_actividad = []  # Lista para guardar toda la actividad
        
        # Crear interfaz profesional
        self.crear_interfaz_profesional()
        self.focus_entry()
        self.after(1000, self.mostrar_bienvenida)
        
        # Estado de conexión
        self.estado_conexion = False
        self.verificar_conexiones_inicial()

    def configurar_ventana_principal(self):
        """Configura la ventana principal con estilo profesional."""
        self.title("🏢 Sistema Profesional de Etiquetas QR - v2.0")
        
        # Configurar para maximizado por defecto pero en modo ventana
        try:
            self.state('zoomed')  # Maximiza la ventana en Windows
        except:
            # Fallback para sistemas que no soporten 'zoomed'
            self.geometry('1200x800')  # Tamaño grande como alternativa
        
        self.resizable(True, True)  # Permitir redimensionar
        self.minsize(750, 600)      # Tamaño mínimo
        
        # Configurar icono corporativo
        try:
            # Buscar archivos de icono comunes
            import os
            posibles_iconos = [
                'icono-agriQR.ico',  # El icono específico que agregaste
                'agrinews.ico',
                'logo.ico', 
                'icon.ico',
                'app.ico',
                'programa.ico'
            ]
            
            icono_encontrado = None
            for icono in posibles_iconos:
                if os.path.exists(icono):
                    icono_encontrado = icono
                    break
            
            if icono_encontrado:
                self.iconbitmap(icono_encontrado)
                print(f"✅ Icono corporativo cargado: {icono_encontrado}")
            else:
                print("ℹ️ No se encontró archivo de icono")
                
        except Exception as e:
            print(f"⚠️ No se pudo cargar el icono: {e}")
        
        # No centrar ventana - se abre maximizada por defecto
        # self.center_window()

    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def configurar_tema(self):
        """Aplica tema profesional a la aplicación."""
        style = ttk.Style()
        
        # Configurar estilo general
        self.configure(bg=ColoresTema.LIGHT)
        
        # Configurar estilos de ttk
        style.configure('Titulo.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       foreground=ColoresTema.PRIMARY,
                       background=ColoresTema.LIGHT)
        
        style.configure('Subtitulo.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=ColoresTema.SECONDARY,
                       background=ColoresTema.LIGHT)
        
        style.configure('Info.TLabel',
                       font=('Segoe UI', 10),
                       foreground=ColoresTema.GRAY,
                       background=ColoresTema.LIGHT)

    def crear_interfaz_profesional(self):
        """Crea la interfaz principal con diseño profesional."""
        # Frame principal con padding elegante
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Header corporativo
        self.crear_header()
        
        # Panel de control de eventos (parte superior)
        self.crear_panel_eventos()
        
        # Separador elegante
        sep1 = ttk.Separator(self.main_frame, orient='horizontal')
        sep1.pack(fill='x', pady=15)
        
        # Panel de escaneo principal
        self.crear_panel_escaneo()
        
        # Separador elegante
        sep2 = ttk.Separator(self.main_frame, orient='horizontal')
        sep2.pack(fill='x', pady=15)
        
        # Panel de vista previa y control
        self.crear_panel_preview_control()
        
        # Footer con controles administrativos
        self.crear_footer()

    def crear_header(self):
        """Crea el header profesional de la aplicación."""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Título principal
        titulo = ttk.Label(header_frame, 
                          text="🏢 SISTEMA DE ETIQUETAS agriNews©",
                          style='Titulo.TLabel')
        titulo.pack(anchor='center')
        
        # Subtítulo
        subtitulo = ttk.Label(header_frame,
                             text="Control de Acceso para Eventos - agriNews©",
                             style='Subtitulo.TLabel')
        subtitulo.pack(anchor='center', pady=(5, 0))
        
        # Indicador de estado
        self.estado_frame = ttk.Frame(header_frame)
        self.estado_frame.pack(anchor='center', pady=10)
        
        self.estado_label = ttk.Label(self.estado_frame, 
                                     text="🔴 Inicializando sistema...",
                                     style='Info.TLabel')
        self.estado_label.pack()

    def crear_panel_eventos(self):
        """Crea el panel profesional de gestión de eventos."""
        eventos_frame = ttk.LabelFrame(self.main_frame, 
                                      text="📋 GESTIÓN DE EVENTOS", 
                                      padding=15)
        eventos_frame.pack(fill='x', pady=(0, 10))
        
        # Info eventos activos
        info_frame = ttk.Frame(eventos_frame)
        info_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(info_frame, 
                 text="Eventos activos para validación de acceso:",
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        
        self.eventos_text = tk.Text(info_frame, height=4, 
                                   font=('Consolas', 9),
                                   bg=ColoresTema.WHITE,
                                   fg=ColoresTema.DARK,
                                   relief='solid', borderwidth=1,
                                   state='disabled')
        self.eventos_text.pack(fill='x', pady=(5, 0))
        
        # Botones de control elegantes
        control_frame = ttk.Frame(eventos_frame)
        control_frame.pack(fill='x', pady=(10, 0))
        
        self.btn_seleccionar = ttk.Button(control_frame, 
                                         text="🎯 Seleccionar Eventos",
                                         command=self.seleccionar_eventos)
        self.btn_seleccionar.pack(side='left', padx=(0, 10))
        
        self.btn_log_accesos = ttk.Button(control_frame,
                                         text="📊 Ver Log de Accesos", 
                                         command=self.ver_log_accesos)
        self.btn_log_accesos.pack(side='left', padx=(0, 10))
        
        self.btn_tabla_usuarios = ttk.Button(control_frame,
                                           text="👥 Tabla de Usuarios", 
                                           command=self.mostrar_tabla_usuarios)
        self.btn_tabla_usuarios.pack(side='left', padx=(0, 10))
        
        self.btn_refresh = ttk.Button(control_frame,
                                     text="🔄 Actualizar",
                                     command=self.actualizar_eventos_display)
        self.btn_refresh.pack(side='left')

    def crear_panel_escaneo(self):
        """Crea el panel principal de escaneo."""
        escaneo_frame = ttk.LabelFrame(self.main_frame,
                                      text="🔍 ESCÁNER DE CÓDIGOS",
                                      padding=15)
        escaneo_frame.pack(fill='x', pady=(0, 10))
        
        # Campo principal de escaneo
        ttk.Label(escaneo_frame, 
                 text="Escanee el código de barras o introduzca el ID:",
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        
        self.entry = ttk.Entry(escaneo_frame, 
                              font=('Segoe UI', 20, 'bold'),
                              width=30)
        self.entry.pack(fill='x', pady=(0, 10))
        self.entry.bind('<Return>', self.on_scan)
        self.entry.bind('<FocusIn>', self.on_entry_focus)
        
        # Controles adicionales
        controles = ttk.Frame(escaneo_frame)
        controles.pack(fill='x')
        
        self.auto_check = ttk.Checkbutton(controles, 
                                         text="🖨️ Impresión automática",
                                         variable=self.auto_mode)
        self.auto_check.pack(side='left')
        
        # Búsqueda manual
        manual_frame = ttk.Frame(controles)
        manual_frame.pack(side='right')
        
        self.manual_entry = ttk.Entry(manual_frame, font=('Segoe UI', 12), width=15)
        self.manual_entry.pack(side='left', padx=(0, 5))
        
        self.btn_buscar = ttk.Button(manual_frame,
                                    text="🔍 Buscar",
                                    command=self.on_buscar_manual)
        self.btn_buscar.pack(side='left')
        
    def crear_panel_preview_control(self):
        """Crea el panel de vista previa y controles."""
        preview_frame = ttk.LabelFrame(self.main_frame,
                                      text="👁️ VISTA PREVIA Y CONTROL",
                                      padding=15)
        preview_frame.pack(fill='x', pady=(0, 10))
        
        # Container para la vista previa con tamaño controlado
        preview_container = tk.Frame(preview_frame, 
                                   bg=ColoresTema.WHITE,
                                   relief='solid', 
                                   borderwidth=2,
                                   width=400,
                                   height=250)
        preview_container.pack(pady=(0, 15), padx=20)
        preview_container.pack_propagate(False)  # Mantener tamaño fijo
        
        # Vista previa de la etiqueta - tamaño controlado
        self.preview_lbl = tk.Label(preview_container,
                                   text="📄 La vista previa aparecerá aquí\n🔍 Escanee un código",
                                   font=('Segoe UI', 12),
                                   fg=ColoresTema.GRAY,
                                   bg=ColoresTema.WHITE,
                                   justify='center')
        self.preview_lbl.pack(expand=True)
        
        # Controles de impresión
        control_frame = ttk.Frame(preview_frame)
        control_frame.pack(fill='x')
        
        # Botón de impresión universal
        self.btn_print = ttk.Button(control_frame,
                                   text="🖨️ IMPRIMIR ETIQUETA",
                                   command=self.on_print)
        self.btn_print.pack(side='left', padx=(0, 10))
        self.btn_print['state'] = 'disabled'
        
        # Información adicional
        info_frame = ttk.Frame(control_frame)
        info_frame.pack(side='right')
        
        self.info_label = ttk.Label(info_frame,
                                   text="",
                                   style='Info.TLabel')
        self.info_label.pack()

    def crear_footer(self):
        """Crea el footer con controles administrativos."""
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill='x', pady=(10, 0))
        
        # Separador
        ttk.Separator(footer_frame, orient='horizontal').pack(fill='x', pady=(0, 10))
        
        # Controles administrativos
        admin_frame = ttk.Frame(footer_frame)
        admin_frame.pack(fill='x')
        
        self.btn_help = ttk.Button(admin_frame,
                                  text="❓ Ayuda",
                                  command=self.mostrar_ayuda)
        self.btn_help.pack(side='left', padx=(0, 10))
        
        self.btn_test_db = ttk.Button(admin_frame,
                                     text="🔌 Probar Conexión",
                                     command=self.probar_conexion_bd)
        self.btn_test_db.pack(side='left', padx=(0, 10))
        
        # Info de sistema
        sistema_frame = ttk.Frame(admin_frame)
        sistema_frame.pack(side='right')
        
        version_label = ttk.Label(sistema_frame,
                                 text="v2.0 Professional • Brother QL Series",
                                 style='Info.TLabel')
        version_label.pack()
        
        # Inicializar eventos
        self.actualizar_eventos_display()
        
    # =====================================================
    # 🎯 MÉTODOS DE CONTROL PRINCIPAL
    # =====================================================
    
    def focus_entry(self):
        """Enfoca el campo de entrada principal."""
        self.entry.focus_set()
        
    def on_entry_focus(self, event):
        """Maneja el evento cuando el campo de entrada obtiene el foco."""
        self.entry.select_range(0, 'end')
        
    def mostrar_bienvenida(self):
        """Muestra mensaje de bienvenida profesional."""
        self.log_message("Sistema Profesional de Etiquetas QR iniciado correctamente")
        self.log_message("Listo para procesar códigos de barras")
        if len(EVENTOS_ACTIVOS) > 0:
            self.log_message(f"{len(EVENTOS_ACTIVOS)} evento(s) activo(s) para validación")
        else:
            self.log_message("No hay eventos seleccionados - Seleccione eventos para activar validación", "WARNING")
            
    def verificar_conexiones_inicial(self):
        """Verifica las conexiones iniciales y actualiza el estado."""
        try:
            # Configuración específica para evitar problemas de localización
            config_principal = DB_CONFIG.copy()
            config_principal['raise_on_warnings'] = False
            
            config_eventos = DB_CONFIG_EVENTOS.copy()
            config_eventos['raise_on_warnings'] = False
            
            # Verificar conexión principal
            with mysql.connector.connect(**config_principal) as conn:
                if conn.is_connected():
                    self.estado_conexion = True
                    print("✅ Conexión principal establecida")
                    
            # Verificar conexión de eventos
            with mysql.connector.connect(**config_eventos) as conn:
                if conn.is_connected():
                    print("✅ Conexión de eventos establecida")
                    self.estado_label.config(text="🟢 Sistema operativo - Conexiones activas")
                    return
                    
        except mysql.connector.Error as e:
            self.estado_label.config(text="🔴 Error de conexión MySQL")
            self.log_message(f"Error de conexión MySQL: {str(e)}", "ERROR")
        except Exception as e:
            self.estado_label.config(text="🔴 Error de conexión - Verificar configuración")
            self.log_message(f"Error de conexión: {str(e)}", "ERROR")

    def log_message(self, msg, tipo="INFO"):
        """Registra un mensaje en el log de actividad."""
        # Simplemente registramos en nuestro log de actividad
        self.registrar_actividad(tipo, msg)

    def log_acceso_resultado(self, datos, autorizado, razon):
        """Registra el resultado de un acceso con colores apropiados."""
        if autorizado:
            # Para acceso autorizado, usar los datos reales del usuario
            evento = datos.get('evento', 'N/A')
            msg = f"ACCESO AUTORIZADO | Evento: {evento}"
            self.registrar_actividad("SUCCESS", msg, datos)
        else:
            id_usuario = datos.get('idUsuario', 'ID desconocido') if isinstance(datos, dict) else str(datos)
            msg = f"ACCESO DENEGADO - ID: {id_usuario} | Razón: {razon}"
            self.registrar_actividad("ERROR", msg, datos)
        
    def obtener_eventos_seguro(self):
        """Obtiene eventos con conexión robusta."""
        try:
            self.log_message("Cargando eventos desde base de datos...", "INFO")
            
            # Estrategia principal: PyMySQL
            try:
                import pymysql
                conn = pymysql.connect(
                    host=DB_CONFIG_EVENTOS['host'],
                    user=DB_CONFIG_EVENTOS['user'],
                    password=DB_CONFIG_EVENTOS['password'],
                    database=DB_CONFIG_EVENTOS['database'],
                    connect_timeout=10
                )
                
                cursor = conn.cursor()
                cursor.execute("SELECT id, Nombre, fecha, dia FROM Eventos ORDER BY fecha DESC")
                resultados = cursor.fetchall()
                
                eventos = []
                for r in resultados:
                    eventos.append({
                        'id': r[0],
                        'Nombre': r[1],
                        'fecha': r[2],
                        'dia': r[3]
                    })
                
                cursor.close()
                conn.close()
                
                self.log_message(f"{len(eventos)} eventos cargados con PyMySQL", "SUCCESS")
                return eventos
                
            except ImportError:
                self.log_message("📌 PyMySQL no disponible, usando mysql.connector...", "INFO")
                # Fallback: mysql.connector con charset latin1
                conn = mysql.connector.connect(
                    host=DB_CONFIG_EVENTOS['host'],
                    user=DB_CONFIG_EVENTOS['user'], 
                    password=DB_CONFIG_EVENTOS['password'],
                    database=DB_CONFIG_EVENTOS['database'],
                    charset='latin1'
                )
                
                cursor = conn.cursor()
                cursor.execute("SELECT id, Nombre, fecha, dia FROM Eventos ORDER BY fecha DESC")
                resultados = cursor.fetchall()
                
                eventos = []
                for r in resultados:
                    eventos.append({
                        'id': r[0],
                        'Nombre': r[1],
                        'fecha': r[2], 
                        'dia': r[3]
                    })
                
                cursor.close()
                conn.close()
                
                self.log_message(f"{len(eventos)} eventos cargados con mysql.connector", "SUCCESS")
                return eventos
                
        except Exception as e:
            self.log_message(f"Error al cargar eventos: {str(e)}", "ERROR")
            return []
    
    def seleccionar_eventos(self):
        """Abre ventana para seleccionar múltiples eventos activos."""
        # Intentar múltiples estrategias para obtener eventos
        eventos = self.obtener_eventos_seguro()
        
        if not eventos:
            # Mostrar error más informativo
            messagebox.showerror("Error de Conexión", 
                               "No se pudieron cargar los eventos desde la base de datos.\n\n" +
                               "Posibles causas:\n" +
                               "• Sin conexión a internet\n" +
                               "• Servidor de base de datos no disponible\n" +
                               "• Configuración de red bloqueada\n\n" +
                               "Verifique la conexión y pruebe el botón 'Probar Conexión'")
            return
        
        # Crear ventana de selección
        ventana = tk.Toplevel(self)
        ventana.title("Seleccionar Eventos Activos")
        ventana.geometry("600x400")
        ventana.transient(self)
        ventana.grab_set()
        
        ttk.Label(ventana, text="Selecciona los eventos que estarán activos:").pack(pady=10)
        
        # Frame con scroll para la lista de eventos
        frame = ttk.Frame(ventana)
        frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Variables para checkboxes
        vars_eventos = {}
        
        for evento in eventos:
            var = tk.BooleanVar()
            # Marcar eventos que ya están activos
            if evento['id'] in EVENTOS_ACTIVOS:
                var.set(True)
            vars_eventos[evento['id']] = var
            
            text = f"ID: {evento['id']} - {evento['Nombre']} - {evento['fecha']} - Día: {evento['dia']}"
            chk = ttk.Checkbutton(scrollable_frame, text=text, variable=var)
            chk.pack(anchor='w', pady=2, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones
        botones = ttk.Frame(ventana)
        botones.pack(pady=10)
        
        def guardar_seleccion():
            global EVENTOS_ACTIVOS
            EVENTOS_ACTIVOS = [evento_id for evento_id, var in vars_eventos.items() if var.get()]
            self.actualizar_eventos_display()
            messagebox.showinfo("Éxito", f"Se han activado {len(EVENTOS_ACTIVOS)} eventos")
            ventana.destroy()
        
        def cancelar():
            ventana.destroy()
        
        ttk.Button(botones, text="Guardar", command=guardar_seleccion).pack(side='left', padx=5)
        ttk.Button(botones, text="Cancelar", command=cancelar).pack(side='left', padx=5)

    def actualizar_eventos_display(self):
        """Actualiza la visualización de eventos activos."""
        self.eventos_text.config(state='normal')
        self.eventos_text.delete(1.0, tk.END)
        
        if EVENTOS_ACTIVOS:
            eventos = self.obtener_eventos_seguro()
            eventos_dict = {e['id']: e for e in eventos}
            
            texto = f"Eventos activos ({len(EVENTOS_ACTIVOS)}):\n"
            for evento_id in EVENTOS_ACTIVOS:
                if evento_id in eventos_dict:
                    e = eventos_dict[evento_id]
                    texto += f"• ID: {e['id']} - {e['Nombre']} - {e['fecha']}\n"
                else:
                    texto += f"• ID: {evento_id} (no encontrado)\n"
        else:
            texto = "⚠️ NO HAY EVENTOS ACTIVOS SELECCIONADOS\nTodos los accesos serán denegados."
        
        self.eventos_text.insert(1.0, texto)
        self.eventos_text.config(state='disabled')

    def ver_log_accesos(self):
        """Muestra el log de accesos y actividad del sistema."""
        # Crear ventana de log
        ventana_log = tk.Toplevel(self)
        ventana_log.title("📋 Log de Accesos y Actividad del Sistema")
        ventana_log.geometry("900x700")
        ventana_log.configure(bg=ColoresTema.WHITE)
        ventana_log.resizable(True, True)
        
        # Centrar ventana
        ventana_log.transient(self)
        ventana_log.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(ventana_log, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(main_frame,
                          text="📋 REGISTRO COMPLETO DE ACTIVIDAD",
                          style='Title.TLabel')
        titulo.pack(pady=(0, 15))
        
        # Área de texto con scroll
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill='both', expand=True)
        
        text_area = tk.Text(text_frame,
                           font=('Consolas', 10),
                           bg=ColoresTema.DARK,
                           fg=ColoresTema.WHITE,
                           relief='solid',
                           borderwidth=2,
                           wrap='word')
        
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        # Mostrar actividad de la sesión actual
        contenido = []
        
        # Agregar actividad de la sesión actual (más reciente primero)
        if self.log_actividad:
            contenido.append("=== ACTIVIDAD DE LA SESIÓN ACTUAL ===")
            for entrada in reversed(self.log_actividad):
                contenido.append(entrada)
            contenido.append("")
        
        # Leer también el archivo de accesos si existe
        try:
            with open(ACCESOS_LOG_FILE, 'r', encoding='utf-8') as f:
                contenido_archivo = f.read()
                if contenido_archivo.strip():
                    contenido.append("=== HISTORIAL DE ACCESOS (ARCHIVO CSV) ===")
                    contenido.append("FECHA,ID_USUARIO,NOMBRE,EMPRESA,EVENTO_USUARIO,ESTADO,RAZON,EVENTOS_ACTIVOS")
                    for linea in contenido_archivo.strip().split('\n'):
                        if linea.strip():
                            contenido.append(linea)
        except FileNotFoundError:
            contenido.append("=== HISTORIAL DE ACCESOS ===")
            contenido.append("No hay registros de accesos guardados aún.")
        except Exception as e:
            contenido.append(f"Error leyendo archivo de accesos: {e}")
        
        # Mostrar todo el contenido
        if contenido:
            for linea in contenido:
                text_area.insert('end', linea + '\n')
        else:
            text_area.insert('end', 'No hay actividad registrada.\n')
        
        text_area.configure(state='disabled')
        
        text_area.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botón cerrar
        btn_cerrar = ttk.Button(main_frame,
                               text="✖ Cerrar",
                               command=ventana_log.destroy,
                               style='Danger.TButton')
        btn_cerrar.pack(pady=(15, 0))

    def mostrar_tabla_usuarios(self):
        """Muestra una tabla con todos los usuarios de los eventos seleccionados."""
        if not EVENTOS_ACTIVOS:
            messagebox.showwarning('Advertencia', 'No hay eventos seleccionados.\nPor favor selecciona al menos un evento primero.')
            return
        
        # Obtener eventos una sola vez para reutilizar
        try:
            eventos = self.obtener_eventos_seguro()
            eventos_dict = {e['id']: e for e in eventos}
        except Exception as e:
            messagebox.showerror('Error', f'Error al obtener eventos:\n{str(e)}')
            return
        
        # Obtener usuarios de los eventos activos
        usuarios = self.obtener_usuarios_eventos_activos()
        if not usuarios:
            messagebox.showinfo('Información', 'No se encontraron usuarios para los eventos seleccionados.')
            return
        
        # Crear ventana de tabla
        ventana_tabla = tk.Toplevel(self)
        ventana_tabla.title("👥 Tabla de Usuarios - Pulseras Entregadas")
        ventana_tabla.geometry("1200x700")
        ventana_tabla.configure(bg=ColoresTema.WHITE)
        ventana_tabla.resizable(True, True)
        
        # Centrar ventana
        ventana_tabla.transient(self)
        ventana_tabla.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(ventana_tabla, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título con información de eventos
        eventos_nombres = []
        for evento_id in EVENTOS_ACTIVOS:
            if evento_id in eventos_dict:
                nombre = eventos_dict[evento_id]['Nombre']
                eventos_nombres.append(f"{evento_id}: {nombre}")
            else:
                eventos_nombres.append(f"{evento_id}: No encontrado")
        
        titulo_texto = f"👥 USUARIOS DE EVENTOS SELECCIONADOS\nEventos: {' | '.join(eventos_nombres)}"
        titulo = ttk.Label(main_frame,
                          text=titulo_texto,
                          style='Title.TLabel')
        titulo.pack(pady=(0, 15))
        
        # Frame para la tabla
        tabla_frame = ttk.Frame(main_frame)
        tabla_frame.pack(fill='both', expand=True)
        
        # Crear Treeview con scrollbars
        columns = ('ID', 'Nombre', 'Apellidos', 'Empresa', 'Entrada', 'Evento', 'Pulsera')
        tree = ttk.Treeview(tabla_frame, columns=columns, show='headings', height=20)
        
        # Configurar columnas
        tree.heading('ID', text='ID Usuario')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Apellidos', text='Apellidos')
        tree.heading('Empresa', text='Empresa')
        tree.heading('Entrada', text='Tipo Entrada')
        tree.heading('Evento', text='Evento')
        tree.heading('Pulsera', text='Pulsera Entregada')
        
        # Ajustar ancho de columnas
        tree.column('ID', width=80, minwidth=60)
        tree.column('Nombre', width=120, minwidth=100)
        tree.column('Apellidos', width=120, minwidth=100)
        tree.column('Empresa', width=200, minwidth=150)
        tree.column('Entrada', width=100, minwidth=80)
        tree.column('Evento', width=150, minwidth=120)
        tree.column('Pulsera', width=120, minwidth=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tabla_frame, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Insertar datos (usar eventos_dict para evitar consultas repetidas)
        for usuario in usuarios:
            pulsera_texto = "✅ SÍ" if usuario.get('comida', 0) == 1 else "❌ NO"
            evento_id = usuario.get('Evento', '')
            
            # Obtener nombre del evento desde el diccionario ya cargado
            if evento_id in eventos_dict:
                evento_nombre = eventos_dict[evento_id]['Nombre']
            else:
                evento_nombre = "No encontrado"
            
            tree.insert('', 'end', values=(
                usuario.get('idUsuario', ''),
                usuario.get('Nombrecompleto', ''),
                usuario.get('apellidos', ''),
                usuario.get('Empresa', ''),
                usuario.get('entrada', ''),
                f"{evento_id} - {evento_nombre}",
                pulsera_texto
            ))
        
        # Pack elementos
        tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Frame para estadísticas y botones
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill='x', pady=(15, 0))
        
        # Estadísticas
        total_usuarios = len(usuarios)
        con_pulsera = len([u for u in usuarios if u.get('comida', 0) == 1])
        sin_pulsera = total_usuarios - con_pulsera
        
        stats_text = f"📊 Total: {total_usuarios} usuarios | ✅ Con pulsera: {con_pulsera} | ❌ Sin pulsera: {sin_pulsera}"
        stats_label = ttk.Label(stats_frame, text=stats_text, font=('Arial', 11, 'bold'))
        stats_label.pack(side='left')
        
        # Botón actualizar
        btn_actualizar = ttk.Button(stats_frame,
                                   text="🔄 Actualizar",
                                   command=lambda: self.actualizar_tabla_usuarios_optimizada(tree),
                                   style='Success.TButton')
        btn_actualizar.pack(side='right', padx=(10, 0))
        
        # Botón cerrar
        btn_cerrar = ttk.Button(stats_frame,
                               text="✖ Cerrar",
                               command=ventana_tabla.destroy,
                               style='Danger.TButton')
        btn_cerrar.pack(side='right', padx=(10, 0))

    def obtener_usuarios_eventos_activos(self):
        """Obtiene todos los usuarios de los eventos activos."""
        if not EVENTOS_ACTIVOS:
            return []
        
        usuarios = []
        try:
            import pymysql
            conn = pymysql.connect(**DB_CONFIG)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            # Construir consulta para eventos activos
            placeholders = ','.join(['%s'] * len(EVENTOS_ACTIVOS))
            query = f"SELECT * FROM asistentes WHERE Evento IN ({placeholders}) ORDER BY Nombrecompleto, apellidos"
            
            cursor.execute(query, EVENTOS_ACTIVOS)
            usuarios = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error obteniendo usuarios: {e}")
            messagebox.showerror('Error', f'Error al obtener usuarios:\n{str(e)}')
        
        return usuarios

    def actualizar_tabla_usuarios_optimizada(self, tree):
        """Actualiza la tabla de usuarios con datos frescos (optimizado)."""
        try:
            # Limpiar tabla actual
            for item in tree.get_children():
                tree.delete(item)
            
            # Obtener eventos una sola vez
            eventos = self.obtener_eventos_seguro()
            eventos_dict = {e['id']: e for e in eventos}
            
            # Obtener datos actualizados
            usuarios = self.obtener_usuarios_eventos_activos()
            
            # Volver a insertar datos
            for usuario in usuarios:
                pulsera_texto = "✅ SÍ" if usuario.get('comida', 0) == 1 else "❌ NO"
                evento_id = usuario.get('Evento', '')
                
                # Obtener nombre del evento desde el diccionario ya cargado
                if evento_id in eventos_dict:
                    evento_nombre = eventos_dict[evento_id]['Nombre']
                else:
                    evento_nombre = "No encontrado"
                
                tree.insert('', 'end', values=(
                    usuario.get('idUsuario', ''),
                    usuario.get('Nombrecompleto', ''),
                    usuario.get('apellidos', ''),
                    usuario.get('Empresa', ''),
                    usuario.get('entrada', ''),
                    f"{evento_id} - {evento_nombre}",
                    pulsera_texto
                ))
        except Exception as e:
            messagebox.showerror('Error', f'Error al actualizar tabla:\n{str(e)}')

    def actualizar_tabla_usuarios(self, tree, usuarios_ref):
        """Actualiza la tabla de usuarios con datos frescos."""
        # Limpiar tabla actual
        for item in tree.get_children():
            tree.delete(item)
        
        # Obtener datos actualizados
        usuarios = self.obtener_usuarios_eventos_activos()
        
        # Volver a insertar datos
        for usuario in usuarios:
            pulsera_texto = "✅ SÍ" if usuario.get('comida', 0) == 1 else "❌ NO"
            evento_nombre = self.obtener_nombre_evento(usuario.get('Evento', ''))
            
            tree.insert('', 'end', values=(
                usuario.get('idUsuario', ''),
                usuario.get('Nombrecompleto', ''),
                usuario.get('apellidos', ''),
                usuario.get('Empresa', ''),
                usuario.get('entrada', ''),
                f"{usuario.get('Evento', '')} - {evento_nombre}",
                pulsera_texto
            ))

    def registrar_actividad(self, tipo, mensaje, datos_usuario=None):
        """Registra actividad del sistema con timestamp y detalles del usuario."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extraer información del usuario si está disponible
        usuario_info = "Sistema"
        if datos_usuario:
            if isinstance(datos_usuario, dict):
                # Buscar nombre en diferentes campos posibles
                nombre = (datos_usuario.get('nombre') or 
                         datos_usuario.get('Usuario') or 
                         datos_usuario.get('Nombrecompleto') or 
                         datos_usuario.get('Nombre') or '')
                
                # Buscar empresa en diferentes campos posibles  
                empresa = (datos_usuario.get('empresa') or 
                          datos_usuario.get('Empresa') or 
                          datos_usuario.get('Company') or '')
                
                # Buscar ID de usuario
                id_usuario = (datos_usuario.get('idUsuario') or 
                             datos_usuario.get('id') or '')
                
                # Buscar apellidos si existe
                apellidos = datos_usuario.get('apellidos', '')
                
                # Construir nombre completo
                nombre_completo = f"{nombre} {apellidos}".strip() if apellidos else nombre
                
                if nombre_completo and empresa:
                    usuario_info = f"{nombre_completo} ({empresa})"
                elif nombre_completo:
                    usuario_info = f"{nombre_completo}"
                elif id_usuario:
                    usuario_info = f"ID: {id_usuario}"
        
        # Formatear mensaje con colores según el tipo (sin duplicar iconos)
        if tipo == "SUCCESS":
            entrada = f"[{timestamp}] ✅ {mensaje} - Usuario: {usuario_info}"
        elif tipo == "ERROR":
            entrada = f"[{timestamp}] ❌ {mensaje} - Usuario: {usuario_info}"
        elif tipo == "WARNING":
            entrada = f"[{timestamp}] ⚠️ {mensaje} - Usuario: {usuario_info}"
        else:  # INFO
            entrada = f"[{timestamp}] ℹ️ {mensaje} - Usuario: {usuario_info}"
        
        # Agregar a la lista de actividad
        self.log_actividad.append(entrada)
        
        # Limitar el tamaño del log en memoria (últimas 100 entradas)
        if len(self.log_actividad) > 100:
            self.log_actividad = self.log_actividad[-100:]

    def obtener_actividad_completa(self):
        """Obtiene actividad del sistema desde la base de datos."""
        actividad = []
        try:
            # Usar la misma lógica de conexión que buscar_asistente
            import pymysql
            
            # Usar IP por defecto - no dependemos de widgets UI
            ip_servidor = '192.168.1.100'  # IP por defecto
            
            configuraciones = [
                {'host': ip_servidor, 'user': 'root', 'password': '', 'database': 'agribusi_acreditacion'},
                {'host': ip_servidor, 'user': 'root', 'password': 'root', 'database': 'agribusi_acreditacion'},
                {'host': ip_servidor, 'user': 'agribusi_acr3D1t', 'password': 'tTe}1*d$Kz*R', 'database': 'agribusi_acreditacion'},
                {'host': '127.0.0.1', 'user': 'root', 'password': '', 'database': 'agribusi_acreditacion'},
            ]
            
            conn = None
            for config in configuraciones:
                try:
                    conn = pymysql.connect(**config)
                    break
                except:
                    continue
            
            if not conn:
                return []
            
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            # Buscar tabla de actividad o logs si existe
            cursor.execute("SHOW TABLES")
            tablas = [row[list(row.keys())[0]] for row in cursor.fetchall()]
            
            if 'actividad' in tablas:
                cursor.execute("SELECT * FROM actividad ORDER BY timestamp DESC LIMIT 50")
                actividad = cursor.fetchall()
            elif 'logs' in tablas:
                cursor.execute("SELECT * FROM logs ORDER BY fecha DESC LIMIT 50")
                registros = cursor.fetchall()
                for reg in registros:
                    actividad.append({
                        'timestamp': reg.get('fecha', 'Sin fecha'),
                        'evento': reg.get('evento', 'Sin evento'),
                        'usuario': reg.get('usuario', 'Sistema')
                    })
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            # Si hay error, registrar y continuar sin actividad de BD
            print(f"Info: No se pudo obtener actividad de BD: {e}")
        
        return actividad

    def obtener_nombre_evento(self, evento_id):
        """Obtiene el nombre de un evento por su ID."""
        try:
            eventos = self.obtener_eventos_seguro()
            eventos_dict = {e['id']: e for e in eventos}
            
            if evento_id in eventos_dict:
                return eventos_dict[evento_id]['Nombre']
            else:
                return f"Evento {evento_id}"
        except Exception as e:
            print(f"Error obteniendo nombre del evento {evento_id}: {e}")
            return f"Evento {evento_id}"

    def on_buscar_manual(self):
        id_asistente = self.manual_entry.get().strip()
        if not id_asistente:
            messagebox.showerror('Error', 'Introduce un ID para buscar.')
            return
        
        # Validar que hay eventos activos
        if not EVENTOS_ACTIVOS:
            messagebox.showerror('Error', 'No hay eventos activos seleccionados.\nPor favor selecciona al menos un evento.')
            return
        
        try:
            print(f"Buscando ID: {id_asistente}")  # Debug
            datos = buscar_asistente(id_asistente)
            print(f"Datos encontrados: {datos}")  # Debug
            
            if not datos:
                messagebox.showerror('Error', f'No se encontró el ID: {id_asistente}')
                # Log acceso denegado por usuario no encontrado
                log_acceso({'idUsuario': id_asistente}, False, "Usuario no encontrado en BD")
                self.log_acceso_resultado({'idUsuario': id_asistente}, False, "Usuario no encontrado en BD")
                return
            
            # Validar que el usuario pertenece a un evento activo
            autorizado, razon = validar_usuario_evento(datos, EVENTOS_ACTIVOS)
            
            # Registrar el acceso en CSV
            log_acceso(datos, autorizado, razon)
            
            # Registrar en el log visual con colores
            self.log_acceso_resultado(datos, autorizado, razon)
            
            if not autorizado:
                mensaje = f"ACCESO DENEGADO\n\n{razon}\n\nEventos activos: {', '.join(map(str, EVENTOS_ACTIVOS))}"
                messagebox.showerror('Acceso Denegado', mensaje)
                return
                
            # Acceso autorizado - generar etiqueta
            self.log_message("Generando etiqueta...", "INFO")
            
            # Obtener nombre del evento desde los eventos cargados
            evento_id = datos.get('Evento')
            eventos = self.obtener_eventos_seguro()
            nombre_evento = obtener_nombre_evento(evento_id, eventos)
            
            self.img_etiqueta = generar_etiqueta(datos, nombre_evento)
            self.show_preview(self.img_etiqueta)
            self.datos_actual = datos
            self.btn_print['state'] = 'normal'
            self.actualizar_info_status("✅ Etiqueta lista para imprimir")
            self.log_message("¡Etiqueta generada correctamente!", "SUCCESS")
            
        except Exception as e:
            messagebox.showerror('Error', f'Error inesperado: {str(e)}')
            self.log_message(f"Error inesperado: {str(e)}", "ERROR")
            print(f"Error completo: {e}")  # Debug

    def probar_conexion_bd(self):
        # Solicita la IP del servidor al usuario
        from tkinter import simpledialog
        ip_servidor = simpledialog.askstring("IP del servidor", 
                                            "Introduce la IP del servidor MySQL/MariaDB:", 
                                            initialvalue="localhost")
        if not ip_servidor:
            return
            
        # Lista de configuraciones comunes a probar
        configuraciones = [
            {'host': ip_servidor, 'user': 'root', 'password': '', 'database': 'agribusi_acreditacion'},
            {'host': ip_servidor, 'user': 'root', 'password': 'root', 'database': 'agribusi_acreditacion'},
            {'host': ip_servidor, 'user': 'root', 'password': 'password', 'database': 'agribusi_acreditacion'},
            {'host': ip_servidor, 'user': 'root', 'password': '1234', 'database': 'agribusi_acreditacion'},
            {'host': ip_servidor, 'user': 'agribusi_acr3D1t', 'password': 'tTe}1*d$Kz*R', 'database': 'agribusi_acreditacion'},
            # También prueba con localhost específicamente
            {'host': '127.0.0.1', 'user': 'root', 'password': '', 'database': 'agribusi_acreditacion'},
            {'host': '127.0.0.1', 'user': 'root', 'password': 'root', 'database': 'agribusi_acreditacion'},
        ]
        
        for i, config in enumerate(configuraciones):
            try:
                conn = mysql.connector.connect(**config)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM asistentes")
                count = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                
                mensaje = f"✅ CONEXIÓN EXITOSA!\n\nConfiguración {i+1}:\nHost: {config['host']}\nUsuario: {config['user']}\nPassword: {'*' * len(config['password']) if config['password'] else '(sin password)'}\nBase de datos: {config['database']}\n\nRegistros en tabla 'asistentes': {count}"
                messagebox.showinfo("Conexión exitosa", mensaje)
                
                # Actualiza la configuración global
                global DB_CONFIG
                DB_CONFIG = config
                return
                
            except Exception as e:
                print(f"Config {i+1} falló: {e}")
                continue
        
        messagebox.showerror("Error", "No se pudo conectar con ninguna configuración común.\n\nVerifica:\n- Que MySQL esté ejecutándose\n- Usuario y contraseña correctos\n- Que exista la base de datos 'agribusi_acreditacion'")

    def mostrar_ayuda(self):
        tutorial = (
            'TUTORIAL DE INICIO\n\n'
            '1. Conecta el escáner NetumScan USB y la impresora Brother QL-600/700/800 (Windows).\n'
            '2. Instala los drivers de la impresora (Windows) o configura tu impresora (Mac/Linux).\n'
            '3. Abre el programa.\n'
            '4. Escanea el código o ID del asistente en el campo de entrada (el escáner lo escribe y envía Enter automáticamente).\n'
            '5. El programa buscará los datos en la base de datos y generará la etiqueta con el nombre, empresa, evento, días y QR.\n'
            f'6. Si el modo Auto está activado, la etiqueta se {"imprimirá" if IS_WINDOWS else "guardará"} automáticamente. Si está en modo Manual, revisa la vista previa y pulsa "{"Imprimir" if IS_WINDOWS else "Guardar"}".\n'
            '7. El log muestra las operaciones realizadas.\n\n'
            'Consejos:\n'
            '- Mantén el campo de entrada enfocado para escanear rápidamente.\n'
            f'- Revisa que {"la impresora y " if IS_WINDOWS else ""}el escáner estén correctamente conectados.\n'
            f'- {"En Mac/Linux las etiquetas se guardan en ~/Etiquetas_QR/" if not IS_WINDOWS else ""}\n'
            '- Si tienes dudas, contacta con soporte técnico.'
        )
        messagebox.showinfo('Ayuda - Cómo usar el programa', tutorial)

    def focus_entry(self):
        self.entry.focus_set()

    def on_scan(self, event=None):
        id_asistente = self.entry.get().strip()
        if not id_asistente:
            return
            
        # Validar que hay eventos activos
        if not EVENTOS_ACTIVOS:
            messagebox.showerror('Error', 'No hay eventos activos seleccionados.')
            self.entry.delete(0, 'end')
            self.focus_entry()
            return
            
        datos = buscar_asistente(id_asistente)
        if not datos:
            messagebox.showerror('Error', f'No se encontró el ID: {id_asistente}')
            log_acceso({'idUsuario': id_asistente}, False, "Usuario no encontrado en BD")
            self.log_acceso_resultado({'idUsuario': id_asistente}, False, "Usuario no encontrado en BD")
            self.entry.delete(0, 'end')
            self.focus_entry()
            return
            
        # Validar que el usuario pertenece a un evento activo
        autorizado, razon = validar_usuario_evento(datos, EVENTOS_ACTIVOS)
        log_acceso(datos, autorizado, razon)
        
        # Registrar en el log visual con colores
        self.log_acceso_resultado(datos, autorizado, razon)
        
        if not autorizado:
            messagebox.showerror('Acceso Denegado', f"{razon}\n\nEventos activos: {', '.join(map(str, EVENTOS_ACTIVOS))}")
            self.entry.delete(0, 'end')
            self.focus_entry()
            return
            
        # Usuario autorizado - proceder con etiqueta
        self.log_message("Generando etiqueta...", "INFO")
        
        # Obtener nombre del evento desde los eventos cargados
        evento_id = datos.get('Evento')
        eventos = self.obtener_eventos_seguro()
        nombre_evento = obtener_nombre_evento(evento_id, eventos)
        
        self.img_etiqueta = generar_etiqueta(datos, nombre_evento)
        self.show_preview(self.img_etiqueta)
        self.datos_actual = datos
        self.actualizar_info_status("✅ Etiqueta lista para imprimir")
        self.log_message("¡Etiqueta generada correctamente!", "SUCCESS")
        
        # Si está en modo automático, imprimir inmediatamente Y marcar comida
        if self.auto_mode.get():
            # Marcar comida en la base de datos
            id_usuario = datos.get('idUsuario')
            if marcar_comida(id_usuario):
                self.log_message(f"Comida registrada para usuario {id_usuario}", "SUCCESS")
            else:
                self.log_message(f"Error al registrar comida para usuario {id_usuario}", "ERROR")
            
            self.imprimir_y_log()
        else:
            self.btn_print['state'] = 'normal'
        self.entry.delete(0, 'end')
        self.focus_entry()

    def show_preview(self, img):
        # Mantener proporción 62×100 mm sin deformar
        target_w = 360  # ancho preview en UI
        ratio = target_w / img.width
        target_h = int(img.height * ratio)
        img_preview = img.resize((target_w, target_h), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img_preview)
        self.preview_lbl.configure(image=self.tk_img)

    def on_print(self):
        self.imprimir_y_log()
        self.btn_print['state'] = 'disabled'

    def imprimir_y_log(self):
        # Marcar comida en la base de datos si estamos en modo manual
        if not self.auto_mode.get() and hasattr(self, 'datos_actual') and self.datos_actual:
            id_usuario = self.datos_actual.get('idUsuario')
            if marcar_comida(id_usuario):
                self.log_message(f"Comida registrada para usuario {id_usuario}", "SUCCESS")
            else:
                self.log_message(f"Error al registrar comida para usuario {id_usuario}", "ERROR")
        
        imprimir_etiqueta(self.img_etiqueta)
        log_impresion(self.datos_actual)
        self.add_log(self.datos_actual)

    def add_log(self, datos):
        """Registra la impresión en el log de actividad."""
        nombre = datos.get('Nombrecompleto', '')
        apellidos = datos.get('apellidos', '')
        id_usuario = datos.get('idUsuario', '')
        mensaje = f"IMPRESIÓN COMPLETADA: {nombre} {apellidos} (ID: {id_usuario})"
        self.registrar_actividad("SUCCESS", mensaje, datos)

    def add_log_acceso(self, mensaje):
        """Agrega un mensaje al log de accesos usando el nuevo sistema con colores."""
        # Determinar el tipo según el contenido del mensaje
        if "AUTORIZADO" in mensaje:
            self.log_message(mensaje.replace("AUTORIZADO: ", ""), "SUCCESS")
        elif "DENEGADO" in mensaje:
            self.log_message(mensaje.replace("DENEGADO: ", ""), "ERROR")
        else:
            self.log_message(mensaje, "INFO")

    def actualizar_info_status(self, texto):
        """Actualiza la información de estado."""
        if hasattr(self, 'info_label'):
            self.info_label.config(text=texto)

if __name__ == '__main__':
    # =====================================================
    # 🚀 INICIO DEL SISTEMA PROFESIONAL
    # =====================================================
    print("🏢 Iniciando Sistema Profesional de Etiquetas QR v2.0")
    print("🔧 Configurando interfaz y conexiones...")
    
    try:
        app = SistemaEtiquetasProfesional()
        print("✅ Sistema iniciado correctamente")
        app.mainloop()
    except Exception as e:
        print(f"❌ Error crítico al iniciar el sistema: {e}")
        input("Presione Enter para salir...")
