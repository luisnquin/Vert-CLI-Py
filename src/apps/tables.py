from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
import typer

from utils.utils import print_error, print_success, isUsingSQL
from constants.constants import queries_path
from db.sql.conn import DbConnection
from db.sql.models import Tables


tables: object = typer.Typer()
console: object = Console()


@tables.command()
def get():
    """
    vert tables get
    """
    if isUsingSQL():
        conn: object = DbConnection()
        query = Tables.get()
        tables = conn.execute(query, get=True)

        table: object = Table(box=SQUARE)
        table.add_column('Tables')
        for row in tables:
            table.add_row(f'- {row[0]}')

        console.print(table)
        raise typer.Exit()

    print_error('You\'re not using SQL')
    raise typer.Exit(code=1)


@tables.command()
def rebuild():
    """
    vert tables rebuild
    """
    if isUsingSQL():
        conn: object = DbConnection()
        queries: list[str] = Tables.drop_and_create(queries_path)

        with typer.progressbar(queries) as items:
            for query in items:
                flag: str = conn.execute(query)
                if flag[-2:] != 'd!':
                    print_error(flag)
                    raise typer.Exit(code=1)

        conn.close()
        print_success('Rebuilt table schema!')
        raise typer.Exit()

    print_error('You\'re not using SQL')
    raise typer.Exit(code=1)
