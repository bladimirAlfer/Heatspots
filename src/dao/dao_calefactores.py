import pymysql
import os

class DAOCalefactor:
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

    # Insertar un nuevo calefactor
    def insert(self, data):
        con = self.connect_to_db()
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO calefactores (nombre, id_piso, id_ubicacion, id_institucion, estado)
                VALUES (%s, %s, %s, %s, %s)
            """, (data['nombre'], data['id_piso'], data['id_ubicacion'], data['id_institucion'], data['estado']))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al insertar calefactor: {e}")
            con.rollback()
            return False
        finally:
            con.close()


    def obtener_calefactores(self):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT c.id_calefactor, c.nombre, p.nombre AS piso, u.nombre AS ubicacion, c.estado, i.nombre AS institucion,
                (SELECT temperatura FROM sensor_registros sr WHERE sr.id_sensor = s.id_sensor ORDER BY sr.fecha_registro DESC LIMIT 1) AS ultima_temp
                FROM calefactores c
                JOIN pisos p ON c.id_piso = p.id_piso
                JOIN instituciones i ON c.id_institucion = i.id_institucion
                JOIN ubicaciones u ON c.id_ubicacion = u.id_ubicacion
                LEFT JOIN sensores s ON s.id_ubicacion = u.id_ubicacion
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener calefactores: {e}")
            return None
        finally:
            con.close()

    # Actualizar calefactor
    def update(self, id_calefactor, data):
        con = self.connect_to_db()
        cursor = con.cursor()
        try:
            cursor.execute("""
                UPDATE calefactores
                SET nombre=%s, id_piso=%s, id_ubicacion=%s, id_institucion=%s
                WHERE id_calefactor=%s
            """, (data['nombre'], data['id_piso'], data['id_ubicacion'], data['id_institucion'], id_calefactor))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar calefactor: {e}")
            con.rollback()
            return False
        finally:
            con.close()


    # Eliminar calefactor
    def eliminar_calefactor(self, id_calefactor):
        con = self.connect_to_db()
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM calefactores WHERE id_calefactor = %s", (id_calefactor,))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar calefactor: {e}")
            con.rollback()
            return False
        finally:
            con.close()


    def get_by_ubicacion(self, id_ubicacion):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute("SELECT * FROM calefactores WHERE id_ubicacion = %s", (id_ubicacion,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener calefactor por ubicación: {e}")
            return None
        finally:
            con.close()

    def get_by_id(self, id_calefactor):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute("SELECT * FROM calefactores WHERE id_calefactor = %s", (id_calefactor,))
            return cursor.fetchone()  # Retorna solo una fila
        except Exception as e:
            print(f"Error al obtener el calefactor: {e}")
            return None
        finally:
            con.close()

    def obtener_pisos_y_ubicaciones(self):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT p.id_piso, p.nombre AS piso, i.nombre AS institucion 
                FROM pisos p
                JOIN instituciones i ON p.id_institucion = i.id_institucion
            """)
            pisos = cursor.fetchall()
            
            cursor.execute("""
                SELECT u.id_ubicacion, u.nombre AS ubicacion 
                FROM ubicaciones u
            """)
            ubicaciones = cursor.fetchall()
            
            return pisos, ubicaciones
        except Exception as e:
            print(f"Error al obtener pisos y ubicaciones: {e}")
            return None, None
        finally:
            con.close()



    def get_by_piso(self, id_piso):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute("SELECT id_ubicacion, nombre FROM ubicaciones WHERE id_piso = %s", (id_piso,))
            return cursor.fetchall()  # Retorna las ubicaciones filtradas por piso
        except Exception as e:
            print(f"Error al obtener ubicaciones por piso: {e}")
            return None
        finally:
            con.close()

    def get_calefactores_by_piso(self, id_piso):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT c.id_calefactor, c.nombre, u.coordenadas, c.estado
                FROM calefactores c
                JOIN ubicaciones u ON c.id_ubicacion = u.id_ubicacion
                WHERE c.id_piso = %s
            """, (id_piso,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener calefactores por piso: {e}")
            return None
        finally:
            con.close()


    def obtener_calefactor(self):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        query = """
        SELECT 
            c.id_calefactor, 
            c.nombre, 
            c.estado, 
            u.nombre AS nombre_ubicacion, 
            u.id_ubicacion 
        FROM calefactores c
        JOIN ubicaciones u ON c.id_ubicacion = u.id_ubicacion;
        """
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener calefactores: {e}")
            return None
        finally:
            con.close()

    def actualizar_estado(self, id_calefactor, estado):
        try:
            with self.connection.cursor() as cursor:
                # Verificar si el calefactor existe
                cursor.execute("SELECT COUNT(*) FROM calefactores WHERE id_calefactor = %s", (id_calefactor,))
                if cursor.fetchone()[0] == 0:
                    raise ValueError(f"El calefactor con ID {id_calefactor} no existe.")

                # Actualizar el estado del calefactor
                cursor.execute(
                    "UPDATE calefactores SET estado = %s WHERE id_calefactor = %s",
                    (estado, id_calefactor)
                )
                print(f"Estado del calefactor {id_calefactor} actualizado a {estado}.")
        except Exception as e:
            print(f"Error al actualizar el estado del calefactor {id_calefactor}: {e}")
            raise
        finally:
            self.connection.close()

    def actualizar_estado(self, id_calefactor, estado):
        try:
            # Verificar si el sensor existe
            query_verificar = "SELECT COUNT(*) AS count FROM calefactores WHERE id_calefactor = %s"
            self.cursor.execute(query_verificar, (id_calefactor,))
            result = self.cursor.fetchone()
            
            if result["count"] == 0:
                raise ValueError(f"El calefactor con ID {id_calefactor} no existe.")

            # Actualizar el estado del sensor
            query_actualizar = "UPDATE calefactores SET estado = %s WHERE id_calefactor = %s"
            self.cursor.execute(query_actualizar, (estado, id_calefactor))
            self.connection.commit()

        except Exception as e:
            print(f"Error al actualizar el estado del calefactor {id_calefactor}: {e}")
            raise

    def get_calefactores_con_ubicacion(self, id_piso):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        
        try:
            query = """
            SELECT c.id_calefactor, c.nombre AS nombre_calefactor, u.nombre AS nombre_ubicacion
            FROM calefactores c
            JOIN ubicaciones u ON c.id_ubicacion = u.id_ubicacion
            WHERE c.id_piso = %s
            """
            cursor.execute(query, (id_piso,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener calefactores con ubicación: {e}")
            return []
        finally:
            con.close()


    def cerrar_conexion(self):
        """Cierra la conexión y el cursor."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
