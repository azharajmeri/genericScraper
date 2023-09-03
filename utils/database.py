import logging

import mysql.connector

# Set up logging
logging.basicConfig(level=logging.ERROR)


class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.conn
        except mysql.connector.Error as err:
            logging.error(f"Error connecting to the database: {err}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
