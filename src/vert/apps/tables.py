from rich.console import Console
from typer import Typer, Exit
from rich.table import Table
from rich.box import SQUARE

from db.models import Tables


tables: object = Typer()
console: object = Console()


@tables.command()
def get():
    """
    vert tables get
    """

    table: object = Table(box=SQUARE)
    table.add_column('Tables')
    
    rows: tuple[tuple] = Tables.get()
    for row in rows:
        table.add_row(' > %s' % (row[0]))

    console.print(table)
    raise Exit()


@tables.command()
def rebuild():
    """
    vert tables rebuild
    """
    Tables.drop_and_create()
    raise Exit()
