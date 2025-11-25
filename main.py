"""
🏢 SISTEMA PROFESIONAL DE IMPRESIÓN DE ETIQUETAS QR
📋 Control de Acceso por Eventos - Brother QL Series
🔧 Stack: Tkinter, Pillow, qrcode, win32print, mysql-connector-python

Desarrollado para gestión profesional de eventos con validación de accesos
y control de impresión de credenciales personalizadas.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
import qrcode
import mysql.connector
import csv
import io
import pandas as pd
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
            
            # Adaptar campos según el origen (MySQL o CSV)
            id_usuario = datos.get('idUsuario') or datos.get('cedula', '')
            nombre = datos.get('Nombrecompleto') or f"{datos.get('nombre', '')} {datos.get('apellidos', '')}".strip()
            empresa = datos.get('Empresa') or datos.get('empresa', '')
            evento = datos.get('Evento') or datos.get('entrada', '')
            
            writer.writerow([
                datetime.now().isoformat(),
                id_usuario,
                nombre,
                empresa,
                evento,
                "AUTORIZADO" if autorizado else "DENEGADO",
                razon,
                ','.join(map(str, EVENTOS_ACTIVOS)) if EVENTOS_ACTIVOS else "CSV_MODE"
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

def marcar_comida(id_usuario, sistema=None):
    """Marca comida = 1 en la tabla de asistentes para el usuario especificado."""
    try:
        print(f"🍽️ Marcando comida para usuario ID: {id_usuario}...")
        
        # Si se pasa la instancia del sistema, verificar si estamos en modo CSV
        if sistema and sistema.modo_csv and sistema.datos_csv is not None:
            return sistema.marcar_comida_csv(id_usuario)
        
        # Modo MySQL: intentar en ambas bases de datos
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

def generar_etiqueta(datos, nombre_evento=None, version_impresion=False):
    """
    Genera etiqueta con dos versiones:
    - version_impresion=False: Versión con colores para vista previa
    - version_impresion=True: Versión original en blanco para impresión
    """
    from PIL import Image, ImageDraw, ImageFont
    import qrcode

    # Adaptar campos según el origen (MySQL o CSV)
    nombre = datos.get('Nombrecompleto') or datos.get('nombre', '')
    apellidos = datos.get('Apellidos') or datos.get('apellidos', '')  # Buscar Apellidos (mayúscula) primero
    empresa = datos.get('Empresa') or datos.get('empresa', '')
    dias = datos.get('Dia', '1')  # Valor por defecto para CSV
    id_usuario = datos.get('idUsuario') or datos.get('cedula', '')
    tipo_entrada = datos.get('Entrada') or datos.get('entrada', 'Congreso')  # Buscar Entrada (mayúscula) primero
    pagado = datos.get('Pagado') or datos.get('pagado', '0')  # Campo para verificar si está pagado
    
    # Construir nombre completo si viene por separado (CSV)
    if not nombre and datos.get('nombre'):
        nombre_completo = f"{datos.get('nombre', '')} {apellidos}".strip()
        nombre = nombre_completo
    elif nombre and apellidos and apellidos not in nombre:
        # Si tenemos nombre y apellidos separados, y apellidos no está ya en nombre
        nombre = f"{nombre} {apellidos}".strip()
    
    # Convertir tipo de entrada a inglés si es necesario
    if tipo_entrada == "Congreso":
        tipo_entrada = "Congress"
    
    # Si no se pasa el nombre del evento, usar valor por defecto
    if nombre_evento is None:
        nombre_evento = "Evento no especificado"

    # ===============================================
    # 🎨 SISTEMA DE COLORES SOLO PARA VISTA PREVIA
    # ===============================================
    
    if version_impresion:
        # VERSIÓN IMPRESIÓN: Fondo blanco tradicional
        fondo_color = 'white'
        banda_color = None  # Sin banda de color
    else:
        # VERSIÓN VISTA PREVIA: Con colores para identificación
        # Determinar color de fondo según el tipo de entrada y evento
        fondo_color = 'white'  # Color por defecto
        
        # Normalizar nombres para comparación
        evento_lower = nombre_evento.lower() if nombre_evento else ''
        tipo_lower = tipo_entrada.lower() if tipo_entrada else ''
        
        if 'expo' in tipo_lower:
            # REGLA ESPECIAL: TODAS las entradas EXPO → fondo negro
            fondo_color = "#2C2C2C"  # Gris muy oscuro/negro para EXPO
        elif 'lpn congress' in evento_lower or 'lpn' in evento_lower:
            # LPN Congress - Congress normal
            if 'congress' in tipo_lower:
                fondo_color = "#FFCB6B"  # Amarillo para Congress
            else:
                fondo_color = '#E6F3FF'  # Azul claro para otros LPN
        elif 'porciforum latam' in evento_lower or 'porciforum mexico' in evento_lower:
            # porciFORUM LATAM - Congress normal
            if 'congress' in tipo_lower:
                fondo_color = '#FFF0F5'  # Rosa claro para Congress
            else:
                fondo_color = '#F8F8FF'  # Blanco fantasma para otros
        else:
            # Otros eventos - mantener blanco o color neutro
            fondo_color = '#F8F8FF'  # Ghost White - Blanco con tinte azul muy sutil

    PRINT_WIDTH = 696   # ancho físico (62 mm a 300 dpi)
    LARGO = 1200        # largo etiqueta
    W, H = LARGO, PRINT_WIDTH
    
    # Crear imagen con el fondo apropiado
    img = Image.new('RGB', (W, H), fondo_color)
    draw = ImageDraw.Draw(img)

    # Cargar fuentes según el sistema operativo
    font_name, font_empresa, font_dias, font_entrada_evento = load_fonts()

    # ===============================================
    # 🌈 BANDA DE COLOR SUPERIOR SOLO PARA VISTA PREVIA
    # ===============================================
    
    banda_color = None
    banda_height = 15  # Altura de la banda en píxeles
    
    if not version_impresion:  # Solo en vista previa, no en impresión
        # Normalizar nombres para comparación
        evento_lower = nombre_evento.lower() if nombre_evento else ''
        tipo_lower = tipo_entrada.lower() if tipo_entrada else ''
        
        if 'lpn congress' in evento_lower or 'lpn' in evento_lower:
            # LPN Congress - Bandas diferenciadas
            if 'expo' in tipo_lower:
                banda_color = '#808080'  # Naranja vibrante para Expo
            elif 'congress' in tipo_lower:
                banda_color = '#FF6B35'  # Azul Dodger para Congress
            else:
                banda_color = "#3DAF3D"  # Verde Lima para otros LPN
        elif 'porciforum latam' in evento_lower or 'porciforum mexico' in evento_lower:
            # porciFORUM LATAM - Color distintivo
            banda_color = '#1E90FF'  # Crimson - Rojo vibrante
        else:
            # Otros eventos - banda gris sutil
            banda_color = '#1E90FF'  # Slate Gray
        
        # Dibujar banda de color en la parte superior
        if banda_color:
            draw.rectangle([0, 0, W, banda_height], fill=banda_color, outline=banda_color)

    pad = 25
    qr_ancho = int(W * 0.40)
    texto_w = W - qr_ancho - (pad * 3)
    texto_x = pad
    
    # Ajustar posición inicial según si hay banda o no
    if banda_color:  # Si hay banda (solo en vista previa)
        y_pos = pad + banda_height + 5
    else:  # Si no hay banda (impresión)
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

    # INDICADOR DE ENTRADA PAGADA - "P" en recuadro negro
    if str(pagado) == '1':  # Si está pagado
        # Configuración del recuadro
        p_font_size = 40
        try:
            p_font = ImageFont.truetype("arial.ttf", p_font_size)
        except:
            try:
                p_font = ImageFont.truetype("DejaVuSans-Bold.ttf", p_font_size)
            except:
                p_font = ImageFont.load_default()
        
        # Dimensiones del recuadro - SIN padding extra
        p_texto = "P"
        bbox = draw.textbbox((0, 0), p_texto, font=p_font)
        p_ancho = bbox[2] - bbox[0] + 10  # padding horizontal reducido
        p_alto = bbox[3] - bbox[1] + 8    # padding vertical reducido
        
        # Posición del recuadro (izquierda, encima del nombre)
        p_x = texto_x  # Alineado con el texto a la izquierda
        p_y = y_pos
        
        # Dibujar recuadro negro
        draw.rectangle([p_x, p_y, p_x + p_ancho, p_y + p_alto], fill='black', outline='black')
        
        # Dibujar "P" en blanco centrada
        texto_x_p = p_x + (p_ancho - (bbox[2] - bbox[0])) // 2
        texto_y_p = p_y + (p_alto - (bbox[3] - bbox[1])) // 2
        draw.text((texto_x_p, texto_y_p), p_texto, font=p_font, fill='white')
        
        # Ajustar y_pos para que el nombre aparezca debajo del indicador
        y_pos += p_alto + 5

    # NOMBRE
    for linea in wrap(nombre + " " + apellidos, font_name, texto_w)[:2]:
        draw.text((texto_x, y_pos), linea, font=font_name, fill='black')
        y_pos += 110  # más separación

    # TIPO DE ENTRADA - formato según versión
    if tipo_entrada:
        if not version_impresion:
            # VERSIÓN VISTA PREVIA: Con colores y descripción de pulsera
            # Agregar descripción del tipo de pulsera
            descripcion_pulsera = ""
            if 'lpn congress' in evento_lower or 'lpn' in evento_lower:
                if 'expo' in tipo_lower:
                    descripcion_pulsera = " • PULSERA EXPO"
                elif 'congress' in tipo_lower:
                    descripcion_pulsera = " • PULSERA CONGRESS"
                else:
                    descripcion_pulsera = " • PULSERA LPN"
            elif 'porciforum latam' in evento_lower or 'porciforum mexico' in evento_lower:
                descripcion_pulsera = " • PULSERA LATAM"
            
            texto_completo = tipo_entrada + descripcion_pulsera
            
            # Calcular dimensiones del texto
            bbox_tipo = draw.textbbox((0, 0), texto_completo, font=font_entrada_evento)
            texto_ancho = bbox_tipo[2] - bbox_tipo[0]
            texto_alto = bbox_tipo[3] - bbox_tipo[1]
            
            # Usar el color de la banda como fondo (o negro por defecto)
            fondo_tipo = banda_color if banda_color else 'black'
            
            # Dibujar rectángulo con color de fondo que coincide con la banda
            draw.rectangle([texto_x, y_pos, texto_x + texto_ancho + 10, y_pos + texto_alto + 8], 
                          fill=fondo_tipo, outline=fondo_tipo)
            
            # Dibujar el texto en blanco encima del fondo colorido
            draw.text((texto_x + 5, y_pos + 4), texto_completo, font=font_entrada_evento, fill='white')
        else:
            # VERSIÓN IMPRESIÓN: Formato original simple con fondo negro
            # Calcular dimensiones del texto
            bbox_tipo = draw.textbbox((0, 0), tipo_entrada, font=font_entrada_evento)
            texto_ancho = bbox_tipo[2] - bbox_tipo[0]
            texto_alto = bbox_tipo[3] - bbox_tipo[1]
            
            # Dibujar rectángulo negro de fondo
            draw.rectangle([texto_x, y_pos, texto_x + texto_ancho + 10, y_pos + texto_alto + 8], 
                          fill='black', outline='black')
            
            # Dibujar el texto en blanco encima del fondo negro
            draw.text((texto_x + 5, y_pos + 4), tipo_entrada, font=font_entrada_evento, fill='white')
    
    y_pos += 60  # espaciado reducido para fuente más pequeña

    # EVENTO
    for linea in wrap(f" - {nombre_evento}", font_entrada_evento, texto_w)[:2]:
        draw.text((texto_x, y_pos), linea, font=font_entrada_evento, fill='black')
        y_pos += 60  # espaciado reducido para fuente más pequeña

    # EMPRESA (ahora después del evento)
    for linea in wrap(empresa, font_empresa, texto_w)[:3]:
        draw.text((texto_x, y_pos), linea, font=font_empresa, fill='black')
        y_pos += 90  # más separación

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



def imprimir_etiqueta(img, sistema=None):
    """Imprime en Brother QL en TODAS las plataformas"""
    try:
        # Intentar impresión Brother QL en cualquier sistema operativo
        if IS_WINDOWS:
            # Windows: usar win32print (pasar sistema para usar impresora seleccionada)
            return imprimir_etiqueta_windows(img, sistema)
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

def imprimir_etiqueta_windows(img, sistema=None):
    """Imprime usando win32print (método Windows nativo más confiable)."""
    try:
        import win32print
        import win32ui
        from PIL import ImageWin
        import tempfile
        import os
        import time
        
        # VERIFICAR SI HAY UNA IMPRESORA SELECCIONADA MANUALMENTE
        impresora_manual = None
        if sistema and hasattr(sistema, 'impresora_seleccionada') and sistema.impresora_seleccionada:
            impresora_manual = sistema.impresora_seleccionada
            print(f"🎯 Usando impresora seleccionada manualmente: {impresora_manual}")
        
        # Si no hay selección manual, buscar automáticamente
        if not impresora_manual:
            print("🔄 Actualizando lista de impresoras...")
            time.sleep(0.1)  # Pequeña pausa para asegurar sincronización
            
            # Buscar impresoras Brother instaladas DINÁMICAMENTE
            impresoras = []
            try:
                # Usar flag PRINTER_ENUM_LOCAL | PRINTER_ENUM_CONNECTIONS (6)
                # para forzar actualización completa
                for printer_info in win32print.EnumPrinters(6):
                    nombre = printer_info[2]
                    if 'Brother' in nombre and ('QL-600' in nombre or 'QL-700' in nombre or 'QL-800' in nombre):
                        impresoras.append(nombre)
                        print(f"   📌 Encontrada: {nombre}")
            except Exception as e:
                print(f"⚠️ Error enumerando impresoras con flag 6, usando flag 2: {e}")
                # Fallback al método original
                for printer_info in win32print.EnumPrinters(2):
                    nombre = printer_info[2]
                    if 'Brother' in nombre and ('QL-600' in nombre or 'QL-700' in nombre or 'QL-800' in nombre):
                        impresoras.append(nombre)
            
            if not impresoras:
                raise Exception("No se encontró ninguna impresora Brother QL instalada en Windows. Instala el driver oficial.")
            
            # Si hay múltiples impresoras, usar la predeterminada del sistema o la primera
            nombre_impresora = None
            
            # Intentar obtener la impresora predeterminada del sistema
            try:
                impresora_predeterminada = win32print.GetDefaultPrinter()
                if any(imp in impresora_predeterminada for imp in impresoras):
                    nombre_impresora = impresora_predeterminada
                    print(f"✅ Usando impresora predeterminada: {nombre_impresora}")
            except:
                pass
            
            # Si no hay predeterminada o no es Brother, usar la primera encontrada
            if not nombre_impresora:
                nombre_impresora = impresoras[0]
                print(f"✅ Usando primera impresora Brother encontrada: {nombre_impresora}")
        else:
            # Usar la impresora seleccionada manualmente
            nombre_impresora = impresora_manual
        
        # Crear contexto de impresión NUEVO cada vez
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

def verificar_archivo_log_disponible():
    """Verifica si el archivo de log está disponible para escritura."""
    try:
        # Intentar abrir el archivo para escritura y cerrarlo inmediatamente
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            pass
        return True
    except PermissionError:
        return False
    except Exception:
        return False

def log_impresion(datos):
    """Registra la impresión en el archivo de log con manejo de errores mejorado."""
    try:
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
        print(f"✅ Log de impresión guardado para usuario {datos.get('idUsuario')}")
    except PermissionError:
        print(f"⚠️ No se pudo escribir el log de impresión: archivo '{LOG_FILE}' en uso o sin permisos")
        print(f"💡 Sugerencia: Cierra Excel u otros programas que puedan tener abierto el archivo")
        # Intentar crear un archivo alternativo con timestamp
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_alternativo = f"log_impresiones_backup_{timestamp}.csv"
            with open(log_alternativo, 'a', newline='', encoding='utf-8') as f:
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
            print(f"✅ Log guardado en archivo alternativo: {log_alternativo}")
        except Exception as e2:
            print(f"❌ Error crítico guardando log: {e2}")
    except Exception as e:
        print(f"❌ Error inesperado al guardar log de impresión: {e}")

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
        
        # Variables para manejo de CSV - SISTEMA MULTI-EVENTO MEJORADO
        self.modo_csv = False
        self.datos_csv = None  # DataFrame maestro que contiene todos los eventos
        self.eventos_csv = None
        self.archivo_csv_actual = None
        self.archivo_eventos_csv = None
        self.mapeo_columnas = {}
        
        # NUEVO: Control de múltiples eventos CSV
        self.eventos_cargados = {}  # Diccionario: {nombre_evento: DataFrame}
        self.eventos_disponibles = []  # Lista de eventos disponibles para cargar
        self.csv_maestro_inicializado = False  # Si ya se estableció la estructura base
        
        # Crear interfaz profesional
        self.crear_interfaz_profesional()
        self.focus_entry()
        self.after(1000, self.mostrar_bienvenida)
        
        # Establecer título inicial
        self.actualizar_titulo_ventana()
        
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
        """Crea la interfaz principal con diseño profesional y scroll."""
        # ===============================================
        # 📜 ESTRUCTURA PRINCIPAL CON SCROLL
        # ===============================================
        
        # Canvas principal para scroll
        self.main_canvas = tk.Canvas(self, bg=ColoresTema.LIGHT)
        self.main_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.main_canvas.yview)
        
        # Frame scrolleable que contendrá todo el contenido
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        # Configurar el scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        # Configurar el canvas para ajustarse al ancho
        def _configure_canvas(event):
            canvas_width = event.width
            self.main_canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        self.main_canvas.bind('<Configure>', _configure_canvas)
        
        # Crear ventana en el canvas
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        
        # Bind del scroll con la rueda del ratón - MEJORADO para que funcione
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind scroll a múltiples elementos para que funcione en toda la ventana
        self.main_canvas.bind("<MouseWheel>", _on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        self.bind("<MouseWheel>", _on_mousewheel)
        
        # Función para propagar el scroll a elementos hijos
        def bind_to_mousewheel(parent):
            parent.bind("<MouseWheel>", _on_mousewheel)
            for child in parent.winfo_children():
                try:
                    bind_to_mousewheel(child)
                except:
                    pass
        
        # Aplicar después de crear la interfaz
        self.after(500, lambda: bind_to_mousewheel(self))
        
        # Empaquetar CORRECTAMENTE - scrollbar primero (derecha), luego canvas (rellena resto)
        self.main_scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)
        
        # Frame principal con padding elegante (ahora dentro del scroll)
        self.main_frame = ttk.Frame(self.scrollable_frame)
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
        
        # Actualizar configuración del scroll después de crear toda la interfaz
        self.after(100, self.actualizar_scroll_region)

    def actualizar_scroll_region(self):
        """Actualiza la región de scroll después de que toda la interfaz esté cargada."""
        try:
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        except:
            pass  # En caso de que el canvas no esté disponible aún

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
        
        # Fila superior de botones principales
        fila1 = ttk.Frame(control_frame)
        fila1.pack(fill='x', pady=(0, 5))
        
        self.btn_seleccionar = ttk.Button(fila1, 
                                         text="🎯 Seleccionar Eventos",
                                         command=self.seleccionar_eventos)
        self.btn_seleccionar.pack(side='left', padx=(0, 10))
        
        self.btn_log_accesos = ttk.Button(fila1,
                                         text="📊 Ver Log de Accesos", 
                                         command=self.ver_log_accesos)
        self.btn_log_accesos.pack(side='left', padx=(0, 10))
        
        self.btn_tabla_usuarios = ttk.Button(fila1,
                                           text="👥 Tabla de Usuarios", 
                                           command=self.mostrar_tabla_usuarios)
        self.btn_tabla_usuarios.pack(side='left', padx=(0, 10))
        
        self.btn_refresh = ttk.Button(fila1,
                                     text="🔄 Actualizar",
                                     command=self.actualizar_eventos_display)
        self.btn_refresh.pack(side='left')
        
        # Fila inferior - Botones CSV y estado
        fila2 = ttk.Frame(control_frame)
        fila2.pack(fill='x')
        
        # Indicador de estado de conexión
        self.estado_frame = ttk.Frame(fila2)
        self.estado_frame.pack(side='left')
        
        self.estado_label = ttk.Label(self.estado_frame, 
                                     text="🌐 Conectando...", 
                                     foreground='orange')
        self.estado_label.pack(side='left', padx=(0, 20))
        
        # Botones CSV y modo
        self.btn_cargar_csv = ttk.Button(fila2,
                                        text="📁 Cargar CSV",
                                        command=self.cargar_csv)
        self.btn_cargar_csv.pack(side='left', padx=(0, 10))
        
        # Botón para gestionar múltiples eventos CSV
        self.btn_gestionar_eventos = ttk.Button(fila2,
                                              text="🎯 Gestionar Eventos", 
                                              command=self.mostrar_gestor_eventos,
                                              state='disabled')
        self.btn_gestionar_eventos.pack(side='left', padx=(0, 10))
        
        self.btn_actualizar_csv = ttk.Button(fila2,
                                           text="🔄 Actualizar CSV", 
                                           command=self.actualizar_csv,
                                           state='disabled')
        self.btn_actualizar_csv.pack(side='left', padx=(0, 10))
        
        self.btn_descargar_csv = ttk.Button(fila2,
                                          text="🗑️ Descargar CSV", 
                                          command=self.descargar_csv,
                                          state='disabled')
        self.btn_descargar_csv.pack(side='left', padx=(0, 10))
        
        self.btn_cambiar_mysql = ttk.Button(fila2,
                                          text="🌐 Cambiar a MySQL", 
                                          command=self.cambiar_a_mysql,
                                          state='disabled')
        self.btn_cambiar_mysql.pack(side='left')

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
        
        # Container principal que contendrá la etiqueta y los indicadores de color
        main_container = tk.Frame(preview_frame)
        main_container.pack(pady=(0, 15), padx=20)
        
        # Container para la vista previa con tamaño OPTIMIZADO - ETIQUETA MÁS GRANDE
        preview_container = tk.Frame(main_container, 
                                   bg=ColoresTema.WHITE,
                                   relief='solid', 
                                   borderwidth=2,
                                   width=800,  # Era 650, ahora 800 para etiqueta más grande
                                   height=500)  # Era 420, ahora 500 para más altura
        preview_container.pack(side='left', padx=(0, 15))  # Menos padding
        preview_container.pack_propagate(False)  # Mantener tamaño fijo
        
        # Vista previa de la etiqueta - tamaño controlado
        self.preview_lbl = tk.Label(preview_container,
                                   text="📄 La vista previa aparecerá aquí\n🔍 Escanee un código",
                                   font=('Segoe UI', 12),
                                   fg=ColoresTema.GRAY,
                                   bg=ColoresTema.WHITE,
                                   justify='center')
        self.preview_lbl.pack(expand=True)
        
        # ===============================================
        # 🎨 PANEL DE INDICADORES DE PULSERAS (SOLO LPN Y PORCIFORUM)
        # ===============================================
        
        # Container para los indicadores de pulseras - MÁS COMPACTO
        # GUARDAMOS LA REFERENCIA para poder mostrar/ocultar según el evento
        self.pulseras_container = tk.Frame(main_container, bg=ColoresTema.WHITE, width=180)
        # NO lo empaquetamos aquí, se mostrará solo para eventos LPN y PorciForum
        self.pulseras_container.pack_propagate(False)  # Mantener ancho fijo
        
        # Título del panel de pulseras
        titulo_pulseras = tk.Label(self.pulseras_container,
                                  text="🎯 PULSERAS A ENTREGAR",
                                  font=('Segoe UI', 10, 'bold'),
                                  bg=ColoresTema.WHITE,
                                  fg=ColoresTema.GRAY)
        titulo_pulseras.pack(pady=(0, 10))
        
        # Indicador PULSERA NARANJA (LPN Congress) - MÁS COMPACTO
        self.pulsera_naranja = tk.Label(self.pulseras_container,
                                       text="🟠 NARANJA\n(LPN Congress)",
                                       font=('Segoe UI', 8, 'bold'),
                                       bg='#fd7e14',
                                       fg='white',
                                       relief='raised',
                                       borderwidth=2,
                                       padx=8,
                                       pady=6)
        self.pulsera_naranja.pack(pady=3, fill='x')
        
        # Indicador PULSERA AZUL (PorciForum Congress) - MÁS COMPACTO
        self.pulsera_azul = tk.Label(self.pulseras_container,
                                    text="🔵 AZUL\n(PorciForum Congress)",
                                    font=('Segoe UI', 8, 'bold'),
                                    bg='#007bff',
                                    fg='white',
                                    relief='raised',
                                    borderwidth=2,
                                    padx=8,
                                    pady=6)
        self.pulsera_azul.pack(pady=3, fill='x')
        
        # Indicador PULSERA NEGRA (EXPO) - MÁS COMPACTO
        self.pulsera_negra = tk.Label(self.pulseras_container,
                                    text="⚫ NEGRA\n(EXPO)",
                                    font=('Segoe UI', 8, 'bold'),
                                    bg='#2C2C2C',
                                    fg='white',
                                    relief='raised',
                                    borderwidth=2,
                                    padx=8,
                                    pady=6)
        self.pulsera_negra.pack(pady=3, fill='x')
        
        # Indicador de pulsera activa (inicialmente oculto)
        self.indicador_activo = tk.Label(self.pulseras_container,
                                        text="👆 ENTREGAR ESTA",
                                        font=('Segoe UI', 8, 'bold'),
                                        bg='#32CD32',
                                        fg='white',
                                        relief='solid',
                                        borderwidth=1,
                                        padx=5,
                                        pady=2)
        # No empaquetamos el indicador activo inicialmente
        
        # Separador para mochilas
        separador_mochila = tk.Label(self.pulseras_container,
                                    text="━━━━━━━━━━━━━━━━━━━━",
                                    font=('Segoe UI', 6),
                                    bg=ColoresTema.WHITE,
                                    fg=ColoresTema.GRAY)
        separador_mochila.pack(pady=(10, 5))
        
        # Título del panel de mochilas
        titulo_mochilas = tk.Label(self.pulseras_container,
                                  text="🎒 ESTADO DE MOCHILA",
                                  font=('Segoe UI', 10, 'bold'),
                                  bg=ColoresTema.WHITE,
                                  fg=ColoresTema.GRAY)
        titulo_mochilas.pack(pady=(0, 10))
        
        # Indicador de mochila SÍ
        self.mochila_si = tk.Label(self.pulseras_container,
                                  text="✅ SÍ MOCHILA\n(Entregar kit completo)",
                                  font=('Segoe UI', 8, 'bold'),
                                  bg='#28a745',
                                  fg='white',
                                  relief='raised',
                                  borderwidth=2,
                                  padx=8,
                                  pady=6)
        self.mochila_si.pack(pady=3, fill='x')
        
        # Indicador de mochila NO
        self.mochila_no = tk.Label(self.pulseras_container,
                                  text="❌ NO MOCHILA\n(Solo credencial y pulsera)",
                                  font=('Segoe UI', 8, 'bold'),
                                  bg='#dc3545',
                                  fg='white',
                                  relief='raised',
                                  borderwidth=2,
                                  padx=8,
                                  pady=6)
        self.mochila_no.pack(pady=3, fill='x')
        
        # Indicador de mochila activa (inicialmente oculto)
        self.indicador_mochila_activo = tk.Label(self.pulseras_container,
                                                text="👆 ESTADO MOCHILA",
                                                font=('Segoe UI', 8, 'bold'),
                                                bg='#ffc107',
                                                fg='black',
                                                relief='solid',
                                                borderwidth=1,
                                                padx=5,
                                                pady=2)
        # No empaquetamos el indicador de mochila inicialmente
        
        # Controles de impresión
        control_frame = ttk.Frame(preview_frame)
        control_frame.pack(fill='x')
        
        # Botón de impresión universal
        self.btn_print = ttk.Button(control_frame,
                                   text="🖨️ IMPRIMIR ETIQUETA",
                                   command=self.on_print)
        self.btn_print.pack(side='left', padx=(0, 10))
        self.btn_print['state'] = 'disabled'
        
        # Botón para seleccionar impresora (solo Windows)
        if IS_WINDOWS:
            self.btn_seleccionar_impresora = ttk.Button(control_frame,
                                                       text="🖨️ Seleccionar Impresora",
                                                       command=self.seleccionar_impresora)
            self.btn_seleccionar_impresora.pack(side='left', padx=(0, 10))
            
            # Variable para almacenar la impresora seleccionada
            self.impresora_seleccionada = None
        
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
        
        # Programar actualización del display después de que se complete la inicialización
        self.after(500, self.verificar_y_actualizar_eventos)
        
        # Programar verificación adicional periódica
        self.after(2000, self.verificacion_periodica_eventos)
        
        # NUEVO: Verificación directa si ya hay CSV cargado
        self.after(3000, self.forzar_actualizacion_si_csv_cargado)
        
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
        # Decidir qué fuente de eventos usar
        if self.modo_csv:
            eventos = self.obtener_eventos_csv()
            titulo_ventana = "🔹 Seleccionar Eventos Activos (MODO OFFLINE - CSV)"
            mensaje_error = "No se pudieron cargar los eventos desde el archivo CSV.\n\nVerifique que el archivo 'Eventos_Etiquetas.csv' esté presente y tenga la estructura correcta."
        else:
            eventos = self.obtener_eventos_seguro()
            titulo_ventana = "🔹 Seleccionar Eventos Activos (MODO ONLINE - MySQL)"
            mensaje_error = "No se pudieron cargar los eventos desde la base de datos.\n\n" + \
                          "Posibles causas:\n" + \
                          "• Sin conexión a internet\n" + \
                          "• Servidor de base de datos no disponible\n" + \
                          "• Configuración de red bloqueada\n\n" + \
                          "Verifique la conexión y pruebe el botón 'Probar Conexión'"
        
        if not eventos:
            messagebox.showerror("Error de Conexión", mensaje_error)
            return
        
        # Crear ventana de selección
        ventana = tk.Toplevel(self)
        ventana.title(titulo_ventana)
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
            modo_texto = "CSV" if self.modo_csv else "MySQL"
            messagebox.showinfo("Éxito", f"Se han activado {len(EVENTOS_ACTIVOS)} eventos en modo {modo_texto}")
            ventana.destroy()
        
        def cancelar():
            ventana.destroy()
        
        ttk.Button(botones, text="Guardar", command=guardar_seleccion).pack(side='left', padx=5)
        ttk.Button(botones, text="Cancelar", command=cancelar).pack(side='left', padx=5)

    def actualizar_eventos_display(self):
        """Actualiza la visualización de eventos activos."""
        self.eventos_text.config(state='normal')
        self.eventos_text.delete(1.0, tk.END)
        
        if self.modo_csv and self.eventos_cargados:
            # Modo CSV: Mostrar eventos cargados del sistema multi-evento
            texto = f"🔹 MODO OFFLINE (CSV) - {len(self.eventos_cargados)} Evento(s) Cargado(s):\n\n"
            
            for evento_nombre, info in self.eventos_cargados.items():
                archivo_nombre = os.path.basename(info['archivo'])
                fecha_carga = info['timestamp'].strftime("%d/%m/%Y %H:%M")
                texto += f"✅ {evento_nombre}\n"
                texto += f"   📄 Archivo: {archivo_nombre}\n"
                texto += f"   👥 Registros: {info['filas']}\n"
                texto += f"   🕒 Cargado: {fecha_carga}\n\n"
            
            total_registros = len(self.datos_csv) if hasattr(self, 'datos_csv') and self.datos_csv is not None else 0
            texto += f"📊 Total registros combinados: {total_registros}\n"
            texto += f"💾 Trabajando completamente OFFLINE"
            
        elif self.modo_csv and hasattr(self, 'datos_csv') and self.datos_csv is not None:
            # Modo CSV con datos cargados pero sin eventos_cargados (sistema anterior)
            total_registros = len(self.datos_csv)
            archivo_nombre = os.path.basename(self.archivo_csv_actual) if self.archivo_csv_actual else "archivo.csv"
            
            texto = f"� MODO OFFLINE (CSV) - Sistema Tradicional:\n\n"
            texto += f"📄 Archivo: {archivo_nombre}\n"
            texto += f"👥 Total registros: {total_registros}\n\n"
            texto += f"� Trabajando completamente OFFLINE\n"
            texto += f"�💡 Para usar el sistema multi-evento, utiliza 'Cargar CSV' para agregar más eventos."
            
        elif EVENTOS_ACTIVOS:
            # Modo MySQL: Mostrar eventos activos tradicional
            if self.modo_csv:
                eventos = self.obtener_eventos_csv()
                modo_texto = "🔹 MODO OFFLINE (CSV)"
            else:
                eventos = self.obtener_eventos_seguro()
                modo_texto = "🔹 MODO ONLINE (MySQL Server)"
                
            eventos_dict = {e['id']: e for e in eventos}
            
            texto = f"{modo_texto} - {len(EVENTOS_ACTIVOS)} Evento(s) Activo(s):\n\n"
            for evento_id in EVENTOS_ACTIVOS:
                if evento_id == 999:
                    # EVENTO ESPECIAL PARA CSV CARGADO
                    if self.eventos_cargados:
                        evento_nombre = list(self.eventos_cargados.keys())[0]
                        texto += f"✅ CSV CARGADO: {evento_nombre}\n"
                    else:
                        texto += f"✅ CSV CARGADO: Evento activo\n"
                elif evento_id in eventos_dict:
                    e = eventos_dict[evento_id]
                    texto += f"• ID: {e['id']} - {e['Nombre']} - {e['fecha']}\n"
                else:
                    texto += f"• ID: {evento_id} (no encontrado)\n"
            
            if not self.modo_csv:
                texto += f"\n🌐 Conectado a servidor MySQL en tiempo real"
        else:
            # Sin eventos
            if self.modo_csv:
                texto = "� MODO OFFLINE (CSV) - SIN DATOS\n\n"
                texto += "⚠️ No hay archivos CSV cargados.\n\n"
                texto += "📋 Para trabajar offline:\n"
                texto += "• Usa 'Cargar CSV' para agregar eventos con participantes\n"
                texto += "• Los datos se almacenan localmente\n"
                texto += "• No requiere conexión a internet"
            else:
                texto = "🔹 MODO ONLINE (MySQL Server) - SIN EVENTOS\n\n"
                texto += "⚠️ NO HAY EVENTOS ACTIVOS SELECCIONADOS\n"
                texto += "Todos los accesos serán denegados.\n\n"
                texto += "📋 Para trabajar online:\n"
                texto += "• Usa 'Seleccionar Eventos' para activar eventos\n"
                texto += "• Los datos se sincronizan en tiempo real\n"
                texto += "• Requiere conexión a servidor MySQL"
        
        self.eventos_text.insert(1.0, texto)
        self.eventos_text.config(state='disabled')

    def verificar_y_actualizar_eventos(self):
        """Verifica si hay eventos CSV cargados y actualiza el display."""
        print(f"🔍 Verificando eventos: modo_csv={self.modo_csv}, eventos_cargados={len(self.eventos_cargados)}")
        print(f"🔍 datos_csv exists: {hasattr(self, 'datos_csv') and self.datos_csv is not None}")
        
        # Si estamos en modo CSV y hay eventos cargados, actualizar display
        if self.modo_csv and self.eventos_cargados:
            print(f"🔄 Actualizando display de eventos: {len(self.eventos_cargados)} eventos cargados")
            self.actualizar_eventos_display()
        # Si no hay eventos CSV pero hay datos CSV cargados, podría ser que se cargó un CSV
        # pero no se registró en eventos_cargados (caso legacy)
        elif self.modo_csv and hasattr(self, 'datos_csv') and self.datos_csv is not None:
            print(f"🔄 Datos CSV detectados sin eventos_cargados, actualizando display")
            self.actualizar_eventos_display()
        # NUEVO: Forzar actualización si hay archivo CSV actual
        elif hasattr(self, 'archivo_csv_actual') and self.archivo_csv_actual:
            print(f"🔄 Archivo CSV detectado: {self.archivo_csv_actual}")
            self.actualizar_eventos_display()
        else:
            print(f"ℹ️ No hay eventos CSV para mostrar en el display")

    def verificacion_periodica_eventos(self):
        """Verificación periódica para detectar cambios en CSV."""
        # Solo verificar si no se ha actualizado recientemente
        texto_actual = self.eventos_text.get(1.0, tk.END).strip()
        
        # Si todavía muestra "NO HAY EVENTOS ACTIVOS" pero hay CSV cargado, actualizar
        if "NO HAY EVENTOS ACTIVOS SELECCIONADOS" in texto_actual:
            if (self.modo_csv and hasattr(self, 'datos_csv') and self.datos_csv is not None) or \
               (hasattr(self, 'archivo_csv_actual') and self.archivo_csv_actual):
                print("🔄 Detectado CSV cargado, forzando actualización del display")
                self.actualizar_eventos_display()

    def forzar_actualizacion_si_csv_cargado(self):
        """Fuerza actualización si detecta CSV cargado pero display no actualizado."""
        texto_actual = self.eventos_text.get(1.0, tk.END).strip()
        
        # Verificar todas las condiciones posibles de CSV cargado
        csv_cargado = False
        
        if self.modo_csv and hasattr(self, 'datos_csv') and self.datos_csv is not None:
            csv_cargado = True
            print("✅ CSV detectado vía datos_csv")
        
        if hasattr(self, 'archivo_csv_actual') and self.archivo_csv_actual:
            csv_cargado = True
            print(f"✅ CSV detectado vía archivo_csv_actual: {self.archivo_csv_actual}")
        
        if self.eventos_cargados:
            csv_cargado = True
            print(f"✅ CSV detectado vía eventos_cargados: {len(self.eventos_cargados)}")
        
        # Si hay CSV cargado pero el display dice "NO HAY EVENTOS", forzar actualización
        if csv_cargado and "NO HAY EVENTOS ACTIVOS SELECCIONADOS" in texto_actual:
            print("🚨 FORZANDO ACTUALIZACIÓN - CSV detectado pero display no actualizado")
            self.actualizar_eventos_display()
        elif csv_cargado:
            print("✅ CSV cargado y display ya actualizado correctamente")
        else:
            print("ℹ️ No hay CSV cargado - estado normal")

    # =====================================================
    # 📁 FUNCIONES PARA MANEJO DE CSV
    # =====================================================
    
    def cargar_csv(self):
        """Sistema mejorado para cargar múltiples CSVs de eventos en paralelo."""
        
        # ===============================================
        # 🎯 PASO 1: SELECTOR DE EVENTO
        # ===============================================
        
        # Obtener eventos desde el CSV de eventos (no hardcodeado)
        evento_seleccionado = self.mostrar_selector_evento(None)
        
        if not evento_seleccionado:
            return  # Usuario canceló
        
        # ===============================================
        # 🎯 PASO 2: SELECCIONAR ARCHIVO CSV
        # ===============================================
        
        try:
            archivo = filedialog.askopenfilename(
                title=f"Seleccionar CSV para: {evento_seleccionado}",
                filetypes=[
                    ("Archivos CSV", "*.csv"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if not archivo:
                return
            
            # ===============================================
            # 🎯 PASO 3: CARGAR Y PROCESAR CSV
            # ===============================================
            
            resultado = self.procesar_csv_evento(archivo, evento_seleccionado)
            
            if resultado:
                self.log_message(f"✅ CSV cargado para evento: {evento_seleccionado}", "SUCCESS")
                self.actualizar_estado_eventos_cargados()
                # Actualizar display de eventos inmediatamente - ahora funcionará porque está en EVENTOS_ACTIVOS
                self.actualizar_eventos_display()
            else:
                self.log_message(f"❌ Error al cargar CSV para: {evento_seleccionado}", "ERROR")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo CSV:\n{str(e)}")

    def mostrar_selector_evento(self, eventos_disponibles):
        """Muestra ventana para seleccionar el evento del CSV."""
        
        # Obtener eventos reales del CSV de eventos
        eventos_reales = self.obtener_eventos_csv()
        
        if not eventos_reales:
            # Si no hay eventos CSV cargados, mostrar mensaje
            respuesta = messagebox.askyesno(
                "Sin eventos CSV", 
                "No hay eventos CSV cargados.\n\n¿Desea cargar el archivo de eventos primero?"
            )
            if respuesta:
                self.cargar_eventos_csv()
                eventos_reales = self.obtener_eventos_csv()
                if not eventos_reales:
                    return None
            else:
                return None
        
        # Crear ventana modal
        ventana = tk.Toplevel(self)
        ventana.title("🎯 Seleccionar Evento para CSV")
        ventana.geometry("600x500")
        ventana.transient(self)
        ventana.grab_set()
        
        # Centrar ventana
        ventana.geometry("+%d+%d" % (self.winfo_rootx() + 50, self.winfo_rooty() + 50))
        
        evento_seleccionado = None
        
        # Frame principal
        main_frame = ttk.Frame(ventana, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(main_frame,
                          text="🎯 Seleccione el evento para este CSV",
                          font=('Segoe UI', 14, 'bold'))
        titulo.pack(pady=(0, 20))
        
        # Lista de eventos cargados (si los hay)
        if self.eventos_cargados:
            cargados_frame = ttk.LabelFrame(main_frame, text="📋 Eventos ya cargados", padding=10)
            cargados_frame.pack(fill='x', pady=(0, 15))
            
            for evento in self.eventos_cargados.keys():
                label = ttk.Label(cargados_frame, 
                                 text=f"✅ {evento}", 
                                 foreground='green')
                label.pack(anchor='w')
        
        # Frame para selección
        seleccion_frame = ttk.LabelFrame(main_frame, text="🎯 Seleccionar evento del CSV", padding=10)
        seleccion_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Crear canvas y scrollbar para la lista de eventos
        canvas = tk.Canvas(seleccion_frame, height=200)
        scrollbar = ttk.Scrollbar(seleccion_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Variable para almacenar selección
        evento_var = tk.StringVar()
        
        # Radio buttons para eventos reales del CSV
        for evento in eventos_reales:
            evento_nombre = evento['Nombre']
            evento_id = evento['id']
            fecha = evento.get('fecha', '')
            
            # Mostrar nombre del evento con ID y fecha
            texto_evento = f"{evento_nombre} (ID: {evento_id})"
            if fecha and fecha != '2025-01-01':
                texto_evento += f" - {fecha}"
            
            ttk.Radiobutton(scrollable_frame, 
                           text=texto_evento, 
                           variable=evento_var, 
                           value=evento_nombre).pack(anchor='w', pady=2)
        
        # Opción personalizada
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Radiobutton(scrollable_frame, 
                       text="Otro evento personalizado:", 
                       variable=evento_var, 
                       value="CUSTOM").pack(anchor='w', pady=2)
        
        custom_entry = ttk.Entry(scrollable_frame, width=50)
        custom_entry.pack(anchor='w', padx=(20, 0), pady=(0, 5))
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Función para usar evento personalizado
        def usar_custom():
            if custom_entry.get().strip():
                nonlocal evento_seleccionado
                evento_seleccionado = custom_entry.get().strip()
                ventana.destroy()
        
        custom_entry.bind('<Return>', lambda e: usar_custom())
        
        # Habilitar scroll con mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', bind_mousewheel)
        canvas.bind('<Leave>', unbind_mousewheel)
        
        # Botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill='x')
        
        def confirmar():
            nonlocal evento_seleccionado
            seleccion = evento_var.get()
            if seleccion and seleccion != "CUSTOM":
                evento_seleccionado = seleccion
                ventana.destroy()
            elif seleccion == "CUSTOM":
                usar_custom()
            elif not seleccion:
                messagebox.showwarning("Advertencia", "Por favor seleccione un evento")
        
        ttk.Button(botones_frame, text="✅ Confirmar", command=confirmar).pack(side='left', padx=(0, 10))
        ttk.Button(botones_frame, text="❌ Cancelar", command=ventana.destroy).pack(side='left')
        
        # Esperar a que se cierre la ventana
        ventana.wait_window()
        
        return evento_seleccionado

    def procesar_csv_evento(self, archivo, evento_seleccionado):
        """Procesa el CSV y lo integra en el sistema de múltiples eventos."""
        
        try:
            # ===============================================
            # 🎯 CARGAR Y VALIDAR CSV
            # ===============================================
            
            # Detectar encoding y separador
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            separadores = [';', ',', '\t']
            datos = None
            encoding_usado = None
            separador_usado = None
            
            for encoding in encodings:
                for sep in separadores:
                    try:
                        datos = pd.read_csv(archivo, encoding=encoding, sep=sep)
                        # Verificar que tenga las columnas esperadas
                        if 'idUsuario' in datos.columns and 'Nombrecompleto' in datos.columns:
                            encoding_usado = encoding
                            separador_usado = sep
                            self.log_message(f"✅ CSV cargado con encoding: {encoding}, separador: '{sep}'", "SUCCESS")
                            break
                    except Exception as e:
                        continue
                if datos is not None and 'idUsuario' in datos.columns:
                    break
            
            if datos is None or 'idUsuario' not in datos.columns:
                messagebox.showerror("Error", 
                    "No se pudo leer el archivo CSV o no tiene la estructura correcta.\n\n"
                    "Columnas requeridas: idUsuario, Nombrecompleto, Apellidos, Dia, Evento, Comida, Empresa, Pagado, Pais, Entrada")
                return False
            
            # Validar estructura del CSV
            columnas_esperadas = ['idUsuario', 'Nombrecompleto', 'Apellidos', 'Dia', 'Evento', 'Comida', 'Empresa', 'Pagado', 'Pais', 'Entrada']
            columnas_faltantes = [col for col in columnas_esperadas if col not in datos.columns]
            
            if columnas_faltantes:
                messagebox.showwarning("Columnas faltantes", 
                    f"El CSV no tiene todas las columnas esperadas.\n\n"
                    f"Columnas faltantes: {', '.join(columnas_faltantes)}\n\n"
                    f"¿Desea continuar de todas formas?")
                # Por ahora continuamos, pero podrías agregar lógica de confirmación
            
            # ===============================================
            # 🎯 PROCESAR DATOS DEL CSV
            # ===============================================
            
            # Limpiar y preparar datos
            datos['idUsuario'] = datos['idUsuario'].astype(str).str.strip()
            if 'Nombrecompleto' in datos.columns:
                datos['Nombrecompleto'] = datos['Nombrecompleto'].astype(str).str.strip()
            if 'Apellidos' in datos.columns:
                datos['Apellidos'] = datos['Apellidos'].astype(str).str.strip()
            
            # ===============================================
            # 🎯 INTEGRAR CON SISTEMA MULTI-EVENTO
            # ===============================================
            
            # Si es el primer CSV, inicializar master CSV
            if not self.csv_maestro_inicializado:
                self.datos_csv = datos.copy()
                self.csv_maestro_inicializado = True
                self.log_message("🎯 CSV maestro inicializado", "INFO")
            else:
                # Agregar datos al CSV maestro (sin duplicar headers)
                self.datos_csv = pd.concat([self.datos_csv, datos], ignore_index=True)
                self.log_message(f"📝 Datos agregados al CSV maestro", "INFO")
            
            # Registrar el evento como cargado
            self.eventos_cargados[evento_seleccionado] = {
                'archivo': archivo,
                'filas': len(datos),
                'timestamp': pd.Timestamp.now()
            }
            
            # FORZAR QUE SE MUESTRE ARRIBA - USAR EVENTOS REALES DEL CSV
            global EVENTOS_ACTIVOS
            
            # LIMPIAR eventos activos previos
            EVENTOS_ACTIVOS.clear()
            
            # OBTENER eventos reales del CSV cargado
            if self.datos_csv is not None:
                try:
                    eventos_reales = sorted(self.datos_csv['Evento'].unique())
                    # Agregar todos los eventos reales encontrados en el CSV
                    for evento_id in eventos_reales:
                        if pd.notna(evento_id):
                            EVENTOS_ACTIVOS.append(int(evento_id))
                    print(f"✅ EVENTOS REALES CARGADOS: {EVENTOS_ACTIVOS}")
                except Exception as e:
                    print(f"❌ Error obteniendo eventos del CSV: {e}")
                    # Fallback: usar primer evento disponible si hay datos
                    if len(self.datos_csv) > 0:
                        EVENTOS_ACTIVOS.append(999)  # Solo como fallback
                        print(f"🔧 FALLBACK: Evento 999 agregado como backup")
            else:
                EVENTOS_ACTIVOS.append(999)  # Solo si no hay datos CSV
                print(f"🚨 FALLBACK: No hay datos CSV, usando evento 999")
            
            # FORZAR actualización del display
            self.after(100, self.actualizar_eventos_display)
            
            # Actualizar modo CSV y variables necesarias
            self.modo_csv = True
            self.usar_csv = True  # Para compatibilidad
            
            # Solo actualizar archivo_csv_actual si no hay un archivo maestro activo
            if not hasattr(self, 'csv_maestro_inicializado') or not self.csv_maestro_inicializado:
                self.archivo_csv_actual = archivo  # Para el estado visual
            else:
                print(f"🎯 Manteniendo referencia al archivo maestro activo: {self.archivo_csv_actual}")
                print(f"   ➡️ CSV individual procesado: {os.path.basename(archivo)}")
            
            # Actualizar estado visual
            self.actualizar_estado_conexion("CSV")
            
            # Actualizar título de ventana
            self.actualizar_titulo_ventana()
            
            # Activar botones relevantes
            self.btn_actualizar_csv.config(state='normal')
            self.btn_descargar_csv.config(state='normal')
            self.btn_cambiar_mysql.config(state='normal')
            self.btn_gestionar_eventos.config(state='normal')
            
            # Limpiar campos de búsqueda para refrescar
            self.entry_buscar.delete(0, tk.END)
            
            # Mostrar resumen
            total_filas = len(self.datos_csv)
            eventos_count = len(self.eventos_cargados)
            
            self.log_message(
                f"📈 RESUMEN: {eventos_count} evento(s) cargados, {total_filas} registros totales", 
                "SUCCESS"
            )
            
            # Ofrecer crear CSV maestro automáticamente si hay 2 o más eventos
            if eventos_count >= 2:
                self.after(500, self.ofrecer_csv_maestro)  # Esperar un poco para que se complete la carga
            
            return True
            
        except Exception as e:
            self.log_message(f"❌ Error procesando CSV: {str(e)}", "ERROR")
            return False

    def actualizar_estado_eventos_cargados(self):
        """Actualiza la interfaz para mostrar el estado de eventos cargados."""
        
        if not self.eventos_cargados:
            return
        
        # Crear o actualizar label de estado de eventos
        if not hasattr(self, 'label_eventos_estado'):
            self.label_eventos_estado = ttk.Label(
                self.frame_estado, 
                text="", 
                font=('Segoe UI', 9)
            )
            self.label_eventos_estado.pack(pady=2)
        
        # Crear texto de resumen
        eventos_texto = []
        for evento, info in self.eventos_cargados.items():
            eventos_texto.append(f"✅ {evento} ({info['filas']} registros)")
        
        self.label_eventos_estado.config(
            text=f"🎯 Eventos cargados: {', '.join(eventos_texto[:2])}" + 
                 (f" y {len(self.eventos_cargados)-2} más..." if len(self.eventos_cargados) > 2 else "")
        )
        
        # Activar botón de gestión de eventos si hay eventos cargados
        if self.eventos_cargados:
            self.btn_gestionar_eventos.config(state='normal')
        
        # Actualizar la visualización de eventos en la interfaz principal
        self.actualizar_eventos_display()

    def ofrecer_csv_maestro(self):
        """Ofrece automáticamente crear un CSV maestro cuando hay múltiples eventos cargados."""
        try:
            if len(self.eventos_cargados) < 2:
                return
            
            # Solo ofrecer si no se ha creado ya un archivo maestro en esta sesión
            if not hasattr(self, '_csv_maestro_ofrecido'):
                self._csv_maestro_ofrecido = True
                
                respuesta = messagebox.askyesno("💡 Crear CSV Maestro",
                    f"🎯 Tienes {len(self.eventos_cargados)} eventos cargados.\n\n"
                    f"¿Te gustaría crear un archivo CSV maestro consolidado?\n\n"
                    f"✅ Ventajas:\n"
                    f"• Un solo archivo con todos los datos\n"
                    f"• Ideal para usar durante toda la jornada\n"
                    f"• Respaldo consolidado de todos los eventos\n"
                    f"• Registro único y organizado\n\n"
                    f"💡 Recomendado: SÍ para eventos de múltiples días",
                    icon='question')
                
                if respuesta:
                    self.reconstruir_csv_maestro()
        except Exception as e:
            self.log_message(f"⚠️ Error ofreciendo CSV maestro: {str(e)}", "ERROR")

    def mostrar_gestor_eventos(self):
        """Muestra ventana para gestionar eventos CSV cargados."""
        
        if not self.eventos_cargados:
            messagebox.showinfo("Sin eventos", "No hay eventos CSV cargados para gestionar.")
            return
        
        # Crear ventana modal
        ventana = tk.Toplevel(self)
        ventana.title("🎯 Gestor de Eventos CSV")
        ventana.geometry("700x500")
        ventana.transient(self)
        ventana.grab_set()
        
        # Centrar ventana
        ventana.geometry("+%d+%d" % (self.winfo_rootx() + 50, self.winfo_rooty() + 50))
        
        # Frame principal
        main_frame = ttk.Frame(ventana, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(main_frame,
                          text="🎯 Gestión de Eventos CSV Cargados",
                          font=('Segoe UI', 14, 'bold'))
        titulo.pack(pady=(0, 20))
        
        # Frame para estadísticas generales
        stats_frame = ttk.LabelFrame(main_frame, text="📊 Estadísticas Generales", padding=10)
        stats_frame.pack(fill='x', pady=(0, 15))
        
        total_eventos = len(self.eventos_cargados)
        total_registros = len(self.datos_csv) if hasattr(self, 'datos_csv') and self.datos_csv is not None else 0
        
        ttk.Label(stats_frame, 
                 text=f"🎭 Total de eventos: {total_eventos}",
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        ttk.Label(stats_frame, 
                 text=f"👥 Total de registros: {total_registros}",
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        
        # Frame para lista de eventos
        lista_frame = ttk.LabelFrame(main_frame, text="📋 Eventos Cargados", padding=10)
        lista_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Crear Treeview para mostrar eventos
        columns = ('Evento', 'Registros', 'Archivo', 'Fecha/Hora')
        tree = ttk.Treeview(lista_frame, columns=columns, show='headings', height=8)
        
        # Configurar columnas
        tree.heading('Evento', text='🎭 Evento')
        tree.heading('Registros', text='👥 Registros')
        tree.heading('Archivo', text='📄 Archivo')
        tree.heading('Fecha/Hora', text='🕒 Cargado')
        
        tree.column('Evento', width=200)
        tree.column('Registros', width=80, anchor='center')
        tree.column('Archivo', width=200)
        tree.column('Fecha/Hora', width=150, anchor='center')
        
        # Insertar datos de eventos
        for evento, info in self.eventos_cargados.items():
            archivo_nombre = os.path.basename(info['archivo'])
            fecha_formato = info['timestamp'].strftime("%d/%m/%Y %H:%M")
            
            tree.insert('', tk.END, values=(
                evento,
                info['filas'],
                archivo_nombre,
                fecha_formato
            ))
        
        # Scrollbar para el tree
        scrollbar = ttk.Scrollbar(lista_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame para botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill='x', pady=(10, 0))
        
        def eliminar_evento():
            global EVENTOS_ACTIVOS
            
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un evento para eliminar")
                return
            
            # Obtener evento seleccionado
            item = tree.item(seleccion[0])
            evento_nombre = item['values'][0]
            
            # Confirmar eliminación
            if messagebox.askyesno("Confirmar", f"¿Eliminar el evento '{evento_nombre}'?"):
                # Encontrar el ID del evento para eliminarlo de eventos activos
                evento_id_a_eliminar = None
                if evento_nombre in self.eventos_cargados:
                    # Buscar el ID del evento en los datos CSV
                    evento_data = self.eventos_cargados[evento_nombre]
                    if hasattr(evento_data, 'get') and 'Evento' in evento_data:
                        evento_id_a_eliminar = evento_data['Evento']
                    elif self.datos_csv is not None:
                        # Buscar en los datos CSV
                        eventos_unicos = self.datos_csv['Evento'].unique()
                        for eid in eventos_unicos:
                            nombre_ev = self.obtener_nombre_evento_csv(eid)
                            if nombre_ev == evento_nombre:
                                evento_id_a_eliminar = eid
                                break
                
                # Eliminar del diccionario
                del self.eventos_cargados[evento_nombre]
                
                # Eliminar de eventos activos si está presente
                if evento_id_a_eliminar and evento_id_a_eliminar in EVENTOS_ACTIVOS:
                    EVENTOS_ACTIVOS.remove(evento_id_a_eliminar)
                    print(f"🗑️ Evento {evento_id_a_eliminar} eliminado de EVENTOS_ACTIVOS")
                
                # Reconstruir CSV maestro sin este evento
                if self.eventos_cargados:
                    self.reconstruir_csv_maestro()
                else:
                    # Si no quedan eventos, limpiar todo
                    self.datos_csv = None
                    self.csv_maestro_inicializado = False
                    self.usar_csv = False
                    self.modo_csv = False
                    
                    # Limpiar eventos activos
                    EVENTOS_ACTIVOS.clear()
                    
                    # Actualizar estado a MySQL
                    self.actualizar_estado_conexion("MySQL")
                    self.btn_gestionar_eventos.config(state='disabled')
                    
                    # Actualizar display de eventos
                    self.actualizar_eventos_display()
                    
                    # Actualizar título de ventana
                    self.actualizar_titulo_ventana()
                
                # Actualizar ventana
                tree.delete(seleccion[0])
                self.actualizar_estado_eventos_cargados()
                
                # Actualizar display de eventos si quedan eventos
                if self.eventos_cargados:
                    self.actualizar_eventos_display()
                
                messagebox.showinfo("Éxito", f"Evento '{evento_nombre}' eliminado correctamente")
        
        def cargar_otro_evento():
            ventana.destroy()
            self.cargar_csv()
        
        def crear_csv_maestro():
            if len(self.eventos_cargados) < 2:
                messagebox.showwarning("Advertencia", 
                    "Se necesitan al menos 2 eventos cargados para crear un CSV maestro.\n\n"
                    "Carga más eventos usando el botón '➕ Cargar Otro Evento'.")
                return
            
            respuesta = messagebox.askyesno("Crear CSV Maestro",
                f"¿Deseas crear un archivo CSV maestro consolidado?\n\n"
                f"📊 Se combinarán {len(self.eventos_cargados)} eventos\n"
                f"📁 Se creará un nuevo archivo con todos los registros\n\n"
                f"Esto es útil para tener un archivo único con todos los\n"
                f"datos de los eventos que se mantendrá durante toda la jornada.")
            
            if respuesta:
                if self.reconstruir_csv_maestro():
                    # Si se creó exitosamente, cerrar la ventana del gestor
                    ventana.destroy()
        
        # Botones
        ttk.Button(botones_frame, text="➕ Cargar Otro Evento", command=cargar_otro_evento).pack(side='left', padx=(0, 10))
        ttk.Button(botones_frame, text="🗑️ Eliminar Evento", command=eliminar_evento).pack(side='left', padx=(0, 10))
        
        # Botón CSV Maestro solo si hay múltiples eventos
        if len(self.eventos_cargados) >= 2:
            ttk.Button(botones_frame, text="📄 Crear CSV Maestro", command=crear_csv_maestro).pack(side='left', padx=(0, 10))
        
        ttk.Button(botones_frame, text="✅ Cerrar", command=ventana.destroy).pack(side='right')

    def reconstruir_csv_maestro(self):
        """Reconstruye el CSV maestro desde todos los eventos cargados y crea un archivo físico consolidado."""
        
        if not self.eventos_cargados:
            self.log_message("❌ No hay eventos cargados para reconstruir CSV maestro", "ERROR")
            return False
        
        # Recargar todos los CSVs
        datos_combinados = []
        eventos_nombres = []
        total_registros_por_evento = {}
        
        self.log_message("🔄 Iniciando reconstrucción de CSV maestro...", "INFO")
        
        for evento, info in self.eventos_cargados.items():
            try:
                # Recargar cada CSV
                datos_evento = pd.read_csv(info['archivo'])
                datos_combinados.append(datos_evento)
                eventos_nombres.append(evento.replace(' ', '_'))  # Reemplazar espacios para nombre de archivo
                total_registros_por_evento[evento] = len(datos_evento)
                self.log_message(f"📄 Recargado: {evento} ({len(datos_evento)} registros)", "INFO")
            except Exception as e:
                self.log_message(f"❌ Error recargando {evento}: {str(e)}", "ERROR")
                continue
        
        if not datos_combinados:
            self.log_message("❌ No se pudieron cargar datos de ningún evento", "ERROR")
            return False
        
        # Combinar todos los DataFrames
        self.datos_csv = pd.concat(datos_combinados, ignore_index=True)
        total_registros = len(self.datos_csv)
        
        # Crear nombre del archivo maestro con fecha y hora
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        eventos_str = "_".join(eventos_nombres[:3])  # Máximo 3 nombres para evitar nombres muy largos
        if len(eventos_nombres) > 3:
            eventos_str += f"_y_{len(eventos_nombres)-3}_mas"
        
        nombre_archivo_maestro = f"CSV_MAESTRO_{eventos_str}_{timestamp}.csv"
        
        try:
            # Guardar el archivo maestro con el mismo formato que los CSVs originales
            self.datos_csv.to_csv(nombre_archivo_maestro, index=False, encoding='utf-8-sig', sep=';')
            
            # Actualizar referencia al archivo actual
            self.archivo_csv_actual = os.path.abspath(nombre_archivo_maestro)
            
            # Log detallado del resultado
            self.log_message(f"✅ CSV maestro creado exitosamente!", "SUCCESS")
            self.log_message(f"📁 Archivo: {nombre_archivo_maestro}", "INFO")
            self.log_message(f"📊 Total registros: {total_registros}", "INFO")
            
            # Mostrar resumen por evento
            for evento, count in total_registros_por_evento.items():
                self.log_message(f"   • {evento}: {count} registros", "INFO")
            
            # Actualizar título de ventana
            self.actualizar_titulo_ventana()
            
            messagebox.showinfo("CSV Maestro Creado", 
                f"✅ Archivo maestro consolidado creado exitosamente!\n\n"
                f"📁 Archivo: {nombre_archivo_maestro}\n"
                f"📊 Total de registros: {total_registros}\n"
                f"🎯 Eventos incluidos: {len(self.eventos_cargados)}\n\n"
                f"💡 Este archivo contiene todos los datos de los eventos cargados\n"
                f"y será usado como fuente principal durante la sesión.")
            
            return True
            
        except Exception as e:
            self.log_message(f"❌ Error al guardar CSV maestro: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"No se pudo crear el archivo maestro:\n{str(e)}")
            return False
            self.csv_maestro_inicializado = False

    def actualizar_csv(self):
        """Recarga el mismo archivo CSV para obtener datos actualizados."""
        if not self.archivo_csv_actual:
            messagebox.showwarning("Advertencia", "No hay ningún archivo CSV cargado.")
            return
        
        if not os.path.exists(self.archivo_csv_actual):
            messagebox.showerror("Error", "El archivo CSV original no existe.\nSeleccione un nuevo archivo.")
            return
        
        # Recargar el mismo archivo
        archivo_temp = self.archivo_csv_actual
        self.archivo_csv_actual = None
        self.datos_csv = None
        
        # Simular carga del mismo archivo
        self.archivo_csv_actual = archivo_temp
        self.cargar_csv_silencioso(archivo_temp)

    def cargar_csv_silencioso(self, archivo):
        """Carga un archivo CSV sin mostrar diálogos de selección."""
        try:
            # Detectar encoding y separador
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            separadores = [';', ',', '\t']
            datos = None
            
            for encoding in encodings:
                for sep in separadores:
                    try:
                        datos = pd.read_csv(archivo, encoding=encoding, sep=sep)
                        # Verificar que tenga las columnas esperadas de la BD
                        if 'idUsuario' in datos.columns and 'Nombrecompleto' in datos.columns:
                            break
                    except Exception:
                        continue
                if datos is not None and 'idUsuario' in datos.columns:
                    break
            
            if datos is None or 'idUsuario' not in datos.columns:
                messagebox.showerror("Error", "No se pudo recargar el archivo CSV o no tiene la estructura correcta.")
                return
            
            # Limpiar datos
            datos['idUsuario'] = datos['idUsuario'].astype(str).str.strip()
            if 'Nombrecompleto' in datos.columns:
                datos['Nombrecompleto'] = datos['Nombrecompleto'].astype(str).str.strip()
            
            self.datos_csv = datos
            total_registros = len(datos)
            nombre_archivo = os.path.basename(archivo)
            
            messagebox.showinfo("CSV Actualizado", 
                f"🔄 Datos actualizados exitosamente!\n\n"
                f"📄 Archivo: {nombre_archivo}\n"
                f"👥 Registros: {total_registros}")
            
            print(f"🔄 CSV actualizado: {total_registros} registros")
            
        except Exception as e:
            print(f"❌ Error actualizando CSV: {e}")
            messagebox.showerror("Error", f"Error al actualizar CSV:\n{str(e)}")

    def cargar_eventos_csv(self):
        """Carga automáticamente el archivo de eventos CSV."""
        archivo_eventos = "Eventos_Etiquetas.csv"
        
        try:
            if not os.path.exists(archivo_eventos):
                print(f"⚠️ No se encontró {archivo_eventos}, continuando sin eventos CSV")
                return
            
            print(f"📁 Cargando eventos CSV: {archivo_eventos}")
            
            # Detectar encoding y separador para eventos
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            separadores = [';', ',', '\t']
            eventos = None
            
            for encoding in encodings:
                for sep in separadores:
                    try:
                        eventos_temp = pd.read_csv(archivo_eventos, encoding=encoding, sep=sep)
                        # Verificar que tenga las columnas esperadas de eventos
                        if 'id' in eventos_temp.columns and 'Nombre' in eventos_temp.columns:
                            eventos = eventos_temp
                            print(f"✅ Eventos CSV cargado con encoding: {encoding}, separador: '{sep}'")
                            break
                    except Exception:
                        continue
                if eventos is not None:
                    break
            
            if eventos is None:
                print(f"❌ No se pudo cargar {archivo_eventos}")
                return
            
            # Limpiar y procesar datos de eventos
            eventos['id'] = eventos['id'].astype(str).str.strip()
            eventos['Nombre'] = eventos['Nombre'].astype(str).str.strip()
            
            # Agregar campos opcionales con valores por defecto si no existen
            if 'fecha' not in eventos.columns:
                eventos['fecha'] = '2025-01-01'  # Fecha por defecto
            if 'dia' not in eventos.columns:
                eventos['dia'] = '1'  # Día por defecto
            
            # Guardar eventos CSV
            self.eventos_csv = eventos
            self.archivo_eventos_csv = archivo_eventos
            
            print(f"📊 Eventos CSV cargados: {len(eventos)} eventos disponibles")
            print(f"📋 Eventos disponibles: {', '.join(eventos['Nombre'].tolist()[:5])}{'...' if len(eventos) > 5 else ''}")
            
        except Exception as e:
            print(f"❌ Error cargando eventos CSV: {e}")
            self.eventos_csv = None

    def obtener_eventos_csv(self):
        """Obtiene la lista de eventos desde el CSV cargado."""
        if self.eventos_csv is None:
            return []
        
        try:
            eventos = []
            for _, fila in self.eventos_csv.iterrows():
                evento = {
                    'id': int(fila['id']),
                    'Nombre': str(fila['Nombre']).strip(),
                    'fecha': str(fila.get('fecha', '2025-01-01')),
                    'dia': str(fila.get('dia', '1'))
                }
                eventos.append(evento)
            
            return eventos
            
        except Exception as e:
            print(f"❌ Error procesando eventos CSV: {e}")
            return []

    def obtener_nombre_evento_csv(self, evento_id):
        """Obtiene el nombre de un evento desde el CSV de eventos."""
        if self.eventos_csv is None:
            return f"Evento {evento_id}"
        
        try:
            # Buscar el evento por ID
            mask = self.eventos_csv['id'].astype(str).str.strip() == str(evento_id).strip()
            resultado = self.eventos_csv[mask]
            
            if not resultado.empty:
                return resultado.iloc[0]['Nombre']
            else:
                return f"Evento {evento_id}"
                
        except Exception as e:
            print(f"Error al obtener nombre de evento CSV: {e}")
            return f"Evento {evento_id}"

    def obtener_nombre_evento_mysql(self, evento_id):
        """Obtiene el nombre de un evento desde MySQL."""
        try:
            eventos = self.obtener_eventos_seguro()
            return obtener_nombre_evento(evento_id, eventos)
        except Exception as e:
            print(f"Error al obtener nombre de evento MySQL: {e}")
            return f"Evento {evento_id}"
            print(f"❌ Error obteniendo nombre de evento CSV: {e}")
            return f"Evento {evento_id}"

    def buscar_usuario_csv(self, id_usuario):
        """Busca un usuario en los datos CSV cargados usando la estructura de la BD."""
        if not self.modo_csv or self.datos_csv is None:
            return None
        
        try:
            # Buscar en el DataFrame usando idUsuario (igual que en MySQL)
            mask = self.datos_csv['idUsuario'].astype(str).str.strip() == str(id_usuario).strip()
            resultado = self.datos_csv[mask]
            
            if resultado.empty:
                return None
            
            # Obtener el primer resultado
            fila = resultado.iloc[0]
            
            # Crear diccionario con estructura idéntica a MySQL
            usuario = {}
            
            # Campos principales (siempre presentes)
            usuario['idUsuario'] = str(fila.get('idUsuario', '')).strip()
            usuario['Nombrecompleto'] = str(fila.get('Nombrecompleto', '')).strip()
            
            # Campos opcionales (pueden no estar en el CSV)
            campos_opcionales = ['Apellidos', 'Dia', 'Evento', 'Comida', 'Empresa', 'Pagado', 'Pais', 'Entrada', 'Pirata']
            
            for campo in campos_opcionales:
                if campo == 'Comida':
                    # Lógica especial para Comida: buscar tanto mayúscula como minúscula
                    valor = fila.get('Comida', fila.get('comida', None))
                    if valor is not None and not pd.isna(valor):
                        usuario['comida'] = str(valor).strip()  # Usar 'comida' minúscula para consistencia interna
                    else:
                        usuario['comida'] = '0'  # Por defecto no ha sido escaneado
                elif campo == 'Pirata':
                    # Lógica especial para Pirata: buscar tanto mayúscula como minúscula
                    valor = fila.get('Pirata', fila.get('pirata', None))
                    if valor is not None and not pd.isna(valor):
                        usuario['pirata'] = str(valor).strip()  # Usar 'pirata' minúscula para consistencia interna
                    else:
                        usuario['pirata'] = '0'  # Por defecto sí debe recibir mochila
                elif campo in fila:
                    valor = fila[campo]
                    # Limpiar valores None o NaN
                    if pd.isna(valor):
                        usuario[campo] = ''
                    else:
                        valor_limpio = str(valor).strip()
                        usuario[campo] = valor_limpio
                else:
                    # Valores por defecto para campos faltantes
                    if campo == 'Dia':
                        usuario[campo] = '1'
                    elif campo == 'Evento':
                        usuario[campo] = '0'
                    elif campo == 'Comida':
                        usuario[campo] = '0'
                    elif campo == 'Pagado':
                        usuario[campo] = '1'
                    elif campo == 'Entrada':
                        usuario[campo] = ''
                    else:
                        usuario[campo] = ''
            
            print(f"✅ Usuario encontrado en CSV: {usuario['idUsuario']} - {usuario['Nombrecompleto']}")
            # Debug: Mostrar valor de pirata específicamente
            if 'pirata' in usuario:
                print(f"🎒 Campo pirata encontrado: '{usuario['pirata']}' (tipo: {type(usuario['pirata'])})")
            else:
                print("❌ Campo pirata NO encontrado en usuario")
            return usuario
            
        except Exception as e:
            print(f"❌ Error buscando usuario en CSV: {e}")
            return None

    def marcar_comida_csv(self, id_usuario):
        """Marca comida = 1 en el CSV cargado y lo guarda."""
        try:
            print(f"🍽️ Marcando comida en CSV para usuario ID: {id_usuario}...")
            
            if not self.modo_csv or self.datos_csv is None:
                print("❌ No hay datos CSV cargados")
                return False
            
            # Verificar si hay un archivo maestro activo
            archivo_a_usar = self.archivo_csv_actual
            archivo_tipo = "individual"
            
            # Si hay un archivo maestro inicializado, usarlo preferentemente
            if hasattr(self, 'csv_maestro_inicializado') and self.csv_maestro_inicializado:
                # Buscar archivo maestro más reciente
                import glob
                archivos_maestros = glob.glob("CSV_MAESTRO_*.csv")
                if archivos_maestros:
                    # Usar el más reciente
                    archivo_maestro_reciente = max(archivos_maestros, key=os.path.getmtime)
                    archivo_a_usar = archivo_maestro_reciente
                    archivo_tipo = "maestro"
                    print(f"🎯 Usando archivo maestro: {os.path.basename(archivo_maestro_reciente)}")
                    
                    # Actualizar la referencia para futuras operaciones
                    self.archivo_csv_actual = os.path.abspath(archivo_maestro_reciente)
            
            # Mostrar qué archivo se va a actualizar
            archivo_nombre = os.path.basename(archivo_a_usar) if archivo_a_usar else "archivo desconocido"
            print(f"📁 Actualizando archivo {archivo_tipo}: {archivo_nombre}")
            
            # Buscar el usuario en el DataFrame
            mask = self.datos_csv['idUsuario'].astype(str).str.strip() == str(id_usuario).strip()
            indices = self.datos_csv.index[mask]
            
            if len(indices) == 0:
                print(f"⚠️ Usuario {id_usuario} no encontrado en CSV")
                return False
            
            # Marcar comida = 1 para el usuario
            self.datos_csv.loc[indices, 'Comida'] = 1
            
            # Guardar el CSV actualizado
            try:
                self.datos_csv.to_csv(archivo_a_usar, sep=';', encoding='utf-8', index=False)
                print(f"✅ Comida marcada y CSV actualizado para usuario {id_usuario}")
                print(f"📄 Archivo guardado: {archivo_nombre}")
                print(f"🎯 Tipo de archivo usado: {archivo_tipo}")
                return True
            except Exception as e:
                print(f"❌ Error guardando CSV: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Error marcando comida en CSV: {e}")
            return False

    def actualizar_estado_conexion(self, modo):
        """Actualiza el indicador visual del estado de conexión con mayor diferenciación."""
        if modo == "CSV":
            nombre_archivo = os.path.basename(self.archivo_csv_actual) if self.archivo_csv_actual else "archivo.csv"
            # Contar eventos cargados
            num_eventos = len(self.eventos_cargados) if self.eventos_cargados else 1
            total_registros = len(self.datos_csv) if hasattr(self, 'datos_csv') and self.datos_csv is not None else 0
            
            self.estado_label.config(
                text=f"� MODO OFFLINE - CSV: {nombre_archivo} ({num_eventos} evento(s), {total_registros} registros)",
                foreground='#E67E22',  # Naranja distintivo
                font=('Segoe UI', 10, 'bold')
            )
        elif modo == "MySQL":
            self.estado_label.config(
                text="🌐 MODO ONLINE - Conectado a MySQL Server",
                foreground='#27AE60',  # Verde distintivo
                font=('Segoe UI', 10, 'bold')
            )
        elif modo == "Error":
            self.estado_label.config(
                text="❌ SIN CONEXIÓN - Error de red",
                foreground='#E74C3C',  # Rojo distintivo
                font=('Segoe UI', 10, 'bold')
            )
        else:
            self.estado_label.config(
                text="🔍 DETECTANDO CONEXIÓN...",
                foreground='#F39C12',  # Amarillo/naranja
                font=('Segoe UI', 10, 'normal')
            )

    def descargar_csv(self):
        """Descarga/elimina el archivo CSV y vuelve a modo MySQL."""
        if not self.modo_csv:
            messagebox.showinfo("Información", "No hay ningún archivo CSV cargado actualmente.")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar Descarga de CSV", 
            "¿Estás seguro de que quieres descargar el modo CSV y cambiar a MySQL?\n\n"
            "• Se eliminará el archivo CSV cargado\n"
            "• El sistema cambiará automáticamente a modo MySQL\n"
            "• Se restablecerá la conexión a la base de datos\n\n"
            "¿Continuar?"
        )
        
        if not respuesta:
            return
        
        try:
            # Limpiar datos CSV
            self.datos_csv = None
            self.eventos_csv = None
            self.archivo_csv_actual = None
            self.archivo_eventos_csv = None
            self.modo_csv = False
            
            # Desactivar botones CSV
            self.btn_actualizar_csv.config(state='disabled')
            self.btn_descargar_csv.config(state='disabled')
            self.btn_cambiar_mysql.config(state='disabled')
            
            # Intentar conectar a MySQL
            self.verificar_conexiones_inicial()
            
            # Actualizar estado visual
            self.actualizar_estado_conexion("MySQL")
            
            # Actualizar título de ventana
            self.actualizar_titulo_ventana()
            
            # Actualizar eventos display
            self.actualizar_eventos_display()
            
            messagebox.showinfo("Modo Cambiado", 
                "✅ Modo CSV descargado exitosamente!\n\n"
                "🌐 El sistema ahora funciona en modo MySQL.\n"
                "📡 Conexión a base de datos restablecida.")
            
            self.log_message("Modo cambiado de CSV a MySQL exitosamente", "SUCCESS")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cambiar a modo MySQL:\n{str(e)}")
            self.log_message(f"Error cambiando a MySQL: {str(e)}", "ERROR")

    def cambiar_a_mysql(self):
        """Cambia del modo CSV al modo MySQL sin eliminar el CSV cargado."""
        if not self.modo_csv:
            messagebox.showinfo("Información", "El sistema ya está en modo MySQL.")
            return
        
        respuesta = messagebox.askyesno(
            "Cambiar a Modo MySQL", 
            "¿Quieres cambiar a modo MySQL?\n\n"
            "• Se mantendrá el archivo CSV cargado\n"
            "• El sistema usará la base de datos MySQL\n"
            "• Podrás volver a CSV cuando quieras\n\n"
            "¿Continuar?"
        )
        
        if not respuesta:
            return
        
        try:
            # Cambiar modo pero mantener datos CSV
            self.modo_csv = False
            
            # Verificar conexión MySQL
            self.verificar_conexiones_inicial()
            
            # Actualizar estado visual
            self.actualizar_estado_conexion("MySQL")
            
            # Actualizar título de ventana
            self.actualizar_titulo_ventana()
            
            # Actualizar botones
            self.btn_cambiar_mysql.config(state='disabled')
            self.btn_actualizar_csv.config(state='disabled')
            
            # Agregar botón para volver a CSV
            if hasattr(self, 'btn_volver_csv'):
                self.btn_volver_csv.config(state='normal')
            else:
                # Crear botón para volver a CSV si no existe
                self.btn_volver_csv = ttk.Button(self.estado_frame.master,
                                               text="💾 Volver a CSV",
                                               command=self.volver_a_csv,
                                               state='normal')
                self.btn_volver_csv.pack(side='left', padx=(0, 10))
            
            # Actualizar eventos display
            self.actualizar_eventos_display()
            
            messagebox.showinfo("Modo Cambiado", 
                "✅ Cambiado a modo MySQL exitosamente!\n\n"
                "🌐 El sistema ahora usa la base de datos.\n"
                "💾 El CSV queda disponible para uso posterior.")
            
            self.log_message("Modo cambiado de CSV a MySQL (CSV conservado)", "SUCCESS")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cambiar a modo MySQL:\n{str(e)}")
            self.log_message(f"Error cambiando a MySQL: {str(e)}", "ERROR")

    def volver_a_csv(self):
        """Vuelve al modo CSV usando los datos previamente cargados."""
        if self.datos_csv is None:
            messagebox.showwarning("Advertencia", "No hay datos CSV disponibles. Carga un archivo CSV primero.")
            return
        
        try:
            # Cambiar a modo CSV
            self.modo_csv = True
            
            # Actualizar estado visual
            self.actualizar_estado_conexion("CSV")
            
            # Actualizar botones
            self.btn_actualizar_csv.config(state='normal')
            self.btn_descargar_csv.config(state='normal')
            self.btn_cambiar_mysql.config(state='normal')
            if hasattr(self, 'btn_volver_csv'):
                self.btn_volver_csv.config(state='disabled')
            
            # Actualizar eventos display
            self.actualizar_eventos_display()
            
            nombre_archivo = os.path.basename(self.archivo_csv_actual) if self.archivo_csv_actual else "archivo.csv"
            total_registros = len(self.datos_csv)
            
            messagebox.showinfo("Modo Cambiado", 
                f"✅ Cambiado a modo CSV exitosamente!\n\n"
                f"📄 Archivo: {nombre_archivo}\n"
                f"👥 Registros: {total_registros}\n"
                f"💾 Funcionando en modo offline.")
            
            self.log_message("Modo cambiado de MySQL a CSV", "SUCCESS")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cambiar a modo CSV:\n{str(e)}")
            self.log_message(f"Error cambiando a CSV: {str(e)}", "ERROR")

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
        
        # Verificar estado del sistema
        modo_texto = "📊 CSV" if self.modo_csv else "🌐 MySQL"
        print(f"👥 Iniciando tabla de usuarios - Modo: {modo_texto}")
        print(f"📋 Eventos activos: {EVENTOS_ACTIVOS}")
        
        if not EVENTOS_ACTIVOS:
            if self.modo_csv:
                mensaje = ('⚠️ No hay eventos seleccionados en modo CSV.\n\n'
                          '📋 Para usar la tabla de usuarios:\n'
                          '1. Carga un archivo CSV con datos de usuarios\n'
                          '2. Selecciona eventos en el selector de eventos\n'
                          '3. Vuelve a hacer clic en "Tabla de Usuarios"')
            else:
                mensaje = ('⚠️ No hay eventos seleccionados.\n\n'
                          'Por favor selecciona al menos un evento primero.')
            
            messagebox.showwarning('Advertencia', mensaje)
            return
        
        # Verificar datos disponibles en CSV
        if self.modo_csv and self.datos_csv is None:
            messagebox.showwarning('Sin datos CSV', 
                'No hay datos CSV cargados.\n\n'
                'Por favor carga un archivo CSV primero usando el botón "📄 Cargar CSV".')
            return
        
        # Obtener eventos una sola vez para reutilizar
        try:
            # Usar la fuente correcta según el modo
            if self.modo_csv:
                eventos = self.obtener_eventos_csv()
                print(f"📊 Eventos CSV disponibles: {len(eventos)}")
            else:
                eventos = self.obtener_eventos_seguro()
                print(f"🌐 Eventos MySQL disponibles: {len(eventos)}")
            eventos_dict = {e['id']: e for e in eventos}
        except Exception as e:
            error_msg = f'Error al obtener eventos ({modo_texto}):\n{str(e)}'
            print(f"❌ {error_msg}")
            messagebox.showerror('Error', error_msg)
            return
        
        # Obtener usuarios de los eventos activos
        print(f"🔍 Obteniendo usuarios para eventos: {EVENTOS_ACTIVOS}")
        usuarios = self.obtener_usuarios_eventos_activos()
        
        if not usuarios:
            if self.modo_csv:
                mensaje = (f'📊 No se encontraron usuarios para los eventos seleccionados en CSV.\n\n'
                          f'🎯 Eventos buscados: {EVENTOS_ACTIVOS}\n'
                          f'💡 Verifica que el CSV contenga usuarios para estos eventos.\n'
                          f'📋 Columna "Evento" debe coincidir con los IDs seleccionados.')
            else:
                mensaje = 'No se encontraron usuarios para los eventos seleccionados.'
            
            messagebox.showinfo('Sin resultados', mensaje)
            return
        
        print(f"✅ Encontrados {len(usuarios)} usuarios para mostrar en tabla")
        
        # Crear ventana de tabla
        ventana_tabla = tk.Toplevel(self)
        modo_texto = "📊 CSV" if self.modo_csv else "🌐 MySQL"
        ventana_tabla.title(f"👥 Tabla de Usuarios - Pulseras Entregadas ({modo_texto})")
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
        
        modo_texto = "📊 CSV" if self.modo_csv else "🌐 MySQL"
        titulo_texto = f"👥 USUARIOS DE EVENTOS SELECCIONADOS ({modo_texto})\nEventos: {' | '.join(eventos_nombres)}"
        titulo = ttk.Label(main_frame,
                          text=titulo_texto,
                          style='Title.TLabel')
        titulo.pack(pady=(0, 15))
        
        # Frame para búsqueda
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill='x', pady=(0, 10))
        
        # Campo de búsqueda
        search_label = ttk.Label(search_frame, text="🔍 Buscar por nombre o apellidos:")
        search_label.pack(side='left', padx=(0, 10))
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
        search_entry.pack(side='left', padx=(0, 10))
        
        # Botón de limpiar búsqueda
        clear_btn = ttk.Button(search_frame, text="🗑️ Limpiar", 
                              command=lambda: self.limpiar_busqueda_tabla(search_var, tree, usuarios, eventos_dict))
        clear_btn.pack(side='left', padx=(0, 10))
        
        # Frame para la tabla
        tabla_frame = ttk.Frame(main_frame)
        tabla_frame.pack(fill='both', expand=True)
        
        # Crear Treeview con scrollbars
        columns = ('ID', 'Nombre', 'Apellidos', 'Empresa', 'Entrada', 'Evento', 'Pulsera', 'Mochila')
        tree = ttk.Treeview(tabla_frame, columns=columns, show='headings', height=20)
        
        # Configurar columnas
        tree.heading('ID', text='ID Usuario')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Apellidos', text='Apellidos')
        tree.heading('Empresa', text='Empresa')
        tree.heading('Entrada', text='Tipo Entrada')
        tree.heading('Evento', text='Evento')
        tree.heading('Pulsera', text='Pulsera Entregada')
        tree.heading('Mochila', text='Mochila')
        
        # Ajustar ancho de columnas
        tree.column('ID', width=80, minwidth=60)
        tree.column('Nombre', width=120, minwidth=100)
        tree.column('Apellidos', width=120, minwidth=100)
        tree.column('Empresa', width=200, minwidth=150)
        tree.column('Entrada', width=100, minwidth=80)
        tree.column('Evento', width=150, minwidth=120)
        tree.column('Pulsera', width=120, minwidth=100)
        tree.column('Mochila', width=100, minwidth=80)
        
        # Configurar búsqueda en tiempo real
        def buscar_en_tabla(*args):
            self.filtrar_tabla_usuarios(search_var.get(), tree, usuarios, eventos_dict)
        
        search_var.trace('w', buscar_en_tabla)
        
        # Configurar doble clic para imprimir etiqueta
        def on_double_click(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                id_usuario = item['values'][0]
                self.imprimir_etiqueta_desde_tabla(id_usuario)
        
        tree.bind('<Double-1>', on_double_click)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tabla_frame, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Insertar datos (usar eventos_dict para evitar consultas repetidas)
        for usuario in usuarios:
            pulsera_texto = "✅ SÍ" if usuario.get('comida', 0) == 1 else "❌ NO"
            # Mochila: pirata = 1 (no mochila), pirata = 0 (sí mochila)
            mochila_texto = "❌ NO" if usuario.get('pirata', 0) == 1 else "✅ SÍ"
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
                pulsera_texto,
                mochila_texto
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
        
        # Calcular mochilas usando la misma lógica compleja de prioridades
        con_mochila = 0
        for u in usuarios:
            # Obtener tipo de entrada
            entrada = u.get('entrada', '').upper()
            pirata = u.get('pirata', 0)
            
            # 1ª PRIORIDAD: Si es entrada EXPO → NUNCA mochila
            if 'EXPO' in entrada:
                mochila = False
            # 2ª PRIORIDAD: Si pirata=1 → NO mochila
            elif pirata == 1:
                mochila = False
            # 3ª PRIORIDAD: Si pirata=0 y NO es EXPO → SÍ mochila  
            elif pirata == 0:
                mochila = True
            else:
                mochila = False
                
            if mochila:
                con_mochila += 1
                
        sin_mochila = total_usuarios - con_mochila
        
        modo_texto = "📊 CSV" if self.modo_csv else "🌐 MySQL"
        stats_text = f"📊 Total: {total_usuarios} usuarios | ✅ Con pulsera: {con_pulsera} | ❌ Sin pulsera: {sin_pulsera} | 🎒 Con mochila: {con_mochila} | ❌ Sin mochila: {sin_mochila} | Fuente: {modo_texto}"
        stats_label = ttk.Label(stats_frame, text=stats_text, font=('Arial', 11, 'bold'))
        stats_label.pack(side='left')
        
        # Frame para botones
        buttons_frame = ttk.Frame(stats_frame)
        buttons_frame.pack(side='right')
        
        # Botón imprimir etiqueta seleccionada
        btn_imprimir = ttk.Button(buttons_frame,
                                 text="🖨️ Imprimir Etiqueta",
                                 command=lambda: self.imprimir_etiqueta_seleccionada(tree),
                                 style='Success.TButton')
        btn_imprimir.pack(side='left', padx=(0, 10))
        
        # Botón actualizar
        btn_actualizar = ttk.Button(buttons_frame,
                                   text="🔄 Actualizar",
                                   command=lambda: self.actualizar_tabla_usuarios_optimizada(tree),
                                   style='Info.TButton')
        btn_actualizar.pack(side='left', padx=(0, 10))
        
        # Botón cerrar
        btn_cerrar = ttk.Button(buttons_frame,
                               text="✖ Cerrar",
                               command=ventana_tabla.destroy,
                               style='Danger.TButton')
        btn_cerrar.pack(side='left')
        
        # Label de instrucciones
        instrucciones_frame = ttk.Frame(main_frame)
        instrucciones_frame.pack(fill='x', pady=(10, 0))
        
        instrucciones_text = "💡 Instrucciones: Busca por nombre/apellidos arriba • Selecciona un usuario y haz clic en 'Imprimir Etiqueta' • O haz doble clic en una fila para imprimir directamente"
        instrucciones_label = ttk.Label(instrucciones_frame, text=instrucciones_text, 
                                       font=('Arial', 9), foreground='gray')
        instrucciones_label.pack()

    def obtener_usuarios_eventos_activos(self):
        """Obtiene todos los usuarios de los eventos activos (CSV o MySQL)."""
        if not EVENTOS_ACTIVOS:
            return []
        
        usuarios = []
        
        # Modo CSV: filtrar datos del CSV cargado
        if self.modo_csv and self.datos_csv is not None:
            try:
                print(f"📊 Obteniendo usuarios desde CSV para eventos: {EVENTOS_ACTIVOS}")
                
                # Filtrar usuarios por eventos activos
                for _, fila in self.datos_csv.iterrows():
                    evento_usuario = fila.get('Evento')
                    if evento_usuario:
                        try:
                            evento_id = int(evento_usuario)
                            if evento_id in EVENTOS_ACTIVOS:
                                # Convertir fila a diccionario con estructura MySQL
                                usuario = {
                                    'idUsuario': str(fila.get('idUsuario', '')).strip(),
                                    'Nombrecompleto': str(fila.get('Nombrecompleto', '')).strip(),
                                    'apellidos': str(fila.get('Apellidos', '')).strip(),  # Buscar Apellidos con mayúscula
                                    'Empresa': str(fila.get('Empresa', '')).strip(),
                                    'entrada': str(fila.get('Entrada', '')).strip(),  # Buscar Entrada con mayúscula
                                    'Evento': evento_id,
                                    'comida': int(fila.get('Comida', 0)) if pd.notna(fila.get('Comida')) else 0,
                                    'pirata': int(fila.get('Pirata', fila.get('pirata', 0))) if pd.notna(fila.get('Pirata', fila.get('pirata', 0))) else 0,  # Campo mochila
                                    'Dia': str(fila.get('Dia', '1')).strip(),
                                    'Pagado': int(fila.get('Pagado', 0)) if pd.notna(fila.get('Pagado')) else 0,
                                    'Pais': str(fila.get('Pais', '')).strip()
                                }
                                usuarios.append(usuario)
                        except (ValueError, TypeError):
                            continue  # Saltar filas con evento inválido
                
                # Ordenar por nombre como en MySQL
                usuarios.sort(key=lambda x: (x.get('Nombrecompleto', ''), x.get('apellidos', '')))
                print(f"✅ {len(usuarios)} usuarios obtenidos desde CSV")
                
            except Exception as e:
                print(f"❌ Error obteniendo usuarios desde CSV: {e}")
                messagebox.showerror('Error CSV', f'Error al obtener usuarios desde CSV:\n{str(e)}')
                
        # Modo MySQL: consulta a base de datos
        else:
            try:
                print(f"🌐 Obteniendo usuarios desde MySQL para eventos: {EVENTOS_ACTIVOS}")
                
                # Intentar con PyMySQL primero
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
                    
                    print(f"✅ {len(usuarios)} usuarios obtenidos desde MySQL con PyMySQL")
                    
                except ImportError:
                    print("📌 PyMySQL no disponible, usando mysql.connector...")
                    # Fallback con mysql.connector
                    import mysql.connector
                    conn = mysql.connector.connect(**DB_CONFIG)
                    cursor = conn.cursor(dictionary=True)
                    
                    placeholders = ','.join(['%s'] * len(EVENTOS_ACTIVOS))
                    query = f"SELECT * FROM asistentes WHERE Evento IN ({placeholders}) ORDER BY Nombrecompleto, apellidos"
                    
                    cursor.execute(query, EVENTOS_ACTIVOS)
                    usuarios = cursor.fetchall()
                    
                    cursor.close()
                    conn.close()
                    
                    print(f"✅ {len(usuarios)} usuarios obtenidos desde MySQL con mysql.connector")
                
            except Exception as e:
                print(f"❌ Error obteniendo usuarios desde MySQL: {e}")
                messagebox.showerror('Error MySQL', f'Error al obtener usuarios desde MySQL:\n{str(e)}')
        
        return usuarios

    def actualizar_tabla_usuarios_optimizada(self, tree):
        """Actualiza la tabla de usuarios con datos frescos (optimizado)."""
        try:
            # Limpiar tabla actual
            for item in tree.get_children():
                tree.delete(item)
            
            # Obtener eventos una sola vez
            if self.modo_csv:
                eventos = self.obtener_eventos_csv()
            else:
                eventos = self.obtener_eventos_seguro()
            eventos_dict = {e['id']: e for e in eventos}
            
            # Obtener datos actualizados
            usuarios = self.obtener_usuarios_eventos_activos()
            
            # Volver a insertar datos
            for usuario in usuarios:
                pulsera_texto = "✅ SÍ" if usuario.get('comida', 0) == 1 else "❌ NO"
                # Mochila: pirata = 1 (no mochila), pirata = 0 (sí mochila)
                mochila_texto = "❌ NO" if usuario.get('pirata', 0) == 1 else "✅ SÍ"
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
                    pulsera_texto,
                    mochila_texto
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
            
            # Generar versión para vista previa (con colores)
            self.img_etiqueta_preview = generar_etiqueta(datos, nombre_evento, version_impresion=False)
            # Generar versión para impresión (sin colores)
            self.img_etiqueta = generar_etiqueta(datos, nombre_evento, version_impresion=True)
            
            # IMPORTANTE: Asignar datos_actual ANTES de show_preview para que los indicadores funcionen correctamente
            self.datos_actual = datos
            self.show_preview(self.img_etiqueta_preview)  # Mostrar versión con colores
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
            
        # Validar que hay datos disponibles (eventos activos o CSV cargado)
        if not EVENTOS_ACTIVOS and not self.modo_csv:
            messagebox.showerror('Error', 'No hay eventos activos seleccionados ni datos CSV cargados.')
            self.entry.delete(0, 'end')
            self.focus_entry()
            return
            
        # Buscar usuario según el modo
        if self.modo_csv:
            datos = self.buscar_usuario_csv(id_asistente)
            if not datos:
                messagebox.showerror('Error', f'No se encontró el ID: {id_asistente} en el archivo CSV')
                log_acceso({'idUsuario': id_asistente}, False, "Usuario no encontrado en CSV")
                self.log_acceso_resultado({'idUsuario': id_asistente}, False, "Usuario no encontrado en CSV")
                self.entry.delete(0, 'end')
                self.focus_entry()
                return
            
            # Para CSV, la validación es más simple - si está en el CSV, está autorizado
            autorizado = True
            razon = "Usuario encontrado en archivo CSV"
            
        else:
            # Modo MySQL normal
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
        
        # Registrar acceso independientemente del modo
        log_acceso(datos, autorizado, razon)
        
        # Registrar en el log visual con colores
        self.log_acceso_resultado(datos, autorizado, razon)
        
        if not autorizado:
            if self.modo_csv:
                messagebox.showerror('Acceso Denegado', f"{razon}")
            else:
                messagebox.showerror('Acceso Denegado', f"{razon}\n\nEventos activos: {', '.join(map(str, EVENTOS_ACTIVOS))}")
            self.entry.delete(0, 'end')
            self.focus_entry()
            return
        
        # Debug: Mostrar información del usuario antes de validación
        print(f"🔍 DEBUG: Usuario autorizado - {datos.get('Nombrecompleto', 'Sin nombre')}")
        print(f"🔍 DEBUG: Campo comida = {datos.get('comida', 'No existe')} (tipo: {type(datos.get('comida', 'No existe'))})")
        
        # ✅ NUEVA VALIDACIÓN: Verificar si ya fue escaneado previamente
        comida_valor = datos.get('comida', 0)
        # Manejar tanto string como int
        if str(comida_valor).strip() == '1' or comida_valor == 1:
            nombre_usuario = datos.get('Nombrecompleto', 'Usuario desconocido')
            mensaje_log = f"QR ya escaneado previamente - {nombre_usuario} (comida={comida_valor})"
            
            # Registrar en logs
            self.log_message(mensaje_log, "WARNING")
            log_acceso(datos, False, "QR ya escaneado previamente")
            
            print(f"⚠️ VALIDACIÓN: Usuario {nombre_usuario} ya fue escaneado (comida={comida_valor})")
            
            # Mostrar popup con opción de reimprimir
            respuesta = messagebox.askyesno('QR Ya Escaneado', 
                f'⚠️ Este QR ya ha sido escaneado previamente.\n\n'
                f'Usuario: {nombre_usuario}\n'
                f'ID: {datos.get("idUsuario", "N/A")}\n\n'
                f'La pulsera ya fue entregada a este usuario.\n\n'
                f'¿Desea imprimir la etiqueta de nuevo?')
            
            if not respuesta:
                # Usuario eligió NO imprimir
                self.log_message("Usuario canceló reimpresión de QR ya escaneado", "INFO")
                self.entry.delete(0, 'end')
                self.focus_entry()
                return
            else:
                # Usuario eligió SÍ reimprimir - continuar con el proceso normal
                self.log_message("Usuario confirmó reimpresión de QR ya escaneado", "INFO")
            
        # Usuario autorizado - proceder con etiqueta
        self.log_message("Generando etiqueta...", "INFO")
        
        # Obtener nombre del evento
        if self.modo_csv:
            # Para CSV, obtener el nombre del evento desde el archivo de eventos CSV
            evento_id = datos.get('Evento', '0')
            nombre_evento = self.obtener_nombre_evento_csv(evento_id)
        else:
            # Para MySQL, obtener desde los eventos cargados
            evento_id = datos.get('Evento')
            eventos = self.obtener_eventos_seguro()
            nombre_evento = obtener_nombre_evento(evento_id, eventos)
        
        # Generar versión para vista previa (con colores)
        self.img_etiqueta_preview = generar_etiqueta(datos, nombre_evento, version_impresion=False)
        # Generar versión para impresión (sin colores)
        self.img_etiqueta = generar_etiqueta(datos, nombre_evento, version_impresion=True)
        
        # IMPORTANTE: Asignar datos_actual ANTES de show_preview para que los indicadores funcionen correctamente
        self.datos_actual = datos
        self.show_preview(self.img_etiqueta_preview)  # Mostrar versión con colores
        self.actualizar_info_status("✅ Etiqueta lista para imprimir")
        self.log_message("¡Etiqueta generada correctamente!", "SUCCESS")
        
        # Si está en modo automático, imprimir inmediatamente Y marcar comida
        if self.auto_mode.get():
            # Marcar comida automáticamente (tanto CSV como MySQL)
            id_usuario = datos.get('idUsuario') or datos.get('cedula')
            if marcar_comida(id_usuario, self):
                self.log_message(f"Comida registrada para usuario {id_usuario}", "SUCCESS")
            else:
                self.log_message(f"Error al registrar comida para usuario {id_usuario}", "ERROR")
            
            self.imprimir_y_log()
        else:
            self.btn_print['state'] = 'normal'
        self.entry.delete(0, 'end')
        self.focus_entry()

    def show_preview(self, img):
        # Mantener proporción 62×100 mm sin deformar - ETIQUETA MUCHO MÁS GRANDE
        target_w = 770  # Era 620, ahora 770 para ajustarse al container más grande
        ratio = target_w / img.width
        target_h = int(img.height * ratio)
        img_preview = img.resize((target_w, target_h), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img_preview)
        self.preview_lbl.configure(image=self.tk_img)
        
        # Actualizar indicadores de pulseras
        self.actualizar_indicadores_pulseras()

    def actualizar_indicadores_pulseras(self):
        """Actualiza los indicadores visuales de pulseras y mochilas según los datos actuales."""
        if not hasattr(self, 'datos_actual') or not self.datos_actual:
            # Ocultar indicadores activos si no hay datos
            self.indicador_activo.pack_forget()
            self.indicador_mochila_activo.pack_forget()
            # Ocultar el panel completo si no hay datos
            self.pulseras_container.pack_forget()
            return
        
        # Obtener datos
        tipo_entrada = self.datos_actual.get('Entrada') or self.datos_actual.get('entrada', '')
        pirata = self.datos_actual.get('pirata', 0)  # Campo mochila: 1=no mochila, 0=sí mochila
        
        # Obtener nombre del evento
        if self.modo_csv:
            evento_id = self.datos_actual.get('Evento', '0')
            nombre_evento = self.obtener_nombre_evento_csv(evento_id)
        else:
            evento_id = self.datos_actual.get('Evento', 0)
            nombre_evento = self.obtener_nombre_evento_mysql(evento_id)
        
        # Normalizar para comparación
        evento_lower = nombre_evento.lower() if nombre_evento else ''
        
        # ⭐ VERIFICAR SI ES UN EVENTO CON PULSERAS (SOLO LPN Y PORCIFORUM)
        es_evento_con_pulseras = ('lpn' in evento_lower or 
                                  'porciforum' in evento_lower or 
                                  'porci forum' in evento_lower)
        
        if not es_evento_con_pulseras:
            # ❌ EVENTO SIN PULSERAS: Ocultar todo el panel
            self.pulseras_container.pack_forget()
            print(f"ℹ️ Evento '{nombre_evento}' sin sistema de pulseras - Panel oculto")
            return
        
        # ✅ EVENTO CON PULSERAS: Mostrar el panel
        # Verificar si ya está visible, si no, mostrarlo
        if not self.pulseras_container.winfo_ismapped():
            self.pulseras_container.pack(side='left', fill='y', padx=(10, 0))
            print(f"✅ Evento '{nombre_evento}' con sistema de pulseras - Panel visible")
        
        # Continuar con la lógica normal de actualización de indicadores
        tipo_lower = tipo_entrada.lower() if tipo_entrada else ''
        
        print("=" * 80)
        print(f"🔍 DEBUG PULSERAS:")
        print(f"   - Usuario: {self.datos_actual.get('Nombrecompleto', 'N/A')}")
        print(f"   - Evento (original): '{nombre_evento}'")
        print(f"   - Evento (lower): '{evento_lower}'")
        print(f"   - Tipo entrada (original): '{tipo_entrada}'")
        print(f"   - Tipo entrada (lower): '{tipo_lower}'")
        
        # Resetear todos los indicadores de pulseras
        self.pulsera_naranja.configure(relief='raised', borderwidth=2)
        self.pulsera_azul.configure(relief='raised', borderwidth=2)
        self.pulsera_negra.configure(relief='raised', borderwidth=2)
        self.indicador_activo.pack_forget()
        
        # Resetear todos los indicadores de mochilas
        self.mochila_si.configure(relief='raised', borderwidth=2)
        self.mochila_no.configure(relief='raised', borderwidth=2)
        self.indicador_mochila_activo.pack_forget()
        
        # 🚨 LÓGICA COMPLETAMENTE NUEVA - REGLAS CORRECTAS 🚨
        # PRIORIDAD 1: EXPO → SIEMPRE PULSERA NEGRA Y NO MOCHILA
        # PRIORIDAD 2: PIRATA=1 → SIEMPRE PULSERA NEGRA Y NO MOCHILA  
        # PRIORIDAD 3: LPN Congress → PULSERA NARANJA + mochila según pirata
        # PRIORIDAD 4: PorciForum Congress → PULSERA AZUL + mochila según pirata
        
        pulsera_activa = None
        mochila_activa = None
        
        print(f"� ANÁLISIS COMPLETO:")
        print(f"   - Evento: '{nombre_evento}'")
        print(f"   - Tipo entrada: '{tipo_entrada}'")
        
        # Convertir pirata a entero de forma segura (maneja tanto int como float)
        try:
            if pirata is not None:
                # Convertir a float primero para manejar casos como 1.0, después a int
                pirata_valor = int(float(str(pirata).strip()))
            else:
                pirata_valor = 0
        except (ValueError, TypeError):
            pirata_valor = 0
            print(f"⚠️ Error convirtiendo pirata, usando 0: {pirata}")
        
        print(f"   - Pirata: {pirata_valor}")
        
        # PASO 1: ¿Es EXPO? → PULSERA NEGRA + NO MOCHILA
        if 'expo' in tipo_lower:
            # CUALQUIER EXPO → PULSERA NEGRA + NO MOCHILA
            print("🖤 REGLA EXPO: Pulsera NEGRA + NO mochila")
            # ACTIVAR PULSERA NEGRA
            pulsera_activa = self.pulsera_negra
            self.pulsera_negra.configure(relief='solid', borderwidth=4, bg='#2C2C2C')
            self.indicador_activo.configure(text="👆 PULSERA NEGRA (EXPO)", bg='#2C2C2C', fg='white')
            self.indicador_activo.pack(after=self.pulsera_negra, pady=(2, 0))
            
            # NO MOCHILA para EXPO
            mochila_activa = self.mochila_no
            self.mochila_no.configure(relief='solid', borderwidth=4)
            self.indicador_mochila_activo.configure(text="👆 NO ENTREGAR MOCHILA (EXPO)", bg='#2C2C2C', fg='white')
            
        # PASO 2: ¿Es PIRATA=1? → PULSERA NEGRA + NO MOCHILA  
        elif pirata_valor == 1:
            print("🖤 REGLA PIRATA: Pulsera NEGRA + NO mochila")
            # ACTIVAR PULSERA NEGRA
            pulsera_activa = self.pulsera_negra
            self.pulsera_negra.configure(relief='solid', borderwidth=4, bg='#2C2C2C')
            self.indicador_activo.configure(text="👆 PULSERA NEGRA (PIRATA)", bg='#2C2C2C', fg='white')
            self.indicador_activo.pack(after=self.pulsera_negra, pady=(2, 0))
            
            # NO MOCHILA para PIRATA
            mochila_activa = self.mochila_no
            self.mochila_no.configure(relief='solid', borderwidth=4)
            self.indicador_mochila_activo.configure(text="👆 NO ENTREGAR MOCHILA (PIRATA)", bg='#2C2C2C', fg='white')
            
        # PASO 3: LPN Congress → PULSERA NARANJA + mochila según pirata
        elif 'lpn' in evento_lower and 'congress' in tipo_lower:
            print("🟠 REGLA LPN CONGRESS: Pulsera NARANJA + mochila según pirata")
            pulsera_activa = self.pulsera_naranja
            self.pulsera_naranja.configure(relief='solid', borderwidth=4)
            self.indicador_activo.pack(after=self.pulsera_naranja, pady=(2, 0))
            
            # Mochila según pirata para LPN Congress
            if pirata_valor == 0:
                mochila_activa = self.mochila_si
                self.mochila_si.configure(relief='solid', borderwidth=4)
                self.indicador_mochila_activo.configure(text="👆 ENTREGAR MOCHILA", bg='#28a745', fg='white')
            else:
                mochila_activa = self.mochila_no
                self.mochila_no.configure(relief='solid', borderwidth=4)
                self.indicador_mochila_activo.configure(text="� NO ENTREGAR MOCHILA", bg='#dc3545', fg='white')
                
        # PASO 4: PorciForum → PULSERA AZUL (Congress) o NEGRA (Expo) + mochila según pirata
        elif any(x in evento_lower for x in ['porciforum', 'porci forum']):
            if 'expo' in tipo_lower:
                # PorciForum EXPO → PULSERA NEGRA + NO MOCHILA
                print("🖤 REGLA PORCIFORUM EXPO: Pulsera NEGRA + NO mochila")
                pulsera_activa = self.pulsera_negra
                self.pulsera_negra.configure(relief='solid', borderwidth=4, bg='#2C2C2C')
                self.indicador_activo.configure(text="👆 PULSERA NEGRA (EXPO)", bg='#2C2C2C', fg='white')
                self.indicador_activo.pack(after=self.pulsera_negra, pady=(2, 0))
                
                # NO MOCHILA para EXPO
                mochila_activa = self.mochila_no
                self.mochila_no.configure(relief='solid', borderwidth=4)
                self.indicador_mochila_activo.configure(text="👆 NO ENTREGAR MOCHILA (EXPO)", bg='#2C2C2C', fg='white')
            else:
                # PorciForum Congress → PULSERA AZUL + mochila según pirata
                print("🔵 REGLA PORCIFORUM CONGRESS: Pulsera AZUL + mochila según pirata")
                pulsera_activa = self.pulsera_azul
                self.pulsera_azul.configure(relief='solid', borderwidth=4)
                self.indicador_activo.pack(after=self.pulsera_azul, pady=(2, 0))
                
                # Mochila según pirata para PorciForum Congress
                if pirata_valor == 0:
                    mochila_activa = self.mochila_si
                    self.mochila_si.configure(relief='solid', borderwidth=4)
                    self.indicador_mochila_activo.configure(text="👆 ENTREGAR MOCHILA", bg='#28a745', fg='white')
                else:
                    mochila_activa = self.mochila_no
                    self.mochila_no.configure(relief='solid', borderwidth=4)
                    self.indicador_mochila_activo.configure(text="👆 NO ENTREGAR MOCHILA", bg='#dc3545', fg='white')
                
        else:
            print("⚠️ CASO NO RECONOCIDO - usando defaults")
            # Caso por defecto
            if pirata_valor == 0:
                mochila_activa = self.mochila_si
                self.mochila_si.configure(relief='solid', borderwidth=4)
                self.indicador_mochila_activo.configure(text="👆 ENTREGAR MOCHILA (DEFAULT)", bg='#ffc107', fg='black')
            else:
                mochila_activa = self.mochila_no  
                self.mochila_no.configure(relief='solid', borderwidth=4)
                self.indicador_mochila_activo.configure(text="👆 NO ENTREGAR MOCHILA (DEFAULT)", bg='#ffc107', fg='black')
        
        # Mostrar indicador de mochila
        if mochila_activa:
            self.indicador_mochila_activo.pack(after=mochila_activa, pady=(2, 0))
        
        print(f"🎯 RESULTADO FINAL:")
        print(f"   - Pulsera activa: {pulsera_activa}")
        print(f"   - Mochila activa: {mochila_activa}")

    def seleccionar_impresora(self):
        """Permite seleccionar manualmente la impresora Brother a usar."""
        try:
            import win32print
            
            # Actualizar lista de impresoras disponibles
            print("🔄 Escaneando impresoras disponibles...")
            impresoras_brother = []
            
            try:
                # Usar flag 6 para forzar actualización completa
                for printer_info in win32print.EnumPrinters(6):
                    nombre = printer_info[2]
                    if 'Brother' in nombre and ('QL-600' in nombre or 'QL-700' in nombre or 'QL-800' in nombre):
                        impresoras_brother.append(nombre)
            except:
                # Fallback
                for printer_info in win32print.EnumPrinters(2):
                    nombre = printer_info[2]
                    if 'Brother' in nombre and ('QL-600' in nombre or 'QL-700' in nombre or 'QL-800' in nombre):
                        impresoras_brother.append(nombre)
            
            if not impresoras_brother:
                messagebox.showwarning("Sin impresoras", 
                    "No se encontraron impresoras Brother QL instaladas.\n\n"
                    "Asegúrate de que el driver de la impresora esté instalado correctamente.")
                return
            
            # Crear ventana de selección
            ventana = tk.Toplevel(self)
            ventana.title("🖨️ Seleccionar Impresora Brother QL")
            ventana.geometry("500x400")
            ventana.transient(self)
            ventana.grab_set()
            
            # Centrar ventana
            ventana.geometry("+%d+%d" % (self.winfo_rootx() + 100, self.winfo_rooty() + 100))
            
            # Frame principal
            main_frame = ttk.Frame(ventana, padding=20)
            main_frame.pack(fill='both', expand=True)
            
            # Título
            titulo = ttk.Label(main_frame,
                              text="🖨️ Seleccione la impresora a usar",
                              font=('Segoe UI', 14, 'bold'))
            titulo.pack(pady=(0, 20))
            
            # Info
            info_text = f"Se encontraron {len(impresoras_brother)} impresora(s) Brother QL:\n"
            info_label = ttk.Label(main_frame, text=info_text, font=('Segoe UI', 10))
            info_label.pack(pady=(0, 10))
            
            # Lista de impresoras con radio buttons
            seleccion_var = tk.StringVar()
            
            # Marcar la impresora actual si existe
            if hasattr(self, 'impresora_seleccionada') and self.impresora_seleccionada:
                seleccion_var.set(self.impresora_seleccionada)
            else:
                # Por defecto, seleccionar la primera
                seleccion_var.set(impresoras_brother[0])
            
            # Frame con scroll para la lista
            lista_frame = ttk.LabelFrame(main_frame, text="Impresoras disponibles", padding=10)
            lista_frame.pack(fill='both', expand=True, pady=(0, 15))
            
            for impresora in impresoras_brother:
                # Verificar si es la predeterminada del sistema
                es_predeterminada = False
                try:
                    if impresora == win32print.GetDefaultPrinter():
                        es_predeterminada = True
                except:
                    pass
                
                texto = impresora
                if es_predeterminada:
                    texto += " ⭐ (Predeterminada del sistema)"
                
                radio = ttk.Radiobutton(lista_frame, 
                                       text=texto, 
                                       variable=seleccion_var, 
                                       value=impresora)
                radio.pack(anchor='w', pady=5)
            
            # Botones
            botones_frame = ttk.Frame(main_frame)
            botones_frame.pack(fill='x')
            
            def confirmar():
                self.impresora_seleccionada = seleccion_var.get()
                print(f"✅ Impresora seleccionada: {self.impresora_seleccionada}")
                self.log_message(f"Impresora cambiada a: {self.impresora_seleccionada}", "SUCCESS")
                messagebox.showinfo("Impresora Actualizada", 
                    f"✅ Impresora configurada correctamente:\n\n{self.impresora_seleccionada}\n\n"
                    "Las próximas etiquetas se imprimirán en esta impresora.")
                ventana.destroy()
            
            def refrescar():
                # Cerrar y volver a abrir para refrescar la lista
                ventana.destroy()
                self.seleccionar_impresora()
            
            ttk.Button(botones_frame, text="🔄 Refrescar Lista", command=refrescar).pack(side='left', padx=(0, 10))
            ttk.Button(botones_frame, text="✅ Confirmar", command=confirmar).pack(side='left', padx=(0, 10))
            ttk.Button(botones_frame, text="❌ Cancelar", command=ventana.destroy).pack(side='left')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al listar impresoras:\n{str(e)}")

    def on_print(self):
        self.imprimir_y_log()
        self.btn_print['state'] = 'disabled'

    def imprimir_y_log(self):
        # Marcar comida en la base de datos o CSV si estamos en modo manual
        if not self.auto_mode.get() and hasattr(self, 'datos_actual') and self.datos_actual:
            id_usuario = self.datos_actual.get('idUsuario')
            if marcar_comida(id_usuario, self):
                self.log_message(f"Comida registrada para usuario {id_usuario}", "SUCCESS")
            else:
                self.log_message(f"Error al registrar comida para usuario {id_usuario}", "ERROR")
        
        imprimir_etiqueta(self.img_etiqueta, sistema=self)
        log_impresion(self.datos_actual)
        self.add_log(self.datos_actual)

    def filtrar_tabla_usuarios(self, texto_busqueda, tree, usuarios, eventos_dict):
        """Filtra la tabla de usuarios según el texto de búsqueda."""
        # Limpiar tabla actual
        for item in tree.get_children():
            tree.delete(item)
        
        # Filtrar usuarios
        texto_busqueda = texto_busqueda.lower().strip()
        usuarios_filtrados = []
        
        if not texto_busqueda:
            # Si no hay texto de búsqueda, mostrar todos
            usuarios_filtrados = usuarios
        else:
            # Buscar en nombre y apellidos
            for usuario in usuarios:
                nombre = str(usuario.get('Nombrecompleto', '')).lower()
                apellidos = str(usuario.get('apellidos', '')).lower()
                
                if (texto_busqueda in nombre or 
                    texto_busqueda in apellidos or
                    texto_busqueda in f"{nombre} {apellidos}"):
                    usuarios_filtrados.append(usuario)
        
        # Insertar usuarios filtrados
        for usuario in usuarios_filtrados:
            pulsera_texto = "✅ SÍ" if usuario.get('comida', 0) == 1 else "❌ NO"
            mochila_texto = "❌ NO" if usuario.get('pirata', 0) == 1 else "✅ SÍ"
            evento_id = usuario.get('Evento', '')
            
            # Obtener nombre del evento
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
                pulsera_texto,
                mochila_texto
            ))
        
        print(f"🔍 Búsqueda '{texto_busqueda}': {len(usuarios_filtrados)} de {len(usuarios)} usuarios")

    def limpiar_busqueda_tabla(self, search_var, tree, usuarios, eventos_dict):
        """Limpia el campo de búsqueda y restaura todos los usuarios."""
        search_var.set("")
        self.filtrar_tabla_usuarios("", tree, usuarios, eventos_dict)

    def imprimir_etiqueta_seleccionada(self, tree):
        """Imprime la etiqueta del usuario seleccionado en la tabla."""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning('Sin selección', 
                'Por favor selecciona un usuario de la tabla para imprimir su etiqueta.')
            return
        
        # Obtener ID del usuario seleccionado
        item = tree.item(selection[0])
        id_usuario = item['values'][0]
        
        if not id_usuario:
            messagebox.showerror('Error', 'No se pudo obtener el ID del usuario seleccionado.')
            return
        
        self.imprimir_etiqueta_desde_tabla(id_usuario)

    def imprimir_etiqueta_desde_tabla(self, id_usuario):
        """Imprime la etiqueta de un usuario específico desde la tabla."""
        try:
            print(f"🖨️ Imprimiendo etiqueta para usuario ID: {id_usuario}")
            
            # Buscar usuario según el modo actual
            if self.modo_csv:
                usuario = self.buscar_usuario_csv(str(id_usuario))
            else:
                usuario = buscar_asistente(str(id_usuario))  # Usar función global para MySQL
            
            if not usuario:
                messagebox.showerror('Usuario no encontrado', 
                    f'No se encontró el usuario con ID {id_usuario}.')
                return
            
            # Generar etiqueta
            self.datos_actual = usuario
            
            # Obtener nombre del evento usando la misma lógica que el programa principal
            evento_id = usuario.get('Evento', '')
            eventos = self.obtener_eventos_seguro()
            nombre_evento = obtener_nombre_evento(evento_id, eventos)
            
            print(f"📅 Evento: {evento_id} - {nombre_evento}")
            
            # Generar etiquetas usando la función global
            self.img_etiqueta_preview = generar_etiqueta(usuario, nombre_evento, version_impresion=False)
            self.img_etiqueta = generar_etiqueta(usuario, nombre_evento, version_impresion=True)
            
            # Marcar comida como entregada
            if self.modo_csv:
                self.marcar_comida_csv(id_usuario)
            else:
                # Importar función de MySQL si está disponible
                try:
                    # Intentar marcar comida en MySQL usando función existente
                    if hasattr(self, 'marcar_comida_mysql'):
                        self.marcar_comida_mysql(id_usuario)
                    else:
                        print("⚠️ Función marcar_comida_mysql no disponible")
                except Exception as e:
                    print(f"⚠️ Error al marcar comida en MySQL: {e}")
            
            # Imprimir etiqueta
            imprimir_etiqueta(self.img_etiqueta, sistema=self)
            
            # Intentar guardar log con manejo de errores
            try:
                log_impresion(self.datos_actual)
                self.add_log(self.datos_actual)
            except Exception as log_error:
                print(f"⚠️ Error al guardar log: {log_error}")
                # La impresión se realizó exitosamente, solo el log falló
            
            messagebox.showinfo('Éxito', 
                f'Etiqueta impresa correctamente para {usuario.get("Nombrecompleto", "Usuario desconocido")}')
            
        except Exception as e:
            error_msg = f"Error al imprimir etiqueta: {str(e)}"
            print(f"❌ {error_msg}")
            # Si el error es solo de log, mostrar mensaje diferente
            if "permission denied" in str(e).lower() and "log" in str(e).lower():
                messagebox.showwarning('Impresión realizada', 
                    f'Etiqueta impresa correctamente para {usuario.get("Nombrecompleto", "Usuario desconocido")}.\n\n'
                    'Nota: No se pudo guardar el registro debido a permisos de archivo. '
                    'Cierra Excel u otros programas que puedan tener abierto el archivo de log.')
            else:
                messagebox.showerror('Error de impresión', error_msg)

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

    def actualizar_titulo_ventana(self):
        """Actualiza el título de la ventana principal según el modo activo."""
        base_titulo = "🏢 Sistema Profesional de Etiquetas QR - v2.0"
        
        if self.modo_csv:
            if self.eventos_cargados:
                num_eventos = len(self.eventos_cargados)
                total_registros = len(self.datos_csv) if hasattr(self, 'datos_csv') and self.datos_csv is not None else 0
                modo_info = f" • OFFLINE ({num_eventos} evento(s), {total_registros} registros)"
            else:
                modo_info = " • OFFLINE (CSV)"
        else:
            modo_info = " • ONLINE (MySQL)"
        
        self.title(base_titulo + modo_info)

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
