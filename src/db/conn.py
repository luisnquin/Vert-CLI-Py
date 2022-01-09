from datetime import datetime

from typing import Optional
import psycopg2

from constants.constants import DSN


class DbConnection():
    connection: any
    cursor: any

    def __str__(self):
        return 'Waiting for requests!'

    def execute(self, query: str, get: Optional[bool] = False):
        self.connection = psycopg2.connect(DSN)
        self.cursor = self.connection.cursor()

        # The targets to protect are the queries that gonna be executed
        try:
            if get:
                self.cursor.execute(query)
                data = self.cursor.fetchall()
                self.connection.close()
                return data

            self.cursor.execute(query)
        except Exception as error:
            return f'{datetime.now()}\n\nError: {error}'

        self.connection.commit()
        self.connection.close()
        return '\nThe last action was committed!'

    def exists(self, query:str):
        self.connection = psycopg2.connect(DSN)
        self.cursor = self.connection.cursor()

        self.cursor.execute(query)

        result = self.cursor.fetchone()[0]
        self.connection.close()
        return result
