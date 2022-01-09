from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
import typer

from db.conn import DbConnection
from db.schemas import *
from db.models import *


app = typer.Typer()
console = Console()
__version__ = 'v0.3.0'


@app.command()
def version():
    typer.echo(f'VertCLI: {__version__}')


@app.command()
def get(tablename: str):
    """
    Just brind me a table from the connected database
    """

    conn = DbConnection()
    if tablename in ['tasks', 'Tasks']:
        rows = conn.execute(Task.get(), get=True)
        table = Table(title="Tasks", box=SQUARE)
        table.add_column('ID')
        table.add_column('Name')
        table.add_column('Category')
        table.add_column('Status')
        table.add_column('Datetime')
        for row in rows:
            table.add_row(str(row[0]), row[1], row[2], row[3], row[4][:-7])

        console.print(table)
        return
        
    else:
        rows = conn.execute(f'SELECT * FROM {tablename};', get=True)
        if type(rows) == str:
            typer.echo(rows)

        if tablename in ['status', 'Status']:
            table = Table(title=tablename.capitalize(), box=SQUARE)

            table.add_column('ID')
            table.add_column('Symbol')
            for row in rows:
                table.add_row(str(row[0]), row[1])

            console.print(table)
            return

        elif tablename in ['categories', 'Categories']:
            table = Table(title=tablename.capitalize(), box=SQUARE)

            table.add_column('ID')
            table.add_column('Symbol')
            for row in rows:
                table.add_row(str(row[0]), row[1])

            console.print(table)
            return
        
        for row in rows:
            typer.echo(row)


@app.command()
def addTask(
        name: str = typer.Option(
            None, prompt='Give me the Task name'
        ),
        category: str = typer.Option(
            None, prompt='Give me the category name'
        ),
        status: int = typer.Option(None, prompt='Status?[0/1]')):
    """
    Just type: vert addtask
    """

    conn = DbConnection()
    flag = conn.exists(Category.exists(category))

    if flag != True:
        typer.echo('The category does not exists!')
        typer.Exit()
        return

    if status not in [0, 1]:
        typer.echo('Bad status')
        typer.Exit()
        return

    sentence = Task(TaskSchema(name=name, category=category, status=status))\
        .add()

    typer.echo(conn.execute(query=sentence))


@app.command()
def updateTaskStatus(id: int = typer.Argument(None), status: int = typer.Option(None, '--status')):
    conn = DbConnection()
    sentence = Task(TaskSchema(id=id, status=status)).updateStatus()

    typer.echo(conn.execute(query=sentence))


@app.command()
def deleteTask(id: int = typer.Argument(None)):
    """
    Just type: vert deletetask <task-id>
    """
    conn = DbConnection()
    if id:
        sentence = Task(TaskSchema(id=id)).delete()
        typer.echo(conn.execute(query=sentence))
        return

    typer.echo('Nothing to do, well')


if __name__ == "__main__":
    app()
