from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
from typing import Union
import typer

from utils.utils import print_error
from db.conn import DbConnection
from db.models import Ideas


ideas: object = typer.Typer()
console: object = Console()


@ideas.command()
def get():
    """
    vert ideas get
    """
    conn: object = DbConnection()
    query: str = Ideas.get()
    rows: Union[tuple[tuple[any]], str] = conn.execute(query=query, get=True)
    if type(rows) == str:
        print_error(rows)
        raise typer.Exit(code=1)

    table: object = Table(box=SQUARE)
    table.add_column('ID')
    table.add_column('Name')
    table.add_column('Datetime')
    for row in rows:
        table.add_row(row[0], row[1], row[2])

    console.print(table)
    raise typer.Exit()


@ideas.command()
def add(name: str = typer.Option(..., prompt='Idea')):
    """
    vert ideas add
    """
    conn: object = DbConnection()
    query: str = Ideas(name=name).add()
    typer.echo(conn.execute(query))
    raise typer.Exit()


@ideas.command()
def remove(id: int = typer.Argument(...)):
    """
    vert ideas delete <id>
    """
    conn: object = DbConnection()
    query: str = Ideas(id).delete()
    typer.echo(conn.execute(query=query))
    raise typer.Exit()
