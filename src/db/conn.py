from datetime import datetime

from typing import Optional
import psycopg2

from constants.constants import DSN


class DbConnection():
    connection: any
    cursor: any

    def __str__(self):
        return 'Waiting for requests!'

    def execute(self, sentence: str, get: Optional[bool] = False):
        self.connection = psycopg2.connect(DSN)
        self.cursor = self.connection.cursor()

        # The targets to protect are the queries that gonna be executed
        try:
            if get:
                self.cursor.execute(sentence)
                data = self.cursor.fetchall()
                self.connection.close()
                return data

            self.cursor.execute(sentence)
        except Exception as error:
            return f'{datetime.now()}\n\nError: {error}'

        self.connection.commit()
        self.connection.close()
        return '\nThe last action was committed!'

    def category_exists(self, category: str):
        self.connection = psycopg2.connect(DSN)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            f"SELECT COUNT(id) FROM categories WHERE name LIKE '{category}%';"
        )

        result = self.cursor.fetchone()[0]
        self.connection.close()
        return result
