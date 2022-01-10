from typing import Union

from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
import typer

from gen.gogen import GenerateGoProject
from gen.pygen import GeneratePyProject
from db.conn import DbConnection
from utils.utils import *
from db.models import *


app: object = typer.Typer()
console: object = Console()
__version__: str = 'v0.6.0'


@app.command()
def version():
    """
    vert version
    """
    printSuccess(f'\nWelcome!\n\nVert CLI: {__version__}')
    raise typer.Exit()


@app.command()
def showmytables():
    """
    vert showmytables
    """
    typer.echo('\nTables:\n - categories\n - tasks\n - ideas')
    raise typer.Exit()


@app.command()
def showcategories():
    conn: object = DbConnection()
    rows = conn.execute('SELECT name FROM categories', get=True)
    typer.echo('\nCategories:\n')
    for row in rows:
        typer.echo(row[0])

    raise typer.Exit()


@app.command()
def migrate():
    """
    vert migrate | Just if you broke something
    """
    pass


@app.command()
def dropandmigrate():
    pass


@app.command()
def get(tablename: str = typer.Argument(...)):
    """
    vert get <tablename> | To see all -> vert showmytables
    """

    conn: object = DbConnection()
    if tablename in ['tasks', 'Tasks']:
        rows: Union[tuple, str] = conn.execute(TaskTable.get(), get=True)
        if type(rows) == str:
            printFatal(rows)
            printSuggestion(' > Check your CLI config -> vert configdbconn')
            printSuggestion(
                ' > If you broke the database -> vert dropandmigrate')
            raise typer.Exit(code=1)

        table = Table(title="Tasks", box=SQUARE)
        table.add_column('ID', justify='center')
        table.add_column('Name', justify='center')
        table.add_column('Category', justify='center')
        table.add_column('Status', justify='center')
        table.add_column('Datetime', justify='center')
        for row in rows:
            table.add_row(str(row[0]), row[1], row[2], row[3], row[4][:-7])

        console.print(table)
        raise typer.Exit()

    else:
        rows = conn.execute(f'SELECT * FROM {tablename};', get=True)
        if type(rows) == str:
            printError(rows)
            printSuggestion(' > Check your CLI config -> vert configdbconn')
            printSuggestion(
                ' > If you broke the database -> vert dropandmigrate')
            raise typer.Exit(code=1)

        if tablename in ['status', 'Status']:
            table = Table(title=tablename.capitalize(), box=SQUARE)
            table.add_column('ID', justify='center')
            table.add_column('Symbol', justify='center')
            for row in rows:
                table.add_row(str(row[0]), row[1])

            console.print(table)
            raise typer.Exit()

        if tablename in ['categories', 'Categories']:
            table = Table(title=tablename.capitalize(), box=SQUARE)
            table.add_column('ID', justify='center')
            table.add_column('Category', justify='center')
            for row in rows:
                table.add_row(str(row[0]), row[1])

            console.print(table)
            raise typer.Exit()

        if tablename in ['Ideas', 'ideas']:
            table = Table(title=tablename.capitalize(), box=SQUARE)
            table.add_column('ID', justify='center')
            table.add_column('Name', justify='center')
            table.add_column('Datetime', justify='center')
            for row in rows:
                table.add_row(str(row[0]), row[1], row[2])

            console.print(table)
            raise typer.Exit()

        for row in rows:
            typer.echo(row)
            raise typer.Exit()


@app.command()
def addTask(name: str = typer.Option(..., prompt='Task name'), category: str = typer.Option(..., prompt='Task category')):
    """
    vert addtask
    """

    conn = DbConnection()
    flag = conn.exists(CategoryTable.exists(category))

    if flag != True:
        printError('The category does not exists!\n')
        printSuggestion('Check -> vert showcategories')
        raise typer.Abort()

    query = TaskTable(name=name, category=category, status=0).add()
    typer.echo(conn.execute(query=query))
    raise typer.Exit()


@app.command()
def addCategory(name: str = typer.Option(..., prompt='Name of the new category')):
    """
    vert addcategory
    """
    conn = DbConnection()
    query = CategoryTable(name=name).add()
    typer.echo(conn.execute(query))
    raise typer.Exit()


@app.command()
def addIdea(name: str = typer.Option(..., prompt='Idea')):
    """
    vert addidea
    """
    conn = DbConnection()
    query = IdeaTable(name=name).add()
    typer.echo(conn.execute(query))
    raise typer.Exit()


@app.command()
def updateTaskStatus(id: int = typer.Argument(...), status: int = typer.Option(..., '--status')):
    """
    vert updatetaskstatus <task-id> --status <0 | 1>
    """

    if status not in [0, 1]:
        printWarning('No changes, your status need to be 0 or 1')
        raise typer.Exit(code=1)

    conn = DbConnection()
    query = TaskTable(id=id, status=status).updateStatus()
    typer.echo(conn.execute(query=query))
    raise typer.Exit()


@app.command()
def updateTaskCategory(id: int = typer.Argument(...), category: str = typer.Option(..., '--category')):
    """
    vert updatetaskcategory <id> --category <category-name>
    """

    conn = DbConnection()
    flag = conn.exists(CategoryTable.exists(category=category))
    if flag:
        query = TaskTable(id=id, category=category)
        typer.echo(conn.execute(query=query))
        raise typer.Exit()

    printWarning("The category doesn't exist in <categories-table>")
    printSuggestion('\nCheck -> vert showcategories')
    raise typer.Exit(code=1)


@app.command()
def cleanTasks():
    """
    vert cleantasks
    """
    conn = DbConnection()
    query = TaskTable.clean()
    typer.echo(conn.execute(query=query))
    raise typer.Exit()


@app.command()
def deleteTask(id: int = typer.Argument(...)):
    """
    vert deletetask <task-id>
    """
    conn = DbConnection()
    query = TaskTable(id=id).delete()
    typer.echo(conn.execute(query=query))
    raise typer.Exit()


@app.command()
def deleteCategory(id: int = typer.Argument(...)):
    """
    vert deletecategory <category-id>
    """
    conn = DbConnection()
    query = CategoryTable(id).delete()
    typer.echo(conn.execute(query))
    raise typer.Exit()


@app.command()
def deleteIdea(id: int = typer.Argument(...)):
    """
    vert deleteidea <idea-id>
    """
    conn = DbConnection()
    query = IdeaTable(id).delete()
    typer.echo(conn.execute(query=query))
    raise typer.Exit()


@app.command()
def newgoproject(project_name=typer.Option(..., prompt='Project name', help='A new Go project will be created in your workspace path')):
    """
    vert newgoproject | Config -> vert configworkspace
    """
    GenerateGoProject(project_name)
    raise typer.Exit()


@app.command()
def newpyproject(project_name=typer.Option(..., prompt='Project name', help='A new Python project will be created in your workspace path')):
    """
    vert newpyproject | Config -> vert configworkspace
    """
    GeneratePyProject(project_name)
    raise typer.Exit()


@app.command()
def configworkspace(path: str = typer.Option(..., prompt=True, help='Path example -> /home/luisnquin/workspace/tests')):
    config = getconfigJSON('./config.json')
    # regex
    config['path'] = path
    overwriteconfigJSON(config, './config.json')
    printSuccess('\nThe workspace path was changed successfully!')
    raise typer.Exit()


@app.command()
def configdbconn(database: str = typer.Option(..., prompt=True), user: str = typer.Option(..., prompt=True),
                 password: str = typer.Option(..., prompt=True, hide_input=True), host: str = typer.Option('localhost', prompt=True),
                 port: int = typer.Option(5432, prompt=True)):

    config = getconfigJSON('./config.json')
    # regex numbers and letters
    config['database'], config['user'], config['password'], config['host'], config['port'] = database, user, password, host, port
    overwriteconfigJSON(config, './config.json')
    printSuccess('\nThe database configuration was changed successfully!')
    raise typer.Exit()


if __name__ == "__main__":
    app()
