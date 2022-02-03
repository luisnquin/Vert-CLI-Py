from typing import Callable, Union, Iterator
from base64 import b64decode
import psycopg2

from utils.utils import print_fatal, print_success, user_config


def connect_and_execute(func: Callable) -> None:
    def inner_func(*arg) -> None:
        try:
            dsn_encoded: str = user_config(section='database', option='dsn')
            dsn: str = b64decode(dsn_encoded).decode(encoding='UTF-8')

            statement: str = func(*arg)
            with psycopg2.connect(dsn=dsn) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(statement)
                    connection.commit()

            print_success('Statement successfully executed!')

        except Exception as error:
            print_fatal(error)

    return inner_func


def connect_execute_and_get(func: Callable) -> None:
    def inner_func() -> tuple[tuple[any]]:
        try:
            dsn_encoded: str = user_config(section='database', option='dsn')
            dsn: str = b64decode(dsn_encoded).decode(encoding='UTF-8')

            query: str = func()
            with psycopg2.connect(dsn=dsn) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    data: tuple[tuple[any]] = cursor.fetchall()

            return data

        except Exception as error:
            print_fatal(error)

    return inner_func


def connect_and_execute_many(func: Callable) -> tuple[tuple[Union[any]]]:
    def inner_func(*arg) -> Union[tuple, None]:
        try:
            dsn_encoded: str = user_config(section='database', option='dsn')
            dsn: str = b64decode(dsn_encoded).decode(encoding='ascii')

            statements: Iterator = func(*arg)
            with psycopg2.connect(dsn=dsn) as connection:
                with connection.cursor() as cursor:
                    for statement in statements:
                        cursor.execute(statement)
                        connection.commit()

        except Exception as error:
            print_fatal(error)

    return inner_func


if __name__ == '__main__':
    pass
