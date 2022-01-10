from datetime import datetime
from typing import Optional, Union

import psycopg2

from constants.constants import DSN


class DbConnection():
    connection: object
    cursor: object

    def __str__(self) -> str:
        return 'Waiting for requests!'

    def execute(self, query: str, get: Optional[bool] = False) -> Union[tuple, str]:
        self.connection = psycopg2.connect(DSN)
        self.cursor = self.connection.cursor()

        try:
            if get:
                self.cursor.execute(query)
                data: tuple = self.cursor.fetchall()
                self.connection.close()
                return data

            self.cursor.execute(query)
        except Exception as error:
            return f'{datetime.now()}\n\nError: {error}'

        self.connection.commit()
        self.connection.close()
        return '\nThe last action was committed!'

    def exists(self, query: str) -> int:
        self.connection = psycopg2.connect(DSN)
        self.cursor = self.connection.cursor()

        self.cursor.execute(query)

        result: int = self.cursor.fetchone()[0]
        self.connection.close()
        return result
