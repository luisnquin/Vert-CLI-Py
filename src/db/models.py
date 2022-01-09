from datetime import datetime
from .schemas import *


class Task():
    task: TaskSchema

    def __init__(self, task: TaskSchema):
        self.task = task
        self.task.datetime = datetime.now()

    def add(self):
        if self.task.description:
            return f"INSERT INTO tasks(name, description, datetime) VALUES('{self.task.name}', '{self.task.description}', '{self.task.datetime}');"

        return f"INSERT INTO tasks(name, datetime) VALUES('{self.task.name}', '{self.task.datetime}');"

    def delete(self):
        if self.task.id:
            return f"DELETE FROM tasks WHERE id = {self.task.id}"
