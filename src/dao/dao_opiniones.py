import pymysql

class DAOOpinion:
    def connect(self):
        return pymysql.connect(host="localhost", user="root", password="", db="heatspots_db")

    def get_all_opiniones(self):
        connection = self.connect()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT 
                    o.id_opinion, 
                    o.opinion_text, 
                    o.rating, 
                    o.created_at, 
                    o.id_usuario,
                    CONCAT(u.nombre, ' ', u.apellido) AS user_name
                FROM 
                    opiniones o
                JOIN 
                    usuarios u ON o.id_usuario = u.id_usuario
                ORDER BY 
                    o.created_at DESC
                """
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_all_for_admin(self):
        connection = self.connect()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT 
                    o.id_opinion, 
                    CONCAT(u.nombre, ' ', u.apellido) AS usuario, 
                    o.opinion_text AS opinion, 
                    o.rating, 
                    DATE(o.created_at) AS fecha, 
                    TIME(o.created_at) AS hora
                FROM 
                    opiniones o
                JOIN 
                    usuarios u ON o.id_usuario = u.id_usuario
                ORDER BY 
                    o.created_at DESC
                """
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            connection.close()
            
    def insert_opinion(self, opinion):
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO opiniones (id_usuario, opinion_text, rating)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (opinion['id_usuario'], opinion['opinion_text'], opinion['rating']))
                conn.commit()
        finally:
            conn.close()

    def get_opinion_by_id(self, id_opinion):
        connection = self.connect()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:  # Usar DictCursor
                query = "SELECT * FROM opiniones WHERE id_opinion = %s"
                cursor.execute(query, (id_opinion,))
                return cursor.fetchone()
        finally:
            connection.close()

    def delete(self, id_opinion):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM opiniones WHERE id_opinion = %s", (id_opinion,))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar opinión: {e}")
            con.rollback()
            return False
        finally:
            con.close()