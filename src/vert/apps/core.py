from base64 import b64encode
from typing import Union

from typer import Typer, Argument, Option, Exit, prompt as typer_prompt
from inquirer import List, prompt as inquirer_prompt

from utils.utils import print_success, print_warning, print_error, check_and_fix_path, user_config
from utils.utils import run_tasker_process, reload_tasker_process, kill_tasker_process
from db.models import Database

__version__: str = 'v2.0.0'
core: object = Typer()


@core.command()
def version():
    """
    vert core version
    """
    print_success('Vert CLI: %s\n\nWelcome!' % (__version__))
    raise Exit()


@core.command()
def ping():
    """
    vert core ping
    """

    Database.ping()
    print_success('The ping to the database was successful')
    raise Exit()


@core.command()
def config():
    """
    The short command that joins your database connection
    settings and your workspace settings
    """
    options: tuple[str] = (
        'Configure database connection(PostgreSQL)',
        'Configure workspace',
        'Exit'
    )

    answer: dict = inquirer_prompt(
        [List(name='action', message='Choose one', choices=options)])

    if answer['action'] == options[0]:
        database: str = typer_prompt(text='Database name')
        user: str = typer_prompt(text='Username')
        password: str = typer_prompt(text='Password', hide_input=True)
        host: str = typer_prompt(text='Host', default='localhost')
        port: int = typer_prompt(text='Port', default=5432)

        dsn: bytes = 'dbname=%s user=%s password=%s host=%s port=%s'\
            % (database, user, password, host, port).encode('ascii')

        user_config('database', 'dsn', b64encode(dsn).decode('ascii'), write=True)
        Database.ping()
        print_success('The ping to the database was successful')

    elif answer['action'] == options[1]:
        path: str = typer_prompt(text='Path')
        fixed_path: Union[str, bool] = check_and_fix_path(path)

        if not fixed_path:
            print_warning('The workspace path was not correct, no changes')
        else:
            user_config('path', 'workspace', fixed_path, write=True)
            print_success('Workspace path, modified\n')

    else:
        print('Goodbye!')
        raise Exit()

    config()


@core.command()
def tasker():
    """
    This command makes the topic of routines make sense
    """
    options: tuple[str] = (
        'Start process',
        'Reload process',
        'Kill process',
        'Exit'
    )

    answer: dict = inquirer_prompt(
        [List(name='action', choices=options, message='Tasker')])

    if answer['action'] == options[0]:
        run_tasker_process()
        print_success('Now tasker is running')
        raise Exit()

    elif answer['action'] == options[1]:
        reload_tasker_process()
        print_success('Tasker process was reloaded')
        raise Exit()

    elif answer['action'] == options[2]:
        kill_tasker_process()
        print_success('Tasker process was killed')
        raise Exit()

    else:
        print('Goodbye!')
        raise Exit()
