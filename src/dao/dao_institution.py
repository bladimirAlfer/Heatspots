import pymysql
import os

class DAOInstitucion:
    def connect_to_db(self):
        """Establece la conexión a la base de datos."""
        return pymysql.connect(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            db=os.getenv("DB_NAME", "heatspots_db"),
        )
    def obtener_instituciones(self):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT instituciones.*, 
                (SELECT COUNT(*) FROM sensores WHERE sensores.estado = 'encendido' AND sensores.id_piso IN (
                    SELECT id_piso FROM pisos WHERE pisos.id_institucion = instituciones.id_institucion
                )) AS sensores_activos 
                FROM instituciones
            """)
            return cursor.fetchall()
        finally:
            con.close()


    def agregar_institucion(self, data):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            cursor.execute("""
                INSERT INTO instituciones (nombre, logo, descripcion, imagen_universidad)
                VALUES (%s, %s, %s, %s)
            """, (data['nombre'], data['logo'], data['descripcion'], data['imagen_universidad']))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al agregar institución: {e}")
            con.rollback()
            return False
        finally:
            con.close()


    def eliminar_institucion(self, id_institucion):
        con = self.connect_to_db()
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM instituciones WHERE id_institucion=%s", (id_institucion,))
            con.commit()
            return True
        finally:
            con.close()

    # Obtener institución por ID
    def get_by_id(self, id_institucion):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM instituciones WHERE id_institucion = %s", (id_institucion,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener la institución: {e}")
            return None
        finally:
            con.close()

    def update(self, id_institucion, nombre, descripcion, logo, imagen_universidad):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            # Consulta para actualizar solo los campos que no son None
            sql = """
                UPDATE instituciones
                SET nombre = %s, descripcion = %s
            """
            params = [nombre, descripcion]

            if logo:
                sql += ", logo = %s"
                params.append(logo)

            if imagen_universidad:
                sql += ", imagen_universidad = %s"
                params.append(imagen_universidad)

            sql += " WHERE id_institucion = %s"
            params.append(id_institucion)

            cursor.execute(sql, params)
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar institución: {e}")
            con.rollback()
            return False
        finally:
            con.close()

