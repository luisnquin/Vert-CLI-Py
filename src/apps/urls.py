from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
from typing import Union
import typer

from utils.utils import relative_dt, html_title_extractor, isUsingSQL, prepare_sql_value
from utils.utils import print_success, print_error, print_warning
from db.json.models import Urls as UrlsJSON
from db.sql.models import Urls as UrlsSQL
from db.sql.conn import DbConnection


urls: object = typer.Typer()
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
    table.add_column('Relative time')
    table.add_column('Date')

    if isUsingSQL():
        conn: object = DbConnection()
        query: str = UrlsSQL.get()
        rows: Union[tuple[tuple[Union[str, int]]], str] =\
            conn.execute(query, get=True)
        conn.close()

        if type(rows) == str:
            print_error(rows)
            raise typer.Exit(code=1)

        for row in rows:
            table.add_row(str(row[0]), row[1], row[2],
                          relative_dt(row[3]), row[3][:10])
    else:
        for value in UrlsJSON.get():
            table.add_row(str(value['id']), value['title'], value['url'], relative_dt(
                value['datetime']), value['datetime'][:10])

    console.print(table)
    raise typer.Exit()


@urls.command()
def add(url: str = typer.Option(..., prompt='URL')):
    """
    vert urls add

    Vert takes the title from your URL through web scraping,
    if you can't, an entry would be open for you
    """
    title: Union[str, bool] = html_title_extractor(url)
    if title == False:
        print_warning('Title not found\n')
        title: Union[str, None] \
            = input('Still, do you want to add a title for your URL?[Leave it blank if not]: ') or None

    if isUsingSQL():
        conn: object = DbConnection()
        if type(title) == str:
            title: str = prepare_sql_value(value=title)

        query: str = UrlsSQL(title=title, url=url).add()
        typer.echo(conn.execute(query))
        conn.close()
        raise typer.Exit()

    print_success(UrlsJSON(title=title, url=url).add())
    raise typer.Exit()


@urls.command()
def remove(id: int = typer.Argument(...)):
    """
    vert urls remove <url-id>
    """
    if isUsingSQL():
        conn: object = DbConnection()
        query: str = UrlsSQL(id=id).remove()

        typer.echo(conn.execute(query))
        conn.close()
        raise typer.Exit()

    print_success(UrlsJSON(id=id).remove())
    raise typer.Exit()
