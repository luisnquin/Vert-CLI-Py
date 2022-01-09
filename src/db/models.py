from datetime import datetime


class TaskTable():
    def get():
        return 'SELECT t.id, t.name, t.category, s.symbol AS status, t.datetime FROM tasks AS t INNER JOIN status AS s ON t.status = s.id ORDER BY id ASC;'

    def clean():
        return f'DELETE FROM tasks WHERE status = 1;'

    def __init__(self, id=None, name=None, status=None, category=None):
        self.id = id
        self.name = name
        self.status = status
        self.category = category
        self.datetime = datetime.now()

    def add(self):
        return f"INSERT INTO tasks(name, category, status, datetime) VALUES('{self.name}', '{self.category}', {self.status}, '{self.datetime}');"

    def updateStatus(self):
        return f'UPDATE tasks SET status = {self.status} WHERE id = {self.id};'

    def updateCategory(self):
        return f'UPDATE tasks SET category = {self.category} WHERE id = {self.id};'

    def delete(self):
        if self.id:
            return f"DELETE FROM tasks WHERE id = {self.id};"


class CategoryTable():
    def exists(category):
        return f"SELECT COUNT(id) FROM categories WHERE name LIKE '{category}%';"

    def __init__(self, id: str = None, name: str = None):
        self.id = id
        self.name = name

    def add(self):
        return f"INSERT INTO categories(name) VALUES('{self.name};')"

    def delete(self):
        return f"DELETE FROM categories WHERE id = {self.id};"


class IdeaTable():
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.datetime = datetime.now()

    def add(self):
        return f"INSERT INTO ideas(name, datetime) VALUES('{self.name}', '{self.datetime}');"

    def delete(self):
        return f"DELETE FROM ideas WHERE id = {self.id};"
