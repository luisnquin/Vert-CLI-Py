from typing import Union

from typer import Typer, Argument, Option, Exit
from inquirer import prompt, List
from rich.console import Console
from rich.table import Table
from rich.box import SQUARE

from db.models import Tasks, Categories
from utils.utils import date_format


tasks: object = Typer()
console: object = Console()


@tasks.command()
def get():
    """
    vert tasks get
    """

    table: object = Table(box=SQUARE)
    table.add_column('ID')
    table.add_column('Name')
    table.add_column('Category')
    table.add_column('Status', justify='center')
    table.add_column('Date')

    rows: tuple[tuple] = Tasks.get()
    for row in rows:
        table.add_row('%d' % (row[0]), row[1], row[2],
                      '%s' % (row[3]), date_format(row[4]))

    console.print(table)
    raise Exit()


@tasks.command()
def add(name: str = Option(..., prompt='Task name')):
    """
    vert tasks add
    """

    categories: tuple[tuple] = Categories.get()
    answer: dict = prompt([List(name='categories', message='Select a category',
                                choices=[c[1] for c in categories])])

    Tasks(name=name, category=answer['categories']).add()
    raise Exit()


@tasks.command()
def check(ids: list[int] = Argument(...)):
    """
    vert tasks check <id's...>

    Update the status of a task
    """

    Tasks(ids=ids).check()
    raise Exit()


@tasks.command()
def remove(ids: list[int] = Argument(...)):
    """
    vert tasks remove <id's...>
    """

    Tasks(ids=ids).delete()
    raise Exit()


@tasks.command()
def clean():
    """
    vert task clean

    If the status of the task is marked as completed,
    then the task will be deleted
    """

    Tasks.clean()
    raise Exit()
