from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
import typer

from db.conn import DbConnection
from db.models import *
from gen.gogen import GenerateGoProject
from gen.pygen import GeneratePyProject


app = typer.Typer()
console = Console()
__version__ = 'v0.5.0'


@app.command()
def version():
    typer.echo(f'Welcome!\n\nVert CLI: {__version__}')


@app.command()
def get(tablename: str):
    """
    Just brind me a table from the connected database
    """

    conn = DbConnection()
    if tablename in ['tasks', 'Tasks']:
        rows = conn.execute(TaskTable.get(), get=True)
        table = Table(title="Tasks", box=SQUARE)
        table.add_column('ID', justify='center')
        table.add_column('Name', justify='center')
        table.add_column('Category', justify='center')
        table.add_column('Status', justify='center')
        table.add_column('Datetime', justify='center')
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
            table.add_column('ID', justify='center')
            table.add_column('Symbol', justify='center')
            for row in rows:
                table.add_row(str(row[0]), row[1])

            console.print(table)
            return

        if tablename in ['categories', 'Categories']:
            table = Table(title=tablename.capitalize(), box=SQUARE)
            table.add_column('ID', justify='center')
            table.add_column('Category', justify='center')
            for row in rows:
                table.add_row(str(row[0]), row[1])

            console.print(table)
            return

        if tablename in ['Ideas', 'ideas']:
            table = Table(title=tablename.capitalize(), box=SQUARE)
            table.add_column('ID', justify='center')
            table.add_column('Name', justify='center')
            table.add_column('Datetime', justify='center')
            for row in rows:
                table.add_row(str(row[0]), row[1], row[2])

        for row in rows:
            typer.echo(row)


@app.command()
def addTask(name: str = typer.Option(
            None, prompt='Give me the Task name'
            ),
            category: str = typer.Option(
            None, prompt='Give me the category name'
            )):
    """
    Just type: vert addtask
    """

    conn = DbConnection()
    flag = conn.exists(CategoryTable.exists(category))

    if flag != True:
        typer.echo('The category does not exists!')
        typer.Exit()
        return

    if name and category:
        query = TaskTable(name=name, category=category, status=0).add()
        typer.echo(conn.execute(query=query))
        return

    typer.echo("You probably didn't enter the name or the category, so, nothing")


@app.command()
def addCategory(name: str = typer.Argument(None)):
    if name:
        conn = DbConnection()
        query = CategoryTable(name=name).add()
        typer.echo(conn.execute(query))
        return

    typer.echo('Nothing to do, well')


@app.command()
def addIdea(name: str = typer.Option(None, prompt='Give me your idea')):
    conn = DbConnection()
    query = IdeaTable(name=name)
    typer.echo(conn.execute(query))


@app.command()
def updateTaskStatus(id: int = typer.Argument(None), status: int = typer.Option(None, '--status')):
    conn = DbConnection()
    query = TaskTable(id=id, status=status).updateStatus()

    typer.echo(conn.execute(query=query))


@app.command()
def updateTaskCategory(id: int = typer.Argument(None), category: str = typer.Option(None, '--category')):
    conn = DbConnection()
    flag = conn.exists(CategoryTable.exists(category=category))
    if flag:
        query = TaskTable(id=id, category=category)
        typer.echo(conn.execute(query=query))
        return

    typer.echo("The category doesn't exist in -> Categories table")


@app.command()
def cleanTasks():
    conn = DbConnection()
    query = TaskTable.clean()
    typer.echo(conn.execute(query=query))


@app.command()
def deleteTask(id: int = typer.Argument(None)):
    """
    Just type: vert deletetask <task-id>
    """
    conn = DbConnection()
    if id:
        query = TaskTable(id=id).delete()
        typer.echo(conn.execute(query=query))
        return

    typer.echo('Nothing to do, well')


@app.command()
def deleteCategory(id: int = typer.Argument(None)):
    if id:
        conn = DbConnection()
        query = CategoryTable(id).delete()
        typer.echo(conn.execute(query))


@app.command()
def deleteIdea(id: int = typer.Argument(None)):
    conn = DbConnection()
    if id:
        query = IdeaTable(id).delete()
        typer.echo(conn.execute(query=query))
        return

    typer.echo('Nothing to do, well')


@app.command()
def newgoproject(project_name=typer.Option(
        None, prompt='Give me the name of your new Go project')):
    """
    If you want to configurate the path to your workspace, type
    """
    GenerateGoProject(project_name)


@app.command()
def newpyproject(project_name=typer.Option(
        None, prompt='Give me the name of your new Py project')):
    """
    If you want to configurate the path to your workspace, type
    """
    GeneratePyProject(project_name)


if __name__ == "__main__":
    app()
