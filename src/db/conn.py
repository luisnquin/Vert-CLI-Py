from datetime import datetime
from typing import Optional, Union
from typer import Exit

import psycopg2

from utils.utils import get_config, print_fatal


class DbConnection():
    def __init__(self) -> None:
        c = get_config('./priv_config.json')
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
                self.connection.close()
                return data

            self.cursor.execute(query)
        except Exception as error:
            return f'{datetime.now()}\n\nError: {error}'

        self.connection.commit()
        self.connection.close()

        return '\nThe last action was committed!'

    def get_tables(self) -> tuple[tuple[str]]:
        try:
            self.cursor.execute(
                'SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\' AND table_type=\'BASE TABLE\';'
            )
        except Exception as error:
            print_fatal(error)
            raise Exit(code=1)

        data: tuple[tuple[str]] = self.cursor.fetchall()
        self.connection.close()
        return data

    def migrate(self, path: str) -> str:
        try:
            with open(path, 'r') as sql:
                queries: list[str] = sql.readlines()
        except Exception as error:
            print_fatal(error)
            raise Exit(code=1)

        try:
            for query in queries:
                if query[:4] == 'DROP' or query[:6] == 'INSERT':
                    continue
                self.cursor.execute(query)

        except Exception as error:
            print_fatal(error)
            raise Exit(code=1)

        self.connection.commit()
        self.connection.close()
        return 'Migrations carried out'

    def drop_and_create(self, path: str) -> str:
        try:
            with open(path, 'r') as sql:
                queries: list[str] = sql.readlines()
        except Exception as error:
            print_fatal(error)
            raise Exit(code=1)

        try:
            for query in queries:
                self.cursor.execute(query)
        except Exception as error:
            print_fatal(error)
            raise Exit(code=1)

        self.connection.commit()
        self.connection.close()

        return 'Tables dropped and created in designated database'

    def exists(self, query: str) -> int:
        self.cursor.execute(query)
        result: int = self.cursor.fetchone()[0]
        self.connection.close()

        return result
