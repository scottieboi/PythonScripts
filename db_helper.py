import psycopg2
import os
from dotenv import load_dotenv


class DbHelper:
    def __init__(self):
        try:
            load_dotenv()
            # Connect to an existing database
            self.connection = psycopg2.connect(
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host="127.0.0.1",
                port="5432",
                database="wines")

            self.cursor = self.connection.cursor()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def close_connection(self):
        if (self.connection):
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
