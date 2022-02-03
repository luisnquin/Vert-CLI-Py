from typer import Typer, Argument, Option, Exit
from rich.console import Console
from rich.table import Table
from rich.box import SQUARE

from db.models import Categories


catories: object = Typer()
console: object = Console()


@catories.command()
def get():
    """
    vert categories get
    """
    table: object = Table(box=SQUARE)
    table.add_column('ID', justify='center')
    table.add_column('Categories')

    rows: tuple[tuple] = Categories.get()
    for row in rows:
        table.add_row('%d' % (row[0]), row[1])

    console.print(table)
    raise Exit()


@catories.command()
def add(name: str = Option(..., prompt='Name of the new category')):
    """
    vert categories add
    """
    Categories(name=name).add()
    raise Exit()


@catories.command()
def remove(ids: list[int] = Argument(...)):
    """
    vert categories remove <id's...>
    """
    Categories(ids=ids).delete()
    raise Exit()
