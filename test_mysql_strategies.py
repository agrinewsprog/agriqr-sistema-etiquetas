#!/usr/bin/env python3
"""
Script de prueba para verificar las estrategias de conexión MySQL
"""

import sys
import traceback

# Configuración de la base de datos
DB_CONFIG_EVENTOS = {
    'host': '148.113.211.234',
    'user': 'agribusi_acr3D1t',
    'password': 'tTe}1*d$Kz*R',
    'database': 'agribusi_3MpR3s4'
}

def test_mysql_connector():
    """Prueba mysql.connector básico"""
    print("🔍 Probando mysql.connector básico...")
    try:
        import mysql.connector
        
        config = {
            'host': DB_CONFIG_EVENTOS['host'],
            'user': DB_CONFIG_EVENTOS['user'],
            'password': DB_CONFIG_EVENTOS['password'],
            'database': DB_CONFIG_EVENTOS['database'],
            'connect_timeout': 5,
            'autocommit': True
        }
        
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Eventos")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"✅ mysql.connector: {count} eventos encontrados")
        return True
        
    except Exception as e:
        print(f"❌ mysql.connector falló: {e}")
        traceback.print_exc()
        return False

def test_mysql_connector_simple():
    """Prueba mysql.connector ultra simple"""
    print("\n🔍 Probando mysql.connector simple...")
    try:
        import mysql.connector
        
        conn = mysql.connector.connect(
            host=DB_CONFIG_EVENTOS['host'],
            user=DB_CONFIG_EVENTOS['user'],
            password=DB_CONFIG_EVENTOS['password'],
            database=DB_CONFIG_EVENTOS['database']
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Eventos")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"✅ mysql.connector simple: {count} eventos encontrados")
        return True
        
    except Exception as e:
        print(f"❌ mysql.connector simple falló: {e}")
        return False

def test_pymysql():
    """Prueba PyMySQL"""
    print("\n🔍 Probando PyMySQL...")
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
        cursor.execute("SELECT COUNT(*) FROM Eventos")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"✅ PyMySQL: {count} eventos encontrados")
        return True
        
    except Exception as e:
        print(f"❌ PyMySQL falló: {e}")
        return False

def test_mysql_connector_latin1():
    """Prueba mysql.connector con charset latin1"""
    print("\n🔍 Probando mysql.connector con charset latin1...")
    try:
        import mysql.connector
        
        conn = mysql.connector.connect(
            host=DB_CONFIG_EVENTOS['host'],
            user=DB_CONFIG_EVENTOS['user'],
            password=DB_CONFIG_EVENTOS['password'],
            database=DB_CONFIG_EVENTOS['database'],
            charset='latin1'
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Eventos")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"✅ mysql.connector latin1: {count} eventos encontrados")
        return True
        
    except Exception as e:
        print(f"❌ mysql.connector latin1 falló: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 PRUEBA DE ESTRATEGIAS DE CONEXIÓN MYSQL")
    print("=" * 60)
    
    strategies = [
        test_mysql_connector,
        test_mysql_connector_simple,
        test_pymysql,
        test_mysql_connector_latin1
    ]
    
    results = []
    for strategy in strategies:
        try:
            result = strategy()
            results.append(result)
        except Exception as e:
            print(f"❌ Error fatal en estrategia: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    strategy_names = [
        "mysql.connector básico",
        "mysql.connector simple", 
        "PyMySQL",
        "mysql.connector latin1"
    ]
    
    successful = 0
    for i, (name, result) in enumerate(zip(strategy_names, results)):
        status = "✅ ÉXITO" if result else "❌ FALLO"
        print(f"{i+1}. {name}: {status}")
        if result:
            successful += 1
    
    print(f"\n🎯 {successful}/{len(strategies)} estrategias exitosas")
    
    if successful > 0:
        print("✅ Al menos una estrategia funciona - la compilación debería funcionar")
    else:
        print("❌ Ninguna estrategia funciona - revisar configuración de base de datos")
    
    return successful > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)