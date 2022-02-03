from datetime import datetime
from typing import Optional

from db.conn import connect_and_execute, connect_execute_and_get, connect_and_execute_many
from utils.utils import check_and_put_singlequotes


class Database:
    @staticmethod
    @connect_execute_and_get
    def ping() -> str: return 'SELECT 1;'


class Tables:
    @staticmethod
    @connect_execute_and_get
    def get() -> str: return 'SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\';'

    @staticmethod
    @connect_and_execute_many
    def drop_and_create() -> tuple[str]:
        return (
            'DROP TABLE IF EXISTS tasks;',
            'DROP TABLE IF EXISTS categories;',
            'DROP TABLE IF EXISTS status;',
            'DROP TABLE IF EXISTS ideas;',
            'DROP TABLE IF EXISTS urls;',
            'DROP TABLE IF EXISTS notifications',
            'CREATE TABLE IF NOT EXISTS status (id INTEGER, symbol CHAR(1), PRIMARY KEY(id));',
            'CREATE TABLE IF NOT EXISTS categories (id INTEGER GENERATED ALWAYS AS IDENTITY, name VARCHAR(35) NOT NULL UNIQUE, PRIMARY KEY(id));',
            'CREATE TABLE IF NOT EXISTS tasks (id INTEGER GENERATED ALWAYS AS IDENTITY, name TEXT NOT NULL, category VARCHAR(25) NOT NULL, status INTEGER NOT NULL, datetime TIMESTAMP NOT NULL, PRIMARY KEY(id), CONSTRAINT fk_category_categories FOREIGN KEY(category) REFERENCES categories(name) ON UPDATE CASCADE ON DELETE CASCADE, CONSTRAINT fk_status_status FOREIGN KEY(status) REFERENCES status(id) ON UPDATE RESTRICT ON DELETE RESTRICT);',
            'CREATE TABLE IF NOT EXISTS ideas (id INTEGER GENERATED ALWAYS AS IDENTITY, name TEXT NOT NULL, datetime TIMESTAMP NOT NULL, PRIMARY KEY(id));',
            'CREATE TABLE IF NOT EXISTS urls (id INTEGER GENERATED ALWAYS AS IDENTITY, title TEXT not null default \'Unknown\', url TEXT not null, datetime TIMESTAMP NOT NULL, PRIMARY KEY(id));',
            'CREATE TABLE IF NOT EXISTS notifications (id INTEGER GENERATED ALWAYS AS IDENTITY, title TEXT NOT NULL, message TEXT NOT NULL DEFAULT \'from VertCLI\', datetime TIMESTAMP NOT NULL, PRIMARY KEY(id));',
            'INSERT INTO categories(name) VALUES(\'Programming\'), (\'Projects\'), (\'Work\'), (\'Homework\');',
            'INSERT INTO status VALUES(0, \'✗\'), (1, \'✓\');'
        )


class Tasks:
    @staticmethod
    @connect_execute_and_get
    def get() -> str: return 'SELECT t.id, t.name, t.category, s.symbol AS status, t.datetime FROM tasks AS t INNER JOIN status AS s ON t.status = s.id ORDER BY t.id ASC;'

    @staticmethod
    @connect_and_execute
    def clean() -> str: return 'DELETE FROM tasks WHERE status = 1;'

    def __init__(self, id: Optional[int] = None, ids: Optional[tuple[int]] = None, name: Optional[str] = None, status: Optional[int] = 0, category: Optional[str] = None) -> object:
        self.id: int = id
        self.ids: tuple[int] = ids
        self.name: str = check_and_put_singlequotes(name)
        self.status: int = status
        self.category: str = category
        self.datetime: datetime = datetime.now()

    @connect_and_execute
    def add(self) -> str:
        return 'INSERT INTO tasks(name, category, status, datetime) VALUES(\'%s\', \'%s\', %d, \'%s\');' % (self.name, self.category, self.status, self.datetime)

    @connect_and_execute_many
    def check(self) -> str:
        for id in self.ids:
            yield 'UPDATE tasks SET status = 1 WHERE id = %d;' % (id)

    @connect_and_execute_many
    def delete(self) -> str:
        for id in self.ids:
            yield 'DELETE FROM tasks WHERE id = %d;' % (id)


class Categories:
    @staticmethod
    @connect_execute_and_get
    def get() -> str: return 'SELECT * FROM categories;'

    def __init__(self, id: Optional[int] = None, ids: Optional[tuple[int]] = None, name: Optional[str] = None) -> object:
        self.id: int = id
        self.ids: tuple[int] = ids
        self.name: str = check_and_put_singlequotes(name)

    @connect_and_execute
    def add(self) -> str:
        return 'INSERT INTO categories(name) VALUES(\'%s\');' % (self.name)

    @connect_and_execute_many
    def delete(self) -> str:
        for id in self.ids:
            yield 'DELETE FROM categories WHERE id = %d;' % (id)


class Ideas:
    @staticmethod
    @connect_execute_and_get
    def get() -> str: return 'SELECT * FROM ideas;'

    def __init__(self, id: Optional[int] = None, ids: Optional[tuple[int]] = None, name: Optional[str] = None) -> object:
        self.id: int = id
        self.ids: tuple[int] = ids
        self.name: str = check_and_put_singlequotes(name)
        self.datetime: datetime = datetime.now()

    @connect_and_execute
    def add(self) -> str:
        return 'INSERT INTO ideas(name, datetime) VALUES(\'%s\', \'%s\');' % (self.name, self.datetime)

    @connect_and_execute_many
    def delete(self) -> str:
        for id in self.ids:
            yield 'DELETE FROM ideas WHERE id = %d;' % (id)


class Urls:
    @staticmethod
    @connect_execute_and_get
    def get() -> str: return 'SELECT * FROM urls;'

    def __init__(self, id: Optional[int] = None, ids: Optional[tuple[int]] = None, title: Optional[str] = None, url: Optional[str] = None) -> object:
        self.id: int = id
        self.ids: tuple[int] = ids
        self.title: str = check_and_put_singlequotes(title)
        self.url: str = check_and_put_singlequotes(url)
        self.datetime: datetime = datetime.now()

    @connect_and_execute
    def add(self) -> str:
        if self.title:
            return 'INSERT INTO urls(title, url, datetime) VALUES(\'%s\', \'%s\', \'%s\');' \
                % (self.title, self.url, self.datetime)

        return 'INSERT INTO urls(url, datetime) VALUES(\'%s\', \'%s\');' \
            % (self.url, self.datetime)

    @connect_and_execute_many
    def delete(self) -> str:
        for id in self.ids:
            yield 'DELETE FROM urls WHERE id = %d;' % (id)


class Routines:
    @staticmethod
    @connect_execute_and_get
    def get() -> str: return 'SELECT * FROM notifications;'

    def __init__(self, id: Optional[int] = None, ids: Optional[tuple[int]] = None, title: Optional[str] = None, message: Optional[str] = None, dt: Optional[datetime] = None):
        self.id: int = id
        self.ids: tuple[int] = ids
        self.title: str = check_and_put_singlequotes(title)
        self.message: str = check_and_put_singlequotes(message)
        self.datetime: datetime = dt

    @connect_and_execute
    def add(self) -> str:
        if self.message:
            return 'INSERT INTO notifications(title, message, datetime) VALUES(\'%s\', \'%s\', \'%s\');' % (self.title, self.message, self.datetime)

        return 'INSERT INTO notifications(title, datetime) VALUES(\'%s\', \'%s\');' % (self.title, self.datetime)

    @connect_and_execute_many
    def delete(self) -> str:
        for id in self.ids:
            yield 'DELETE FROM notifications WHERE id = %d;' % (id)
