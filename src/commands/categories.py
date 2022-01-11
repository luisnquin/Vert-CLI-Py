from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
from typing import Union
import typer

from db.conn import DbConnection
from db.models import Categories
from utils.utils import print_error


category: object = typer.Typer()
console: object = Console()


@category.command()
def get():
    """
    vert categories get
    """
    conn: object = DbConnection()
    query: str = Categories.get()
    rows: Union[tuple[tuple[any]], str] = conn.execute(query, get=True)

    if type(rows) == str:
        print_error(rows)
        raise typer.Exit(code=1)

    table: object = Table(box=SQUARE)
    table.add_column('Categories')
    for row in rows:
        table.add_row(f'- {row[0]}')

    console.print(table)

    raise typer.Exit()


@category.command()
def add(name: str = typer.Option(..., prompt='Name of the new category')):
    """
    vert categories add
    """
    conn: object = DbConnection()
    query: str = Categories(name=name).add()
    typer.echo(conn.execute(query))
    raise typer.Exit()


@category.command()
def remove(id: int = typer.Argument(...)):
    """
    vert categories remove <id>
    """
    conn: object = DbConnection()
    query: str = Categories(id).delete()
    typer.echo(conn.execute(query))
    raise typer.Exit()
