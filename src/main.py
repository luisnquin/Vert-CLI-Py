from db.conn import DbConnection
from db.schemas import *
from db.models import *
import typer


app = typer.Typer()
__version__ = 'v0.0.2'


@app.command()
def version():
    typer.echo(f'VertCLI: {__version__}')


@app.command()
def get(tablename: str):
    """
    Just brind me a table from the connected database
    """
    conn = DbConnection()
    rows = conn.execute(f'SELECT * FROM {tablename};', get=True)
    if type(rows) == str:
        typer.echo(rows)
    else:
        for row in rows:
            typer.echo(row)


@app.command()
def addTask(
        name: str = typer.Option(None, prompt='Give me the Task name'),
        description: str = typer.Option(None, prompt='Give the task description(Optional)')):
    """
    Just type: vert addtask
    """
    conn = DbConnection()
    if description:
        sentence = Task(TaskSchema(name=name, description=description)).add()
    else:
        sentence = Task(TaskSchema(name=name)).add()

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
