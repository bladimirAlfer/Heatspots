import pymysql
import os

class DAOSensores:
    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        self.connection = self.connect_to_db()
        self.cursor = self.connection.cursor()

    def connect_to_db(self):
        """Establece la conexión a la base de datos."""
        return pymysql.connect(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            db=os.getenv("DB_NAME", "heatspots_db"),
        )

    # Obtener todos los sensores con la última temperatura e imagen
    def obtener_sensores(self):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        query = """
        SELECT 
            s.id_sensor, 
            s.nombre, 
            s.estado, 
            u.nombre AS ubicacion, 
            p.nombre AS piso, 
            i.nombre AS institucion,
            -- Últimos datos de sensor_registros
            (SELECT temperatura 
             FROM sensor_registros sr 
             WHERE sr.id_sensor = s.id_sensor 
             ORDER BY sr.fecha_registro DESC 
             LIMIT 1) AS ultima_temp,
            (SELECT imagen 
             FROM sensor_registros sr 
             WHERE sr.id_sensor = s.id_sensor 
             ORDER BY sr.fecha_registro DESC 
             LIMIT 1) AS ultima_imagen,
            (SELECT fecha_registro 
             FROM sensor_registros sr 
             WHERE sr.id_sensor = s.id_sensor 
             ORDER BY sr.fecha_registro DESC 
             LIMIT 1) AS ultima_fecha
        FROM 
            sensores s
        JOIN 
            ubicaciones u ON s.id_ubicacion = u.id_ubicacion
        JOIN 
            pisos p ON s.id_piso = p.id_piso
        LEFT JOIN 
            instituciones i ON s.id_institucion = i.id_institucion;
        """
        try:
            cursor.execute(query)
            sensores = cursor.fetchall()

            # Procesar cada sensor para manejar el campo `ultima_imagen`
            for sensor in sensores:
                if sensor["ultima_imagen"]:  # Si hay datos en `ultima_imagen`
                    try:
                        # Decodificar de bytes a string si es necesario
                        sensor["ultima_imagen"] = sensor["ultima_imagen"].decode("utf-8")
                    except AttributeError:
                        # Si ya es un string, no hacemos nada
                        pass

            return sensores
        except Exception as e:
            print(f"Error al obtener sensores: {e}")
            return None
        finally:
            con.close()

    # Insertar sensor
    def insertar_sensor(self, data):
        con = self.connect_to_db()
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO sensores (nombre, id_institucion, id_piso, id_ubicacion, estado) 
                VALUES (%s, %s, %s, %s, %s)
            """, (data['nombre'], data['id_institucion'], data['id_piso'], data['id_ubicacion'], data['estado']))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al insertar sensor: {e}")
            con.rollback()
            return False
        finally:
            con.close()

    # Actualizar sensor
    def actualizar_sensor(self, id_sensor, data):
        con = self.connect_to_db()
        cursor = con.cursor()
        try:
            cursor.execute("""
                UPDATE sensores 
                SET nombre = %s, id_institucion = %s, id_piso = %s, 
                    id_ubicacion = %s, estado = %s
                WHERE id_sensor = %s
            """, (data['nombre'], data['id_institucion'], data['id_piso'], 
                  data['id_ubicacion'], data['estado'], id_sensor))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar sensor: {e}")
            con.rollback()
            return False
        finally:
            con.close()

    # Eliminar sensor
    def eliminar_sensor(self, id_sensor):
        con = self.connect_to_db()
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM sensores WHERE id_sensor = %s", (id_sensor,))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar sensor: {e}")
            con.rollback()
            return False
        finally:
            con.close()

    # Obtener un sensor por su ID
    def obtener_sensor_por_id(self, id_sensor):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM sensores WHERE id_sensor = %s", (id_sensor,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener sensor: {e}")
            return None
        finally:
            con.close()

    # Actualizar el estado de un sensor
    def actualizar_estado(self, id_sensor, estado):
        try:
            # Verificar si el sensor existe
            query_verificar = "SELECT COUNT(*) AS count FROM sensores WHERE id_sensor = %s"
            self.cursor.execute(query_verificar, (id_sensor,))
            result = self.cursor.fetchone()
            
            if result["count"] == 0:
                raise ValueError(f"El sensor con ID {id_sensor} no existe.")

            # Actualizar el estado del sensor
            query_actualizar = "UPDATE sensores SET estado = %s WHERE id_sensor = %s"
            self.cursor.execute(query_actualizar, (estado, id_sensor))
            self.connection.commit()

        except Exception as e:
            print(f"Error al actualizar el estado del sensor {id_sensor}: {e}")
            raise

    def cerrar_conexion(self):
        """Cierra la conexión y el cursor."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
