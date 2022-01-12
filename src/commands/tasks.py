from inquirer import prompt, List
from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
from typing import Union
import typer

from utils.utils import print_error, data_proccessing
from db.models import Categories, Tasks
from db.conn import DbConnection


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
        table.add_row(str(row[0]), row[1], row[2], row[3], row[4])

    console.print(table)
    raise typer.Exit()


@tasks.command()
def add(name: str = typer.Option(..., prompt='Task name')):
    """
    vert tasks add
    """
    conn: object = DbConnection()
    query: str = Categories.get()
    categories: Union[tuple[str], str] = conn.execute(query, get=True)

    if type(categories) == str:
        print_error(categories)
        raise typer.Exit(code=1)

    answer: Union[dict, None] = \
        prompt([List(name='categories', message='Select a category',
               choices=[c[0] for c in categories])])

    name: str = data_proccessing(name)
    query: str = \
        Tasks(name=name, category=answer.get('categories'), status=0).add()

    typer.echo(conn.execute(query=query))
    conn.close()
    raise typer.Exit()


@tasks.command()
def update(id: int = typer.Argument(...), action: str = typer.Option(..., prompt='Status or category[s/c]')):
    if action == 's':
        conn: object = DbConnection()
        answer: Union[dict, None] = \
            prompt([List(name='status', message='Choose an status', choices=[0, 1])])

        query: str = Tasks(id=id, status=answer['status']).update_status()
        typer.echo(conn.execute(query=query))
        conn.close()
        raise typer.Exit()

    elif action == 'c':
        conn: object = DbConnection()
        categories: tuple[str] = conn.execute(query=Categories.get(), get=True)
        answer: Union[dict, None] = \
            prompt([List('categories', message='Choose an category',
                   choises=[c[0] for c in categories])])

        query: str = \
            Tasks(id=id, categories=answer.get('categories')).update_category()

        typer.echo(conn.execute(query=query))
        conn.close()
        raise typer.Exit()


@tasks.command()
def remove(id: int = typer.Argument(...)):
    """
    vert task remove <task-id>
    """
    conn: object = DbConnection()
    query: str = Tasks(id=id).delete()
    typer.echo(conn.execute(query=query))
    conn.close()
    raise typer.Exit()


@tasks.command()
def clean():
    """
    vert task clean
    """
    conn: object = DbConnection()
    query: str = Tasks.clean()
    typer.echo(conn.execute(query=query))
    conn.close()
    raise typer.Exit()
