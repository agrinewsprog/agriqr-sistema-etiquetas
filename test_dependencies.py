#!/usr/bin/env python3
"""
Prueba de verificación de PIL ImageTk para PyInstaller
Este script se usa para verificar que PyInstaller incluye correctamente PIL ImageTk
"""

def verificar_pil_imagetk():
    """Verifica que PIL ImageTk esté disponible"""
    try:
        print("🔍 Verificando PIL...")
        from PIL import Image
        print("✅ PIL.Image importado correctamente")
        
        from PIL import ImageTk
        print("✅ PIL.ImageTk importado correctamente")
        
        from PIL import ImageDraw
        print("✅ PIL.ImageDraw importado correctamente")
        
        from PIL import ImageFont
        print("✅ PIL.ImageFont importado correctamente")
        
        # Verificar tkinter
        print("🔍 Verificando tkinter...")
        import tkinter as tk
        print("✅ tkinter importado correctamente")
        
        # Verificar MySQL
        print("🔍 Verificando MySQL...")
        import mysql.connector
        print("✅ mysql.connector importado correctamente")
        
        import pymysql
        print("✅ pymysql importado correctamente")
        
        # Verificar QR
        print("🔍 Verificando QR...")
        import qrcode
        print("✅ qrcode importado correctamente")
        
        # Verificar Brother QL (opcional)
        try:
            import brother_ql
            print("✅ brother_ql importado correctamente")
        except ImportError:
            print("⚠️ brother_ql no disponible (opcional)")
        
        print("🎉 ¡Todas las verificaciones pasaron!")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Verificación de dependencias para AgriQR")
    print("=" * 50)
    
    if verificar_pil_imagetk():
        print("\n✅ El sistema está listo para ejecutar AgriQR")
        exit(0)
    else:
        print("\n❌ Hay problemas con las dependencias")
        exit(1)