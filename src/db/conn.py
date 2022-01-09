from constants.constants import DSN
from typing import Optional
from datetime import datetime
import psycopg2


class DbConnection():
    connection: any
    cursor: any

    def __str__(self):
        return 'Nothing to connnect to Vert!'

    def execute(self, sentence: str, get: Optional[bool] = False):
        self.connection = psycopg2.connect(DSN)
        self.cursor = self.connection.cursor()

        try:
            if get is not None:
                if get == True:
                    self.cursor.execute(sentence)
                    data = self.cursor.fetchall()
                    self.connection.close()
                    return data

            self.cursor.execute(sentence)
        except Exception as error:
            return f'{datetime.now()}\n\nError: {error}'

        self.connection.commit()
        self.connection.close()
        return 'The last action was committed!'
