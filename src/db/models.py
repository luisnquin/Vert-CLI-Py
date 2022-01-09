from datetime import datetime
from .schemas import *


class Task():
    task: TaskSchema

    def get():
        return 'SELECT t.id, t.name, t.category, s.symbol AS status, t.datetime FROM tasks AS t INNER JOIN status AS s ON t.status = s.id ORDER BY id ASC;'

    def __init__(self, task: TaskSchema):
        self.task = task
        self.task.datetime = datetime.now()

    def add(self):
        return f"INSERT INTO tasks(name, category, status, datetime) VALUES('{self.task.name}', '{self.task.category}', {self.task.status}, '{self.task.datetime}');"

    def updateStatus(self):
        return f'UPDATE tasks SET status = {self.task.status} WHERE id = {self.task.id};'

    def delete(self):
        if self.task.id:
            return f"DELETE FROM tasks WHERE id = {self.task.id};"


class Category():
    category: CategorySchema

    def __init__(self, category: CategorySchema):
        self.category = category

    def add(self):
        return f"INSERT INTO categories(name) VALUES('{self.category.name};')"

    def delete(self):
        return f"DELETE FROM categories WHERE id = {self.category.id};"
