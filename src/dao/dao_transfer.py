import pymysql

class DAOTransfer:
    def __init__(self):
        self.sensor_db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "sensor_db"
        }
        self.heatspots_db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "heatspots_db"
        }

    def connect_to_db(self, db_config):
        return pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            cursorclass=pymysql.cursors.DictCursor
        )

    def transfer_data(self):
        try:
            sensor_db = self.connect_to_db(self.sensor_db_config)
            heatspots_db = self.connect_to_db(self.heatspots_db_config)

            with sensor_db.cursor() as sensor_cursor, heatspots_db.cursor() as heatspots_cursor:
                sensor_cursor.execute("SELECT temperatura, imagen FROM esp32cam WHERE id = 1")
                row = sensor_cursor.fetchone()

                if row:
                    heatspots_cursor.execute("""
                        INSERT INTO sensor_registros (id_sensor, temperatura, imagen)
                        VALUES (%s, %s, %s)
                    """, (1, row['temperatura'], row['imagen']))
                    heatspots_db.commit()
                    print("Datos transferidos con éxito.")

        except Exception as e:
            print(f"Error al transferir datos: {e}")
        finally:
            if sensor_db:
                sensor_db.close()
            if heatspots_db:
                heatspots_db.close()
