import mysql.connector
from config import settings

class DatabaseConfig:
    def __init__(self):
        self.host = settings.DB_SETTINGS["host"]
        self.port = settings.DB_SETTINGS["port"]
        self.user = settings.DB_SETTINGS["user"]
        self.password = settings.DB_SETTINGS["password"]
        self.database = settings.DB_SETTINGS["database"]

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connection to database established successfully.")
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

