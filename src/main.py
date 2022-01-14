from apps.categories import category
from apps.notifier import notifier
from apps.tables import tables
from apps.tasks import tasks
from apps.ideas import ideas
from apps.core import core
from apps.urls import urls
from apps.gen import gen

from typer import Typer


app: object = Typer()


app.add_typer(category, name='categories')
app.add_typer(notifier, name='notifier')
app.add_typer(tables, name='tables')
app.add_typer(tasks, name='tasks')
app.add_typer(ideas, name='ideas')
app.add_typer(core, name='core')
app.add_typer(urls, name='urls')
app.add_typer(gen, name='gen')


if __name__ == "__main__":
    app()
