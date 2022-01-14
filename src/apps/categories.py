from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
from typing import Union
import typer

from utils.utils import print_error, print_success, isUsingSQL, prepare_sql_value
from db.json.models import Categories as CategoriesJSON
from db.sql.models import Categories as CategoriesSQL
from db.sql.conn import DbConnection


category: object = typer.Typer()
console: object = Console()


@category.command()
def get():
    """
    vert categories get
    """
    table: object = Table(box=SQUARE)
    table.add_column('ID', justify='center')
    table.add_column('Categories')
    if isUsingSQL():
        conn: object = DbConnection()
        query: str = CategoriesSQL.get()
        rows: Union[tuple[tuple[any]], str] = conn.execute(query, get=True)
        conn.close()

        if type(rows) == str:
            print_error(rows)
            raise typer.Exit(code=1)

        for row in rows:
            table.add_row(str(row[0]), row[1])

        console.print(table)
        raise typer.Exit()

    for row in CategoriesJSON.get():
        table.add_row(str(row['id']), row['name'])

    console.print(table)
    raise typer.Exit()


@category.command()
def add(name: str = typer.Option(..., prompt='Name of the new category')):
    """
    vert categories add
    """
    if isUsingSQL():
        conn: object = DbConnection()
        name: str = prepare_sql_value(name)
        query: str = CategoriesSQL(name=name).add()
        typer.echo(conn.execute(query))
        conn.close()
        raise typer.Exit()

    print_success(CategoriesJSON(name=name).add())
    raise typer.Exit()


@category.command()
def remove(id: int = typer.Argument(...)):
    """
    vert categories remove <category-id>
    """
    if isUsingSQL():
        conn: object = DbConnection()
        query: str = CategoriesSQL(id).delete()
        typer.echo(conn.execute(query))
        conn.close()
        raise typer.Exit()

    print_success(CategoriesJSON(id=id).remove())
    raise typer.Exit()
