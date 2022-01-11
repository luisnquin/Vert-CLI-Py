from commands.categories import category
from commands.tables import tables
from commands.tasks import tasks
from commands.ideas import ideas
from commands.core import core
from commands.gen import gen

import typer

app: object = typer.Typer()


app.add_typer(category, name='categories')
app.add_typer(tables, name='tables')
app.add_typer(tasks, name='tasks')
app.add_typer(ideas, name='ideas')
app.add_typer(core, name='core')
app.add_typer(gen, name='gen')


if __name__ == "__main__":
    app()
