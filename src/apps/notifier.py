from datetime import time
from typing import Union

from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
import typer

from utils.utils import get_json, overwrite_json, print_success, print_warning, kill_tasker_process
from constants.constants import config_path


notifier: object = typer.Typer()
console: object = Console()


@notifier.command()
def get_routines():
    """
    vert notifier get-routines
    """
    routines: list = get_json(config_path)['notifier']
    table: object = Table(box=SQUARE)
    table.add_column('ID')
    table.add_column('Title')
    table.add_column('Message')
    table.add_column('Hour')
    for routine in routines:
        table.add_row(str(routine['id']), routine['title'],
                      routine['message'], routine['hour'])

    console.print(table)
    raise typer.Exit()


@notifier.command()
def add_routine(title: str = typer.Option(..., prompt=True), message: str = typer.Option('from VertCLI', prompt=True),
                hour: int = typer.Option(..., prompt=True), minute: int = typer.Option(..., prompt=True)):
    """
    vert notifier add-routine
    """
    hour: str = str(time(hour=hour, minute=minute))

    c: dict[Union[dict, list]] = get_json(config_path)

    routine: dict \
        = {"id": max({value['id'] for value in c['notifier']}) + 1, "title": title, "message": message, "hour": hour}

    c['notifier'].append(routine)
    overwrite_json(c, config_path)
    print_success('Task added successfully')
    kill_tasker_process()
    raise typer.Exit()


@notifier.command()
def remove_routine(id: int = typer.Argument(...)):
    """
    vert notifier remove-routine <routine-id>
    """
    c: dict = get_json(config_path)
    for i, routine in enumerate(c['notifier']):
        if routine['id'] == id:
            c['notifier'].pop(i)
            overwrite_json(c, config_path)
            print_success(
                f'The routine with the ID {id} was successfully removed')
            kill_tasker_process()
            raise typer.Exit()

    print_warning('There are no matches, so nothing was removed')
