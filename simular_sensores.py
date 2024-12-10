import pymysql
import random
import datetime
import time

# Conexión a MySQL
def connect():
    return pymysql.connect(
        host='localhost', 
        user='root', 
        password='', 
        db='heatspots_db',
        autocommit=True  # Asegura que los cambios se guarden automáticamente
    )

# Diccionario para mantener la última temperatura registrada por cada sensor
ultimo_valor = {}

# Obtener todos los sensores desde la base de datos (solo los encendidos)
def obtener_sensores():
    try:
        connection = connect()
        cursor = connection.cursor()
        query = """
        SELECT id_sensor, tipo_sensor 
        FROM sensores 
        WHERE estado = 'encendido'
        """
        cursor.execute(query)
        sensores = cursor.fetchall()  # Lista de tuplas [(id, tipo), ...]
    except Exception as e:
        print(f"Error al obtener sensores: {e}")
        sensores = []
    finally:
        cursor.close()
        connection.close()
    return sensores

# Inserta un registro para un sensor específico
def insertar_registro(id_sensor, tipo):
    try:
        connection = connect()
        cursor = connection.cursor()

        # Generar datos según el tipo de sensor
        if tipo == 'personas':
            personas = random.randint(0, 5)  # Personas entre 0 y 5
            temperatura = 0  # No genera temperatura para sensores de personas
        elif tipo == 'temperatura':
            # Obtener la última temperatura registrada para evitar variaciones bruscas
            ultima_temp = ultimo_valor.get(id_sensor, random.uniform(18, 22))
            temperatura = round(max(18, min(22, ultima_temp + random.uniform(-0.5, 0.5))), 2)
            personas = 0  # No genera personas para sensores de temperatura

            # Guardar la nueva temperatura para futuras simulaciones
            ultimo_valor[id_sensor] = temperatura

        # Inserción en la base de datos
        query = """
        INSERT INTO sensor_registros (id_sensor, temperatura, personas) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (id_sensor, temperatura, personas))
        print(f"[{datetime.datetime.now()}] Registro insertado: Sensor {id_sensor}, Temp={temperatura}, Personas={personas}")

    except Exception as e:
        print(f"Error al insertar registro para sensor {id_sensor}: {e}")

    finally:
        cursor.close()
        connection.close()

# Simula la inserción periódica de datos para todos los sensores encendidos
def simular_registros():
    sensores = obtener_sensores()  # Obtener sensores iniciales
    if not sensores:
        print("No se encontraron sensores encendidos.")

    while True:
        sensores = obtener_sensores()  # Refresh cada vez que se genera un ciclo
        for id_sensor, tipo in sensores:
            insertar_registro(id_sensor, tipo)
        time.sleep(10)  # Espera 10 segundos antes de la próxima inserción

# Ejecutar la simulación en un bucle continuo
if __name__ == "__main__":
    while True:
        try:
            simular_registros()  # Ejecuta la simulación
        except Exception as e:
            print(f"Error en la simulación: {e}")
        time.sleep(2)  # Refresh de sensores cada 2 segundos
