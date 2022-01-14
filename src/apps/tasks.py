from inquirer import prompt, List
from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
from typing import Union
import typer

from utils.utils import relative_dt, isUsingSQL, prepare_sql_value
from utils.utils import print_error, print_success

from db.sql.models import Categories as CategoriesSQL, Tasks as TasksSQL
from db.json.models import Categories as CategoriesJSON, Tasks as TasksJSON
from db.sql.conn import DbConnection



tasks: object = typer.Typer()
console: object = Console()


@tasks.command()
def get():
    """
    vert tasks get
    """
    table: object = Table(box=SQUARE)
    table.add_column('ID')
    table.add_column('Name')
    table.add_column('Category')
    table.add_column('Status', justify='center')
    table.add_column('Relative time')
    table.add_column('Date')
    if isUsingSQL():
        conn: object = DbConnection()
        query: str = TasksSQL.get()
        rows: Union[tuple[tuple[Union[str, int]]],
                    str] = conn.execute(query=query, get=True)
        if type(rows) == str:
            print_error(rows)
            raise typer.Exit(code=1)

        for row in rows:
            table.add_row(str(row[0]), row[1], row[2],
                          str(row[3]), relative_dt(row[4]), row[4][:10])

        console.print(table)
        raise typer.Exit()

    for row in TasksJSON.get():
        table.add_row(str(row['id']), row['name'], row['category'],
                      str(row['status']), relative_dt(row['datetime']), row['datetime'][:10])

    console.print(table)
    raise typer.Exit()


@tasks.command()
def add(name: str = typer.Option(..., prompt='Task name')):
    """
    vert tasks add
    """
    if isUsingSQL():
        conn: object = DbConnection()
        query: str = CategoriesSQL.get()
        categories: Union[tuple[str], str] = conn.execute(query, get=True)

        if type(categories) == str:
            print_error(categories)
            raise typer.Exit(code=1)

        answer: Union[dict, None] = \
            prompt([List(name='categories', message='Select a category',
                         choices=[c[1] for c in categories])])

        name: str = prepare_sql_value(name)
        query: str = \
            TasksSQL(name=name, category=answer['categories'], status=0).add()

        typer.echo(conn.execute(query=query))
        conn.close()
        raise typer.Exit()

    categories: list[str] = \
        [category['name'] for category in CategoriesJSON.get()]

    answer: Union[dict, None] = \
        prompt(
            [List(name='categories', message='Select a category', choices=categories)])

    print_success(TasksJSON(name=name, category=answer['categories']).add())
    raise typer.Exit()


@tasks.command()
def update(id: int = typer.Argument(...)):
    """
    vert tasks update <task-id>

    Update the status of a task
    """
    answer: Union[dict, None] = \
        prompt([List(name='status', message='Choose an status', choices=[0, 1])])

    if isUsingSQL():
        conn: object = DbConnection()

        query: str = \
            TasksSQL(id=id, status=answer['status']).update_status()
        typer.echo(conn.execute(query=query))
        conn.close()
        raise typer.Exit()
    
    print_success(TasksJSON(id=id, status=answer['status']).update_status())
    raise typer.Exit()


@tasks.command()
def remove(id: int = typer.Argument(...)):
    """
    vert task remove <task-id>
    """
    if isUsingSQL():
        conn: object = DbConnection()
        query: str = TasksSQL(id=id).delete()
        typer.echo(conn.execute(query=query))
        conn.close()
        raise typer.Exit()

    print_success(TasksJSON(id=id).remove())
    raise typer.Exit()


@tasks.command()
def clean():
    """
    vert task clean

    If the status of the task is marked as completed,
    then the task will be deleted
    """
    if isUsingSQL():
        conn: object = DbConnection()
        query: str = TasksSQL.clean()
        typer.echo(conn.execute(query=query))
        conn.close()
        raise typer.Exit()

    print_success(TasksJSON.clean())
