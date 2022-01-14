from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
from typing import Union
import typer

from utils.utils import print_success, print_error, relative_dt, isUsingSQL, prepare_sql_value
from db.json.models import Ideas as IdeasJSON
from db.sql.models import Ideas as IdeasSQL
from db.sql.conn import DbConnection


ideas: object = typer.Typer()
console: object = Console()


@ideas.command()
def get():
    """
    vert ideas get
    """
    table: object = Table(box=SQUARE)
    table.add_column('ID')
    table.add_column('Name')
    table.add_column('Relative time')
    table.add_column('Date', justify='center')

    if isUsingSQL():
        conn: object = DbConnection()
        query: str = IdeasSQL.get()
        rows: Union[tuple[tuple[any]], str] = conn.execute(
            query=query, get=True)
        conn.close()

        if type(rows) == str:
            print_error(rows)
            raise typer.Exit(code=1)

        for row in rows:
            table\
                .add_row(str(row[0]), row[1], relative_dt(row[2]), row[2][:10])

        console.print(table)
        raise typer.Exit()

    rows: list[dict] = IdeasJSON.get()

    for row in rows:
        table\
            .add_row(str(row['id']), row['name'], relative_dt(row['datetime']), row['datetime'][:10])

    console.print(table)
    raise typer.Exit()


@ideas.command()
def add(name: str = typer.Option(..., prompt='Idea')):
    """
    vert ideas add
    """
    if isUsingSQL():
        conn: object = DbConnection()
        name: str = prepare_sql_value(name)
        query: str = IdeasSQL(name=name).add()
        typer.echo(conn.execute(query))
        conn.close()
        raise typer.Exit()
    
    print_success(IdeasJSON(name=name).add())
    raise typer.Exit()


@ideas.command()
def remove(id: int = typer.Argument(...)):
    """
    vert ideas delete <idea-id>
    """
    if isUsingSQL():
        conn: object = DbConnection()
        query: str = IdeasSQL(id).delete()
        typer.echo(conn.execute(query=query))
        conn.close()
        raise typer.Exit()

    print_success(IdeasJSON(id=id).remove())
