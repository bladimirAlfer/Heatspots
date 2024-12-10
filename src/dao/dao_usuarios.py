import pymysql
import os
from werkzeug.security import generate_password_hash

class DAOUsuario:
    def connect_to_db(self):
        """Establece la conexión a la base de datos."""
        return pymysql.connect(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            db=os.getenv("DB_NAME", "heatspots_db"),
        )

    # Método insert de DAOUsuario actualizado
    def insert(self, data):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, apellido, email, password, telefono, direccion, imagen_perfil, acerca_de, rol)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (data['nombre'], data['apellido'], data['email'], data['password'], 
                data.get('telefono'), data.get('direccion'), 
                data.get('imagen_perfil'), 
                data.get('acerca_de', ''), data['rol']))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            con.rollback()
            return False
        finally:
            con.close()


    # Obtener usuario por email
    def get_by_email(self, email):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener usuario por email: {e}")
            return None
        finally:
            con.close()



    # Actualizar usuario por email y manejar la actualización de la imagen de perfil
    def update_user(self, email, data):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            # Si el usuario ha subido una nueva imagen, la incluimos en la actualización
            if 'imagen_perfil' in data:
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre=%s, apellido=%s, telefono=%s, direccion=%s, acerca_de=%s, imagen_perfil=%s
                    WHERE email=%s
                """, (data.get('nombre'), data.get('apellido'), 
                    data.get('telefono'), data.get('direccion'), 
                    data.get('acerca_de'), data.get('imagen_perfil'), email))
            else:
                # Si no hay nueva imagen, no actualizamos el campo de la imagen de perfil
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre=%s, apellido=%s, telefono=%s, direccion=%s, acerca_de=%s
                    WHERE email=%s
                """, (data.get('nombre'), data.get('apellido'), 
                    data.get('telefono'), data.get('direccion'), 
                    data.get('acerca_de'), email))
            
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            con.rollback()
            return False
        finally:
            con.close()


    # Eliminar usuario por email
    def delete_user(self, email):
        con = self.connect_to_db()
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM usuarios WHERE email = %s", (email,))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            con.rollback()
            return False
        finally:
            con.close()


    def get_all(self):
        con = self.connect_to_db()
        cursor = con.cursor(pymysql.cursors.DictCursor)  # Asegúrate de usar DictCursor
        try:
            cursor.execute("""
                SELECT nombre, apellido, email, telefono, direccion, rol
                FROM usuarios
                ORDER BY created_at DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []  # Devuelve una lista vacía en caso de error
        finally:
            con.close()

