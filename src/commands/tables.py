from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
import typer

from constants.constants import queries_path
from utils.utils import print_success
from db.conn import DbConnection
from db.models import Tables


tables: object = typer.Typer()
console: object = Console()


@tables.command()
def get():
    """
    vert tables show
    """
    conn: object = DbConnection()
    query = Tables.get()
    tables = conn.execute(query, get=True)

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
    queries: list[str] = Tables.migrate(queries_path)
    for query in queries:
        if query[:4] == 'DROP' or query[:6] == 'INSERT':
            continue
        conn.execute(query)

    conn.close()
    print_success('Migrations carried out!')
    raise typer.Exit()


@tables.command()
def dropandmigrate():
    """
    vert tables dropandmigrate
    """
    conn: object = DbConnection()
    queries: list[str] = Tables.drop_and_create(queries_path)
    for query in queries:
        conn.execute(query)

    conn.close()
    print_success('Rebuilt table schema!')
    raise typer.Exit()
