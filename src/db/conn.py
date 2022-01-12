from datetime import datetime
from typing import Optional, Union
from typer import Exit

import psycopg2

from utils.utils import get_config, print_fatal
from constants.constants import config_path


class DbConnection():
    @staticmethod
    def ping() -> int:
        c = get_config(config_path)
        dsn: str = 'dbname={} user={} password={} host={} port={}'\
            .format(c['database'], c['user'], c['password'], c['host'], c['port'])

        try:
            connection: object = psycopg2.connect(dsn)
            cursor: object = connection.cursor()
        except psycopg2.OperationalError:
            return 0

        cursor.execute('SELECT 1;')
        pong: tuple[int] = cursor.fetchone()
        connection.close()
        
        return pong[0]

    def __init__(self) -> None:
        c = get_config(config_path)

        try:
            self.dsn: str = 'dbname={} user={} password={} host={} port={}'\
                .format(c['database'], c['user'], c['password'], c['host'], c['port'])

            self.connection: object = psycopg2.connect(self.dsn)
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
            return f'{datetime.now()} \n\nMessage: {error}'

        self.connection.commit()
        return '\nThe last action was committed!'

    def close(self) -> None:
        self.connection.close()

    def exists(self, query: str) -> int:
        self.cursor.execute(query)
        result: int = self.cursor.fetchone()[0]

        return result
