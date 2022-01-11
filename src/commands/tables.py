from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
import typer

from db.conn import DbConnection
from utils.utils import print_success


tables: object = typer.Typer()
console: object = Console()


@tables.command()
def show():
    """
    vert tables show
    """
    conn: object = DbConnection()
    tables: tuple = conn.get_tables()

    table: object = Table(box=SQUARE)
    table.add_column('Tables')
    for row in tables:
        table.add_row(f'- {row[0]}')

    console.print(table)
    raise typer.Exit()


@tables.command()
def migrate():
    """
    vert tables migrate
    """
    conn: object = DbConnection()
    print_success(conn.migrate('./../db/db.sql'))


@tables.command()
def dropandmigrate():
    """
    vert tables dropandmigrate
    """
    conn: object = DbConnection()
    print_success(conn.drop_and_create('./../db/db.sql'))
