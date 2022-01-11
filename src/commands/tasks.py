from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
from typing import Union
import typer

from db.conn import DbConnection
from db.models import Categories, Tasks
from utils.utils import print_prompt, print_error, print_warning


tasks: object = typer.Typer()
console: object = Console()


@tasks.command()
def get():
    """
    vert tasks get
    """
    conn: object = DbConnection()
    query: str = Tasks.get()
    rows: Union[tuple[tuple[any]], str] = conn.execute(query=query, get=True)
    if type(rows) == str:
        print_error(rows)
        raise typer.Exit(code=1)

    table: object = Table(box=SQUARE)
    table.add_column('ID')
    table.add_column('Name')
    table.add_column('Category')
    table.add_column('Status')
    table.add_column('Datetime')
    for row in rows:
        table.add_row(row[0], row[1], row[2], row[3], row[4])

    console.print(table)
    raise typer.Exit()


@tasks.command()
def add(name: str = typer.Option(..., prompt='Task name'), category: str = typer.Option(..., prompt='Task category')):
    """
    vert tasks add
    """
    conn: object = DbConnection()
    flag: bool = conn.exists(Categories.exists(category))

    if flag != True:
        print_error('The category does not exists!\n')
        print_prompt('Check -> vert showcategories')
        raise typer.Abort()

    query = Tasks(name=name, category=category, status=0).add()
    typer.echo(conn.execute(query=query))
    raise typer.Exit()


@tasks.command()
def update_status(id: int = typer.Argument(...), status: int = typer.Option(..., '--status')):
    """
    vert tasks update-status <id> --status <0 or 1>
    """
    if status not in [0, 1]:
        print_warning('No changes, your status need to be zero or one')
        raise typer.Exit(code=1)

    conn: object = DbConnection()
    query: str = Tasks(id=id, status=status).update_status()
    typer.echo(conn.execute(query=query))
    raise typer.Exit()


@tasks.command()
def update_category(id: int = typer.Argument(...), category: str = typer.Option(..., '--category')):
    """
    vert task update-category <id> --category <category-name>
    """
    conn: object = DbConnection()
    flag: str = conn.exists(Categories.exists(category=category))
    if flag:
        query: str = Tasks(id=id, category=category).update_category()
        typer.echo(conn.execute(query=query))
        raise typer.Exit()

    print_warning("The category doesn't exist in <categories-table>")
    print_prompt('Check -> vert showcategories')
    raise typer.Exit(code=1)


@tasks.command()
def remove(id: int = typer.Argument(...)):
    """
    vert task remove <task-id>
    """
    conn: object = DbConnection()
    query: str = Tasks(id=id).delete()
    typer.echo(conn.execute(query=query))
    raise typer.Exit()


@tasks.command()
def clean():
    """
    vert task clean
    """
    conn: object = DbConnection()
    query: str = Tasks.clean()
    typer.echo(conn.execute(query=query))
    raise typer.Exit()
