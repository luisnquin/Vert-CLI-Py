from datetime import datetime
from typing import Optional


class TaskTable():
    def get() -> str:
        return 'SELECT t.id, t.name, t.category, s.symbol AS status, t.datetime FROM tasks AS t INNER JOIN status AS s ON t.status = s.id ORDER BY id ASC;'

    def clean() -> str:
        return f'DELETE FROM tasks WHERE status = 1;'

    def __init__(self, id: Optional[int] = None, name: Optional[str] = None, status: Optional[int] = None, category: Optional[str] = None):
        self.id: int = id
        self.name: str = name
        self.status: int = status
        self.category: str = category
        self.datetime: datetime = datetime.now()

    def add(self) -> str:
        return f"INSERT INTO tasks(name, category, status, datetime) VALUES('{self.name}', '{self.category}', {self.status}, '{self.datetime}');"

    def updateStatus(self) -> str:
        return f'UPDATE tasks SET status = {self.status} WHERE id = {self.id};'

    def updateCategory(self) -> str:
        return f'UPDATE tasks SET category = {self.category} WHERE id = {self.id};'

    def delete(self) -> str:
        return f"DELETE FROM tasks WHERE id = {self.id};"


class CategoryTable():
    def exists(category: str) -> str:
        return f"SELECT COUNT(id) FROM categories WHERE name LIKE '{category}%';"

    def __init__(self, id: Optional[int] = None, name: Optional[str] = None):
        self.id: int = id
        self.name: str = name

    def add(self) -> str:
        return f"INSERT INTO categories(name) VALUES('{self.name};')"

    def delete(self) -> str:
        return f"DELETE FROM categories WHERE id = {self.id};"


class IdeaTable():
    def __init__(self, id: Optional[id], name: Optional[str]):
        self.id: int = id
        self.name: str = name
        self.datetime: datetime = datetime.now()

    def add(self) -> str:
        return f"INSERT INTO ideas(name, datetime) VALUES('{self.name}', '{self.datetime}');"

    def delete(self) -> str:
        return f"DELETE FROM ideas WHERE id = {self.id};"
