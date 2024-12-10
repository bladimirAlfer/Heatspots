import pymysql
import os

class DAOPiso:
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
                INSERT INTO pisos (id_institucion, nombre, imagen, plano)
                VALUES (%s, %s, %s, %s)
            """, (data['id_institucion'], data['nombre'], data.get('imagen'), data.get('plano')))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al insertar piso: {e}")
            con.rollback()
            return False
        finally:
            con.close()
    # Obtener todos los pisos con sensores activos y reportes en estado 'por revisar' o 'en revision'
    # Obtener todos los pisos con sensores activos y reportes
    def obtener_pisos(self):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute("""
                SELECT p.id_piso, p.nombre, 
                    IFNULL(p.imagen, 'default_image.png') AS imagen, 
                    p.plano, i.nombre AS institucion, 
                    (SELECT COUNT(*) FROM sensores s WHERE s.id_piso = p.id_piso AND s.estado = 'encendido') AS sensores_activos,
                    (SELECT COUNT(*) FROM reportes r WHERE r.id_piso = p.id_piso AND r.estado IN ('por revisar', 'en revision')) AS reportes_activos
                FROM pisos p
                JOIN instituciones i ON p.id_institucion = i.id_institucion
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener pisos: {e}")
            return None
        finally:
            con.close()


    # Obtener un piso por ID



    def update(self, id_piso, nombre, id_institucion, imagen, plano):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            sql = """
                UPDATE pisos
                SET nombre=%s, id_institucion=%s, imagen=%s, plano=%s
                WHERE id_piso=%s
            """
            cursor.execute(sql, (nombre, id_institucion, imagen, plano, id_piso))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar piso: {e}")
            con.rollback()
            return False
        finally:
            con.close()

    # Eliminar un piso por ID
    def eliminar_piso(self, id_piso):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM pisos WHERE id_piso = %s", (id_piso,))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar piso: {e}")
            con.rollback()
            return False
        finally:
            con.close()

# Obtener pisos por ID de institución
    def get_by_institution_id(self, id_institucion):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id_piso, nombre, IFNULL(imagen, 'default_image.png') AS imagen
                FROM pisos 
                WHERE id_institucion = %s
            """, (id_institucion,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener pisos por institución: {e}")
            return None
        finally:
            con.close()


    # Obtener pisos por institución
    def obtener_pisos_por_institucion(self, id_institucion):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id_piso, nombre FROM pisos WHERE id_institucion = %s", (id_institucion,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener pisos: {e}")
            return None
        finally:
            con.close()

    def get_plano_by_piso(self, id_piso):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute("SELECT plano FROM pisos WHERE id_piso = %s", (id_piso,))
            result = cursor.fetchone()
            return result['plano'] if result else None  # Devuelve el archivo del plano si existe
        except Exception as e:
            print(f"Error al obtener el plano del piso: {e}")
            return None
        finally:
            con.close()



    def get_by_id(self, id_piso):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute("SELECT * FROM pisos WHERE id_piso = %s", (id_piso,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener piso: {e}")
            return None
        finally:
            con.close()
            
    def get_by_piso(self, id_piso):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id_ubicacion, nombre, coordenadas, imagen_ubicacion, personas 
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

