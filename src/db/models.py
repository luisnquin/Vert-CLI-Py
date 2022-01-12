from datetime import datetime


class Tables():
    @staticmethod
    def get() -> str:
        return 'SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\' AND table_type=\'BASE TABLE\';'

    @staticmethod
    def migrate(path: str) -> list[str]:
        with open(path, 'r') as sql:
            queries: list[str] = sql.readlines()

        return queries

    @staticmethod
    def drop_and_create(path: str) -> list[str]:
        with open(path, 'r') as sql:
            queries: list[str] = sql.readlines()

        return queries


class Tasks():
    @staticmethod
    def get() -> str:
        return 'SELECT t.id, t.name, t.category, s.symbol AS status, t.datetime FROM tasks AS t INNER JOIN status AS s ON t.status = s.id ORDER BY id ASC;'

    @staticmethod
    def clean() -> str:
        return f'DELETE FROM tasks WHERE status = 1;'

    def __init__(self, id: int = None, name: str = None, status: int = None, category: str = None):
        self.id: int = id
        self.name: str = name
        self.status: int = status
        self.category: str = category
        self.datetime: datetime = datetime.now()

    def add(self) -> str:
        return f"INSERT INTO tasks(name, category, status, datetime) VALUES('{self.name}', '{self.category}', {self.status}, '{self.datetime}');"

    def update_status(self) -> str:
        return f'UPDATE tasks SET status = {self.status} WHERE id = {self.id};'

    def update_category(self) -> str:
        return f'UPDATE tasks SET category = {self.category} WHERE id = {self.id};'

    def delete(self) -> str:
        return f"DELETE FROM tasks WHERE id = {self.id};"


class Categories():
    @staticmethod
    def get() -> str:
        return 'SELECT name FROM categories;'

    def __init__(self, id: int = None, name: str = None):
        self.id: int = id
        self.name: str = name

    def add(self) -> str:
        return f"INSERT INTO categories(name) VALUES('{self.name}');"

    def delete(self) -> str:
        return f"DELETE FROM categories WHERE id = {self.id};"


class Ideas():
    @staticmethod
    def get() -> str:
        return 'SELECT * FROM ideas;'

    def __init__(self, id: id = None, name: str = None):
        self.id: int = id
        self.name: str = name
        self.datetime: datetime = datetime.now()

    def add(self) -> str:
        return f"INSERT INTO ideas(name, datetime) VALUES('{self.name}', '{self.datetime}');"

    def delete(self) -> str:
        return f"DELETE FROM ideas WHERE id = {self.id};"
