import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, database, user, password, port=3306):
        self.connection = mysql.connector.connect(
            host=host,
            database = database,
            user = user,
            password = password,
            port = port
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()
    
    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        return result

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params)
        result = self.cursor.fetchone()
        return result