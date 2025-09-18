#!/usr/bin/env python3"""

"""Script para configurar automáticamente impresoras Brother QL-600/700/800

🖨️ CONFIGURADOR DE IMPRESORAS BROTHER QLSe ejecuta una sola vez durante la instalación del programa

🏢 Sistema AgriQR - Agrinews"""

import winreg

Utilidad para configurar automáticamente impresoras Brother QLimport win32print

Compatible con QL-600, QL-700, QL-800, QL-810W, QL-820NWBimport os

"""import sys

import subprocess

import os

import sysdef es_administrador():

import platform    """Verifica si el script se está ejecutando como administrador"""

import subprocess    try:

import json        return os.getuid() == 0

from datetime import datetime    except AttributeError:

        # Windows

# Configuración de impresoras Brother QL soportadas        try:

BROTHER_QL_MODELS = {            return os.access('C:\\Windows\\System32', os.W_OK)

    'QL-600': {        except:

        'name': 'Brother QL-600',            return False

        'driver_file': 'QL600_Driver.exe',

        'paper_sizes': ['62mm', '29mm x 90mm', '38mm x 90mm', '17mm x 54mm'],def ejecutar_como_admin():

        'connection': ['USB'],    """Re-ejecuta el script como administrador"""

        'max_width': 62    try:

    },        if sys.argv[-1] != 'asadmin':

    'QL-700': {            script = os.path.abspath(sys.argv[0])

        'name': 'Brother QL-700',            params = ' '.join([script] + sys.argv[1:] + ['asadmin'])

        'driver_file': 'QL700_Driver.exe',             subprocess.run(['powershell.exe', '-Command', f'Start-Process python -ArgumentList "{params}" -Verb RunAs'], check=True)

        'paper_sizes': ['62mm', '29mm x 90mm', '38mm x 90mm', '17mm x 54mm'],            return True

        'connection': ['USB'],    except Exception as e:

        'max_width': 62        print(f"No se pudo ejecutar como administrador: {e}")

    },        return False

    'QL-800': {    return False

        'name': 'Brother QL-800',

        'driver_file': 'QL800_Driver.exe',def configurar_brother_registro():

        'paper_sizes': ['62mm', '29mm x 90mm', '38mm x 90mm', '17mm x 54mm'],    """Configura la impresora Brother via registro (requiere admin)"""

        'connection': ['USB'],    try:

        'max_width': 62        # Buscar impresoras Brother

    },        impresoras_brother = []

    'QL-810W': {        for printer_info in win32print.EnumPrinters(2):

        'name': 'Brother QL-810W',            nombre = printer_info[2]

        'driver_file': None,  # Requiere descarga desde Brother            if 'Brother' in nombre and ('QL-600' in nombre or 'QL-700' in nombre or 'QL-800' in nombre):

        'paper_sizes': ['62mm', '29mm x 90mm', '38mm x 90mm', '17mm x 54mm'],                impresoras_brother.append(nombre)

        'connection': ['USB', 'WiFi'],        

        'max_width': 62        if not impresoras_brother:

    },            print("❌ No se encontraron impresoras Brother QL instaladas")

    'QL-820NWB': {            return False

        'name': 'Brother QL-820NWB',        

        'driver_file': None,  # Requiere descarga desde Brother        for nombre_impresora in impresoras_brother:

        'paper_sizes': ['62mm', '29mm x 90mm', '38mm x 90mm', '17mm x 54mm'],            print(f"Configurando: {nombre_impresora}")

        'connection': ['USB', 'WiFi', 'Bluetooth'],            

        'max_width': 62            try:

    }                # Configurar en registro de Windows

}                reg_path = f"SYSTEM\\CurrentControlSet\\Control\\Print\\Printers\\{nombre_impresora}\\PrinterDriverData"

                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE)

def log_message(message, level="INFO"):                

    """Registra un mensaje con timestamp"""                # Configuraciones para etiquetas 62x100mm

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")                winreg.SetValueEx(key, "PaperSize", 0, winreg.REG_DWORD, 256)    # Personalizado

    print(f"[{timestamp}] [{level}] {message}")                winreg.SetValueEx(key, "PaperWidth", 0, winreg.REG_DWORD, 620)   # 62mm

                winreg.SetValueEx(key, "PaperLength", 0, winreg.REG_DWORD, 1000) # 100mm

def detectar_sistema():                winreg.SetValueEx(key, "Orientation", 0, winreg.REG_DWORD, 1)    # Vertical

    """Detecta el sistema operativo y su versión"""                

    sistema = platform.system()                winreg.CloseKey(key)

    version = platform.release()                print(f"✅ {nombre_impresora} configurada correctamente (62x100mm)")

    arquitectura = platform.machine()                

                except Exception as e:

    log_message(f"Sistema detectado: {sistema} {version} ({arquitectura})")                print(f"Error configurando {nombre_impresora}: {e}")

    return sistema, version, arquitectura                continue

        

def detectar_impresoras_instaladas():        return True

    """Detecta impresoras Brother QL ya instaladas en el sistema"""        

    sistema, _, _ = detectar_sistema()    except Exception as e:

    impresoras_encontradas = []        print(f"Error general: {e}")

            return False

    if sistema == "Windows":

        try:def crear_archivo_configuracion():

            # Usar wmic para listar impresoras    """Crea archivos de configuración como respaldo"""

            resultado = subprocess.run(    try:

                ['wmic', 'printer', 'get', 'name'],        # Crear configuración en directorio del programa

                capture_output=True,        config_content = """

                text=True,# Configuración automática Brother QL

                check=True# Este archivo se crea para recordar la configuración aplicada

            )

            [Configuracion]

            lineas = resultado.stdout.split('\n')PaperSize=62x100mm

            for linea in lineas:PaperWidth=62

                linea = linea.strip()PaperLength=100

                if 'Brother' in linea and 'QL' in linea:Orientation=Portrait

                    impresoras_encontradas.append(linea)Configured=True

                    log_message(f"Impresora encontrada: {linea}")"""

                            

        except subprocess.CalledProcessError as e:        with open('brother_config.txt', 'w') as f:

            log_message(f"Error detectando impresoras: {e}", "ERROR")            f.write(config_content)

            

    elif sistema == "Darwin":  # macOS        print("✅ Archivo de configuración creado")

        try:        return True

            # Usar lpstat para listar impresoras        

            resultado = subprocess.run(    except Exception as e:

                ['lpstat', '-p'],        print(f"Error creando archivo config: {e}")

                capture_output=True,        return False

                text=True,

                check=Truedef main():

            )    print("=== CONFIGURADOR AUTOMÁTICO BROTHER QL ===")

                print("Configurando impresoras Brother QL-600/700/800...")

            lineas = resultado.stdout.split('\n')    

            for linea in lineas:    # Si no es admin, intentar ejecutar como admin

                if 'Brother' in linea and 'QL' in linea:    if not es_administrador() and 'asadmin' not in sys.argv:

                    impresoras_encontradas.append(linea.split()[-1])        print("Solicitando permisos de administrador...")

                    log_message(f"Impresora encontrada: {linea}")        if ejecutar_como_admin():

                                return

        except subprocess.CalledProcessError as e:    

            log_message(f"Error detectando impresoras en macOS: {e}", "ERROR")    # Configurar impresoras

        exito_registro = configurar_brother_registro()

    elif sistema == "Linux":    exito_archivo = crear_archivo_configuracion()

        try:    

            # Usar lpstat para listar impresoras    if exito_registro:

            resultado = subprocess.run(        print("\n🎉 ¡CONFIGURACIÓN COMPLETADA!")

                ['lpstat', '-p'],        print("Las impresoras Brother están configuradas para etiquetas 62x100mm")

                capture_output=True,    elif exito_archivo:

                text=True,        print("\n⚠️  Configuración parcial aplicada")

                check=True        print("Se creó archivo de respaldo")

            )    else:

                    print("\n❌ No se pudo aplicar la configuración automática")

            lineas = resultado.stdout.split('\n')        print("Será necesario configurar manualmente el tamaño 62x100mm")

            for linea in lineas:    

                if 'Brother' in linea and 'QL' in linea:    input("\nPresiona Enter para continuar...")

                    impresoras_encontradas.append(linea.split()[-1])

                    log_message(f"Impresora encontrada: {linea}")if __name__ == "__main__":

                        main()

        except subprocess.CalledProcessError as e:
            log_message(f"Error detectando impresoras en Linux: {e}", "ERROR")
    
    return impresoras_encontradas

def verificar_drivers_brother():
    """Verifica si los drivers Brother están disponibles"""
    sistema, _, _ = detectar_sistema()
    drivers_disponibles = []
    
    if sistema == "Windows":
        # Verificar archivos de driver en el directorio actual
        for modelo, config in BROTHER_QL_MODELS.items():
            driver_file = config.get('driver_file')
            if driver_file and os.path.exists(driver_file):
                drivers_disponibles.append(modelo)
                log_message(f"Driver disponible: {driver_file}")
    
    return drivers_disponibles

def instalar_driver_windows(modelo):
    """Instala driver Brother QL en Windows"""
    if modelo not in BROTHER_QL_MODELS:
        log_message(f"Modelo no soportado: {modelo}", "ERROR")
        return False
    
    config = BROTHER_QL_MODELS[modelo]
    driver_file = config.get('driver_file')
    
    if not driver_file:
        log_message(f"No hay driver local para {modelo}. Descargar desde Brother.com", "WARNING")
        return False
    
    if not os.path.exists(driver_file):
        log_message(f"Archivo de driver no encontrado: {driver_file}", "ERROR")
        return False
    
    try:
        log_message(f"Instalando driver para {modelo}...")
        
        # Ejecutar instalador silencioso
        resultado = subprocess.run(
            [driver_file, '/VERYSILENT', '/NORESTART'],
            check=True,
            capture_output=True,
            text=True
        )
        
        log_message(f"Driver {modelo} instalado exitosamente")
        return True
        
    except subprocess.CalledProcessError as e:
        log_message(f"Error instalando driver {modelo}: {e}", "ERROR")
        return False

def configurar_impresora_predeterminada(nombre_impresora):
    """Configura una impresora Brother QL como predeterminada"""
    sistema, _, _ = detectar_sistema()
    
    if sistema == "Windows":
        try:
            # Usar rundll32 para configurar impresora predeterminada
            subprocess.run([
                'rundll32',
                'printui.dll,PrintUIEntry',
                '/y',
                f'/n"{nombre_impresora}"'
            ], check=True)
            
            log_message(f"Impresora configurada como predeterminada: {nombre_impresora}")
            return True
            
        except subprocess.CalledProcessError as e:
            log_message(f"Error configurando impresora predeterminada: {e}", "ERROR")
            return False
    
    return False

def crear_configuracion_brother_ql():
    """Crea archivo de configuración para brother_ql"""
    config = {
        'default_printer': 'QL-700',
        'default_label': '62',
        'backend': 'pyusb',
        'compression': True,
        'rotation': 0
    }
    
    try:
        with open('brother_config.txt', 'w') as f:
            json.dump(config, f, indent=2)
        
        log_message("Archivo de configuración brother_ql creado")
        return True
        
    except Exception as e:
        log_message(f"Error creando configuración: {e}", "ERROR")
        return False

def generar_script_test():
    """Genera script de prueba para verificar impresión"""
    script_test = '''#!/usr/bin/env python3
"""
Script de prueba para impresoras Brother QL
Genera una etiqueta de prueba simple
"""

import sys
import os

# Añadir directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import SistemaEtiquetasProfesional
    import tkinter as tk
    
    print("🧪 Iniciando prueba de impresión Brother QL...")
    
    # Crear instancia de la aplicación
    root = tk.Tk()
    app = SistemaEtiquetasProfesional(root)
    
    # Simular datos de prueba
    app.cedula_var.set("12345678")
    app.nombre_var.set("USUARIO DE PRUEBA")
    app.empresa_var.set("AGRINEWS TEST")
    
    print("✅ Configuración de prueba lista")
    print("🖨️ Presiona 'Imprimir Etiqueta' para probar la impresora")
    
    root.mainloop()
    
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("📁 Asegúrate de estar en el directorio correcto")
    
except Exception as e:
    print(f"❌ Error durante la prueba: {e}")
'''
    
    try:
        with open('test_impresora.py', 'w', encoding='utf-8') as f:
            f.write(script_test)
        
        log_message("Script de prueba generado: test_impresora.py")
        return True
        
    except Exception as e:
        log_message(f"Error generando script de prueba: {e}", "ERROR")
        return False

def main():
    """Función principal del configurador"""
    print("=" * 60)
    print("🖨️  CONFIGURADOR DE IMPRESORAS BROTHER QL")
    print("🏢 Sistema AgriQR - Agrinews")
    print("=" * 60)
    
    # Detectar sistema
    sistema, version, arch = detectar_sistema()
    
    if sistema == "Windows":
        log_message("Iniciando configuración para Windows...")
        
        # Detectar impresoras instaladas
        impresoras = detectar_impresoras_instaladas()
        
        if impresoras:
            log_message("Impresoras Brother QL encontradas:")
            for impresora in impresoras:
                print(f"  • {impresora}")
        else:
            log_message("No se encontraron impresoras Brother QL instaladas")
            
            # Verificar drivers disponibles
            drivers = verificar_drivers_brother()
            
            if drivers:
                log_message("Drivers disponibles para instalación:")
                for driver in drivers:
                    print(f"  • {driver}")
                
                # Preguntar si instalar drivers
                respuesta = input("\n¿Instalar drivers automáticamente? (s/N): ").strip().lower()
                
                if respuesta in ['s', 'si', 'y', 'yes']:
                    for modelo in drivers:
                        if instalar_driver_windows(modelo):
                            log_message(f"✅ Driver {modelo} instalado")
                        else:
                            log_message(f"❌ Error instalando driver {modelo}")
            else:
                log_message("No hay drivers locales disponibles")
                log_message("Descargar drivers desde: https://www.brother.com/")
    
    elif sistema in ["Darwin", "Linux"]:
        log_message(f"Configuración para {sistema}...")
        log_message("Para impresión Brother QL instalar: pip install brother_ql")
        
        # Verificar si brother_ql está instalado
        try:
            import brother_ql
            log_message("✅ brother_ql ya está instalado")
        except ImportError:
            log_message("❌ brother_ql no está instalado")
            log_message("🔧 Instalar con: pip install brother_ql")
    
    # Crear configuración
    crear_configuracion_brother_ql()
    
    # Generar script de prueba
    generar_script_test()
    
    # Detectar impresoras finales
    impresoras_finales = detectar_impresoras_instaladas()
    
    if impresoras_finales:
        log_message("\n🎉 Configuración completada!")
        log_message("Impresoras configuradas:")
        for impresora in impresoras_finales:
            print(f"  ✅ {impresora}")
        
        log_message("\n📋 Próximos pasos:")
        print("  1. Ejecutar test_impresora.py para probar")
        print("  2. Verificar etiquetas en la aplicación principal")
        print("  3. Configurar tamaño de papel en las preferencias de impresora")
        
    else:
        log_message("\n⚠️  No se detectaron impresoras Brother QL")
        log_message("📋 Verificar:")
        print("  1. Impresora conectada y encendida")
        print("  2. Drivers instalados correctamente")
        print("  3. Cable USB funcionando")
    
    print("\n" + "=" * 60)
    log_message("Configuración finalizada")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_message("\nConfiguración cancelada por el usuario")
    except Exception as e:
        log_message(f"Error inesperado: {e}", "ERROR")
        sys.exit(1)