import pymysql
import os

class DAOUbicacion:
    def connect_to_db(self):
        """Establece la conexión a la base de datos."""
        return pymysql.connect(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            db=os.getenv("DB_NAME", "heatspots_db"),
        )

    def insert(self, data):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            cursor.execute("""
                INSERT INTO ubicaciones (nombre, id_piso, id_institucion, coordenadas, detalle, imagen_ubicacion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (data['nombre'], data['id_piso'], data['id_institucion'], data['coordenadas'], data['detalle'], data['imagen_ubicacion']))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al insertar ubicación: {e}")
            con.rollback()
            return False
        finally:
            con.close()



    def obtener_ubicaciones(self):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        query = """
        SELECT u.id_ubicacion, u.nombre, u.detalle, u.imagen_ubicacion, p.nombre AS piso_nombre,
            i.nombre AS institucion_nombre,  -- Incluimos el nombre de la institución
            (SELECT COUNT(*) FROM calefactores c WHERE c.id_ubicacion = u.id_ubicacion) AS cantidad_calefactores,
            (SELECT COUNT(*) FROM sensores s WHERE s.id_ubicacion = u.id_ubicacion) AS cantidad_sensores
        FROM ubicaciones u
        JOIN pisos p ON u.id_piso = p.id_piso
        JOIN instituciones i ON p.id_institucion = i.id_institucion  -- Relación con la institución
        """
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener ubicaciones: {e}")
            return None
        finally:
            con.close()


    # Actualizar una ubicación por ID
    def update(self, id_ubicacion, data):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            cursor.execute("""
                UPDATE ubicaciones
                SET nombre = %s, coordenadas = %s, id_piso = %s, detalle = %s
                WHERE id_ubicacion = %s
            """, (data['nombre'], data['coordenadas'], data['id_piso'], data['detalle'], id_ubicacion))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar ubicación: {e}")
            con.rollback()
            return False
        finally:
            con.close()

    # Eliminar una ubicación por ID
    def eliminar(self, id_ubicacion):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM ubicaciones WHERE id_ubicacion = %s", (id_ubicacion,))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar ubicación: {e}")
            con.rollback()
            return False
        finally:
            con.close()

    def get_by_id(self, id_ubicacion):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute("SELECT * FROM ubicaciones WHERE id_ubicacion = %s", (id_ubicacion,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener la ubicación: {e}")
            return None
        finally:
            con.close()


    def get_by_piso(self, id_piso):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id_ubicacion, nombre, coordenadas, imagen_ubicacion 
                FROM ubicaciones 
                WHERE id_piso = %s
            """, (id_piso,))
            ubicaciones = cursor.fetchall()
            return ubicaciones
        except Exception as e:
            print(f"Error al obtener ubicaciones: {e}")
            return None
        finally:
            con.close()



    def get_ubicacion_with_sensors(self, id_calefactor):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        query = """
        SELECT 
            u.nombre AS nombre_ubicacion, 
            u.imagen_ubicacion, 
            u.coordenadas,
            sr.temperatura AS ultima_temperatura,
            sr.imagen AS ultima_imagen
        FROM ubicaciones u
        JOIN calefactores c ON c.id_ubicacion = u.id_ubicacion
        LEFT JOIN sensores s ON s.id_ubicacion = u.id_ubicacion
        LEFT JOIN sensor_registros sr ON sr.id_sensor = s.id_sensor
        WHERE c.id_calefactor = %s
        ORDER BY sr.fecha_registro DESC
        LIMIT 1;
        """
        try:
            cursor.execute(query, (id_calefactor,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener ubicación con sensores: {e}")
            return None
        finally:
            con.close()

