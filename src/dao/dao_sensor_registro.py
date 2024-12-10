import pymysql
import os

class DAOSensorRegistro:
    def connect_to_db(self):
        """Establece la conexión a la base de datos."""
        return pymysql.connect(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            db=os.getenv("DB_NAME", "heatspots_db"),
        )

    # Obtener el último registro de un sensor (temperatura o imagen) por id_calefactor
    def get_ultimo_registro(self, id_calefactor):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            cursor.execute("""
                SELECT sr.temperatura, sr.imagen, sr.fecha_registro
                FROM sensor_registros sr
                JOIN sensores s ON sr.id_sensor = s.id_sensor
                JOIN calefactores c ON s.id_ubicacion = c.id_ubicacion
                WHERE c.id_calefactor = %s
                ORDER BY sr.fecha_registro DESC
                LIMIT 1
            """, (id_calefactor,))
            registro = cursor.fetchone()
            if registro and registro['imagen']:
                registro['imagen'] = registro['imagen'].decode('latin1')  # Convertir imagen binaria si es necesario
            return registro
        except Exception as e:
            print(f"Error al obtener el último registro del sensor: {e}")
            return None
        finally:
            con.close()

    # Sincronizar datos desde la tabla esp32cam a sensor_registros
    def sincronizar_datos(self, id_sensor):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            # Obtener el último registro de esp32cam
            cursor.execute("SELECT temperatura, imagen FROM esp32cam WHERE id = 1")
            datos = cursor.fetchone()

            if not datos:
                print("No se encontraron datos en la tabla esp32cam.")
                return False

            # Insertar el registro en sensor_registros
            cursor.execute("""
                INSERT INTO sensor_registros (id_sensor, temperatura, imagen)
                VALUES (%s, %s, %s)
            """, (id_sensor, datos['temperatura'], datos['imagen']))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al sincronizar datos desde esp32cam: {e}")
            con.rollback()
            return False
        finally:
            con.close()

    # Obtener todos los registros de un sensor por id_sensor
    def get_registros_por_sensor(self, id_sensor):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            cursor.execute("""
                SELECT temperatura, imagen, fecha_registro
                FROM sensor_registros
                WHERE id_sensor = %s
                ORDER BY fecha_registro DESC
            """, (id_sensor,))
            registros = cursor.fetchall()
            for registro in registros:
                if registro['imagen']:
                    registro['imagen'] = registro['imagen'].decode('latin1')  # Convertir la imagen binaria
            return registros
        except Exception as e:
            print(f"Error al obtener registros por sensor: {e}")
            return []
        finally:
            con.close()

    # Guardar un registro manualmente en sensor_registros
    def guardar_registro(self, id_sensor, temperatura, imagen):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            cursor.execute("""
                INSERT INTO sensor_registros (id_sensor, temperatura, imagen)
                VALUES (%s, %s, %s)
            """, (id_sensor, temperatura, imagen))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al guardar registro en sensor_registros: {e}")
            con.rollback()
            return False
        finally:
            con.close()
