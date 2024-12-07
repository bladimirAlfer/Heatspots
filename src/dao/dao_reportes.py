import pymysql

class DAOReportes:
    def connect(self):
        return pymysql.connect(host="localhost", user="root", password="", db="heatspots_db")

    def insert(self, data):
        query = """
        INSERT INTO reportes (id_institucion, id_piso, id_calefactor, tipo_reporte, comentario)
        VALUES (%s, %s, %s, %s, %s)
        """  
        params = (
            data['id_institucion'],
            data['id_piso'],
            data['id_calefactor'],
            data['tipo_reporte'],
            data['comentario']
        )
        connection = self.connect()  # Establece la conexión
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()  # Guarda los cambios
        except Exception as e:
            print(f"Error al insertar reporte: {e}")
            connection.rollback()  # Deshace los cambios en caso de error
        finally:
            connection.close()  # Cierra la conexión

    def actualizar_estado(self, id_reporte, nuevo_estado):
        con = self.connect()
        cursor = con.cursor()
        try:
            query = "UPDATE reportes SET estado = %s WHERE id_reporte = %s"
            cursor.execute(query, (nuevo_estado, id_reporte))
            con.commit()
        except Exception as e:
            print(f"Error al actualizar el estado del reporte {id_reporte}: {e}")
            raise
        finally:
            con.close()

    def obtener_reportes_completos(self):
        con = self.connect()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
                SELECT 
                    r.id_reporte,
                    i.nombre AS institucion,
                    p.nombre AS piso,
                    c.nombre AS calefactor,
                    u.nombre AS ubicacion,  -- Agregar el nombre de la ubicación
                    r.tipo_reporte,
                    r.comentario,
                    r.estado
                FROM reportes r
                LEFT JOIN instituciones i ON r.id_institucion = i.id_institucion
                LEFT JOIN pisos p ON r.id_piso = p.id_piso
                LEFT JOIN calefactores c ON r.id_calefactor = c.id_calefactor
                LEFT JOIN ubicaciones u ON c.id_ubicacion = u.id_ubicacion  -- Relación con la tabla de ubicaciones
                ORDER BY r.id_reporte DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener reportes completos: {e}")
            return []
        finally:
            con.close()

    def eliminar_reporte(self, id_reporte):
        con = self.connect()
        cursor = con.cursor()
        try:
            query = "DELETE FROM reportes WHERE id_reporte = %s"
            cursor.execute(query, (id_reporte,))
            con.commit()
            print(f"Reporte con ID {id_reporte} eliminado correctamente.")
        except Exception as e:
            print(f"Error al eliminar reporte {id_reporte}: {e}")
            con.rollback()
            raise
        finally:
            con.close()
