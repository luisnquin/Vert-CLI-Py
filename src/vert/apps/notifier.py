from datetime import datetime

from typer import Typer, Argument, Option, Exit
from rich.console import Console
from rich.table import Table
from rich.box import SQUARE

from utils.utils import print_error, time_format
from db.models import Routines


notifier: object = Typer()
console: object = Console()


@notifier.command()
def get():
    """
    vert notifier get
    """

    table: object = Table(box=SQUARE)
    table.add_column('ID')
    table.add_column('Title')
    table.add_column('Message', justify='center')
    table.add_column('Hour')

    rows: tuple[tuple] = Routines.get()
    for row in rows:
        table.add_row('%d' % (row[0]), row[1], row[2], time_format(row[3]))

    console.print(table)
    raise Exit()


@notifier.command()
def add(title: str = Option(..., prompt=True), message: str = Option(None, prompt=True),
        hour: int = Option(..., prompt=True), minute: int = Option(..., prompt=True)):
    """
    vert notifier add
    """
    try:
        time_stamp: datetime = datetime.now().replace(hour=hour, minute=minute)
    except Exception as error:
        print_error(error)

    Routines(title=title, message=message, dt=time_stamp).add()
    raise Exit()


@notifier.command()
def remove(ids: list[int] = Argument(...)):
    """
    vert notifier remove <id's...>
    """
    Routines(ids=ids).delete()
    raise Exit()
