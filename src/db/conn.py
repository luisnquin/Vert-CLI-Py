from constants.constants import DSN
from typing import Optional
import psycopg2


class DbConnection():
    connection: any
    cursor: any

    def __str__(self):
        return 'Nothing to connnect to Vert!'

    def execute(self, sentence: str, get: Optional[str] = None):
        self.connection = psycopg2.connect(DSN)
        self.cursor = self.connection.cursor()

        if get is not None:
            if get == "many":
                self.cursor.execute(sentence)
                data = self.cursor.fetchall()
                self.connection.close()
                return data

            if get == "one":
                self.cursor.execute(sentence)
                data = self.cursor.fetchone()
                self.connection.close()
                return data

        self.cursor.execute(sentence)
        self.connection.commit()
        self.connection.close()
        return
