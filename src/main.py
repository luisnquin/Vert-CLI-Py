from getpass import getpass

from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
import typer

from utils import overwriteconfigJSON, printError, printWarning, printSpecial, overwriteconfigJSON, getconfigJSON
from gen.gogen import GenerateGoProject
from gen.pygen import GeneratePyProject
from db.conn import DbConnection
from db.models import *


app = typer.Typer()
console = Console()
__version__ = 'v0.5.1'


@app.command()
def version():
    """
    vert version
    """
    printSpecial(f'\nWelcome!\n\nVert CLI: {__version__}')


@app.command()
def showmytables():
    """
    vert showmytables
    """
    typer.echo('\nTables:\n - categories\n - tasks\n - ideas')


@app.command()
def migrate():
    """
    vert migrate | Just if you broke something
    """
    pass


@app.command()
def get(tablename: str):
    """
    vert get <tablename> | To see all -> vert showmytables
    """

    conn = DbConnection()
    if tablename in ['tasks', 'Tasks']:
        rows = conn.execute(TaskTable.get(), get=True)
        if type(rows) == str:
            printError(rows)
            return

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
            printError(rows)
            return

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

            console.print(table)

        for row in rows:
            typer.echo(row)


@app.command()
def addTask(name: str = typer.Option(None, prompt='Task name'),
            category: str = typer.Option(None, prompt='Task category')):
    """
    vert addtask
    """

    conn = DbConnection()
    flag = conn.exists(CategoryTable.exists(category))

    if flag != True:
        printError('The category does not exists!')
        typer.echo('\n\nPrompt:\n type vert get categories')
        typer.Exit()
        return

    query = TaskTable(name=name, category=category, status=0).add()
    typer.echo(conn.execute(query=query))
    return


@app.command()
def addCategory(name: str = typer.Argument(None)):
    """
    vert addcategory <category-name>
    """
    if name:
        conn = DbConnection()
        query = CategoryTable(name=name).add()
        typer.echo(conn.execute(query))
        return

    printWarning('Nothing to do, well')


@app.command()
def addIdea(name: str = typer.Option(None, prompt='Idea')):
    """
    vert addidea
    """
    conn = DbConnection()
    query = IdeaTable(name=name)
    typer.echo(conn.execute(query))


@app.command()
def updateTaskStatus(id: int = typer.Argument(None), status: int = typer.Option(None, '--status')):
    """
    vert updatetaskstatus <id> --status <status[0 | 1]>
    """

    if status:
        conn = DbConnection()
        query = TaskTable(id=id, status=status).updateStatus()
        typer.echo(conn.execute(query=query))

    printWarning('No changes, your forgot to enter --status <argument>')


@app.command()
def updateTaskCategory(id: int = typer.Argument(None), category: str = typer.Option(None, '--category')):
    """
    vert updatetaskcategory <id> --category <category-name>
    """

    if category:
        conn = DbConnection()
        flag = conn.exists(CategoryTable.exists(category=category))
        if flag:
            query = TaskTable(id=id, category=category)
            typer.echo(conn.execute(query=query))
            return

        printWarning("The category doesn't exist in <categories-table>")
        return
    printWarning('No changes, your forgot to enter --category <argument>')


@app.command()
def cleanTasks():
    """
    vert cleantasks
    """
    conn = DbConnection()
    query = TaskTable.clean()
    typer.echo(conn.execute(query=query))


@app.command()
def deleteTask(id: int = typer.Argument(None)):
    """
    vert deletetask <task-id>
    """
    if id:
        conn = DbConnection()
        query = TaskTable(id=id).delete()
        typer.echo(conn.execute(query=query))
        return

    printWarning('Nothing to do, well')


@app.command()
def deleteCategory(id: int = typer.Argument(None)):
    """
    vert deletecategory <category-id>
    """
    if id:
        conn = DbConnection()
        query = CategoryTable(id).delete()
        typer.echo(conn.execute(query))
        return

    printWarning('Nothing to do, well')


@app.command()
def deleteIdea(id: int = typer.Argument(None)):
    """
    vert deleteidea <idea-id>
    """
    if id:
        conn = DbConnection()
        query = IdeaTable(id).delete()
        typer.echo(conn.execute(query=query))
        return

    printWarning('Nothing to do, well')


@app.command()
def newgoproject(project_name=typer.Option(None, prompt='Project name')):
    """
    vert newgoproject | Config -> vert configcli
    """
    GenerateGoProject(project_name)


@app.command()
def newpyproject(project_name=typer.Option(None, prompt='Project name')):
    """
    vert newpyproject | Config -> vert configcli
    """
    GeneratePyProject(project_name)


@app.command()
def configcli(
        configurePath: bool = typer.Option(False, prompt='Edit workspace?'),
        configureDBConnection: bool = typer.Option(False, prompt='Edit DB config?')):
    """
    vert configcli
    """
    config = getconfigJSON('./config.json')
    print()
    if configurePath:
        path = input(
            'New workspace path(Example: /home/luisnquin/workspace/tests): ')
        config['path'] = path

    if configureDBConnection:
        dbname, dbuser, dbpwd = input('Database: '), input('User: '), getpass('Password: ')
        dbhost, dbport = input('Host: '), input('Port: ')

        config['dbname'], config['dbuser'], config['dbpwd'] = dbname, dbuser, dbpwd
        config['dbhost'], config['dbport'] = dbhost, dbport

    overwriteconfigJSON(config, './config.json')
    printSpecial('\nSuccess!')


if __name__ == "__main__":
    app()
