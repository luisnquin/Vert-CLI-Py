from typer import Typer, Argument, Option, Exit
from rich.console import Console
from rich.table import Table
from rich.box import SQUARE

from utils.utils import date_format
from db.models import Ideas

ideas: object = Typer()
console: object = Console()


@ideas.command()
def get():
    """
    vert ideas get
    """
    table: object = Table(box=SQUARE)
    table.add_column('ID')
    table.add_column('Name')
    table.add_column('Date', justify='center')

    rows: tuple[tuple] = Ideas.get()
    for row in rows:
        table.add_row(str(row[0]), row[1], date_format(row[2]))

    console.print(table)
    raise Exit()


@ideas.command()
def add(name: str = Option(..., prompt='Idea')):
    """
    vert ideas add
    """

    Ideas(name=name).add()
    raise Exit()


@ideas.command()
def remove(ids: list[int] = Argument(...)):
    """
    vert ideas remove <id's...>
    """

    Ideas(ids=ids).delete()
    raise Exit()
