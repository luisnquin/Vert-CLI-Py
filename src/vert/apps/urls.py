from typing import Union

from typer import Typer, Argument, Option, Exit
from rich.console import Console
from rich.table import Table
from rich.box import SQUARE

from utils.utils import html_title_extractor, date_format, print_warning
from db.models import Urls


urls: object = Typer()
console: object = Console()


@urls.command()
def get():
    """
    vert urls get
    """

    table: object = Table(box=SQUARE)
    table.add_column('ID')
    table.add_column('Title')
    table.add_column('URL')
    table.add_column('Date')

    rows: tuple[tuple] = Urls.get()
    for row in rows:
        table.add_row('%d' % (row[0]), row[1], row[2], date_format(row[3]))

    console.print(table)
    raise Exit()


@urls.command()
def add(url: str = Option(..., prompt=True)):
    """
    vert urls add

    Vert takes the title from your URL through web scraping,
    if you can't, an entry would be open for you
    """
    
    title: Union[str, bool] = html_title_extractor(url)
    if not title:
        print_warning('Title not found\n')
        title: Union[str, None] = input(
            'Still, do you want to add a title for your URL?[Leave it blank if not]: ') or None

    Urls(title=title, url=url).add()
    raise Exit()


@urls.command()
def remove(ids: list[int] = Argument(...)):
    """
    vert urls remove <id's...>
    """

    Urls(ids=ids).delete()
    raise Exit()
