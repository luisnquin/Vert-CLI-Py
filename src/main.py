from db.conn import DbConnection
from db.schemas import *
from db.models import *
import typer


app = typer.Typer()
__version__ = 'v0.2.0'


@app.command()
def version():
    typer.echo(f'VertCLI: {__version__}')


@app.command()
def get(tablename: str):
    """
    Just brind me a table from the connected database
    """

    conn = DbConnection()
    if tablename == 'tasks':
        rows = conn.execute(Task.get(), get=True)
    else:
        rows = conn.execute(f'SELECT * FROM {tablename};', get=True)

    if type(rows) == str:
        typer.echo(rows)
    else:
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
    flag = conn.category_exists(category)

    if flag != True:
        typer.echo('The category does not exists!')
        typer.Exit()
        return

    if status not in [0, 1]:
        typer.echo('Bad status')
        typer.Exit()
        return

    sentence = Task(TaskSchema(
        name=name, category=category, status=status)).add()

    typer.echo(conn.execute(sentence=sentence))


@app.command()
def updateTaskStatus(id: int = typer.Argument(None), status: int = typer.Option(None, '--status')):
    conn = DbConnection()
    sentence = Task(TaskSchema(id=id, status=status)).updateStatus()

    typer.echo(conn.execute(sentence=sentence))


@app.command()
def deleteTask(id: int = typer.Argument(None)):
    """
    Just type: vert deletetask <task-id>
    """
    conn = DbConnection()
    if id:
        sentence = Task(TaskSchema(id=id)).delete()
        typer.echo(conn.execute(sentence=sentence))
        return

    typer.echo('Nothing to do, well')


if __name__ == "__main__":
    app()
