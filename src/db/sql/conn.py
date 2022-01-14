from datetime import datetime
from typing import Optional, Union
from typer import Exit

import psycopg2

from utils.utils import get_json, print_fatal
from constants.constants import config_path


class DbConnection():
    @staticmethod
    def ping() -> int:
        dsn: str = get_json(config_path)['dsn']
        try:
            connection: object = psycopg2.connect(dsn)
            cursor: object = connection.cursor()
            cursor.execute('SELECT 1;')
            connection.close()
            return 1

        except psycopg2.OperationalError:
            return 0

    def __init__(self) -> None:
        dsn: str = get_json(config_path)['dsn']
        try:
            self.connection: object = psycopg2.connect(dsn)
            self.cursor: object = self.connection.cursor()

        except Exception as error:
            print_fatal(error)
            raise Exit(code=1)

    def __str__(self) -> str:
        return '\nDatabase connected, waiting for requests!'

    def execute(self, query: str, get: Optional[bool] = False) -> Union[tuple[tuple[any]], str]:
        try:
            if get:
                self.cursor.execute(query)
                data: tuple[tuple[any]] = self.cursor.fetchall()
                return data

            self.cursor.execute(query)

        except Exception as error:
            return f'{datetime.now()}\nMessage: {error}'

        self.connection.commit()
        return '\nThe last action was committed!'

    def close(self) -> None:
        self.connection.close()

    def exists(self, query: str) -> int:
        self.cursor.execute(query)
        result: int = self.cursor.fetchone()[0]

        return result
