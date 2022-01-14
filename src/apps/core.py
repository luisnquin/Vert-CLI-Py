from os.path import isfile

from inquirer import List, prompt
from typing import Union
import typer

from utils.utils import get_json, overwrite_json, check_and_fix_path, is_tasker_active, run_tasker_process
from utils.utils import print_success, print_warning, print_error, isUsingSQL, kill_tasker_process
from constants.constants import config_path, tasker_path, json_db_path
from db.sql.conn import DbConnection

__version__: str = 'v1.0.0'
core: object = typer.Typer()


@core.command()
def version():
    """
    vert core version
    """
    print_success(f'Welcome!\n\nVert CLI: {__version__}')
    raise typer.Exit()


@core.command()
def ping():
    """
    Check your database connection or JSON file existence based on your configuration
    """
    if isUsingSQL():
        pong: int = DbConnection.ping()
        if pong != 1:
            print_error('There was no response from the database')
            raise typer.Exit(code=1)

        print_success('Successful response from the database')
        raise typer.Exit()

    if isfile(json_db_path):
        print_success('Data persistence check in JSON was successful')
        raise typer.Exit()

    print_warning(
        'Well, your data persistence in JSON doesn\' was found. So, start to use SQL, I guess')
    raise typer.Exit(code=1)


@core.command()
def change_persistence():
    """
    Choose between PostgreSQL and JSON, PostgreSQL for a better performance
    """
    options: list[str] = ['PostgreSQL', 'JSON']
    answer: Union[dict, None] = \
        prompt([List(name='persistence', message='Select a category', choices=options)])

    config: dict[any] = get_json(config_path)
    if answer['persistence'] == options[0]:
        config['isUsingSQL'] = True
    elif answer['persistence'] == options[1]:
        config['isUsingSQL'] = False

    overwrite_json(config, config_path)
    print_success('Now you\'re using {}'.format(answer['persistence']))
    raise typer.Exit()


@core.command()
def start_tasker():
    """
    This command makes the topic of routines make sense
    """
    isActive: bool = is_tasker_active()
    if isActive:
        print_warning(
            'Is already running, make more process would target your performance')
        raise typer.Exit(code=1)

    run_tasker_process(tasker_path)
    print_success('Tasker is running')
    raise typer.Exit()


@core.command()
def reload_tasker():
    """
    Weird use case but it still makes sense to have this
    """
    isActive: bool = is_tasker_active()
    if isActive:
        kill_tasker_process()
        run_tasker_process(tasker_path)
        print_success('Tasker process was reloaded')
        raise typer.Exit()

    print_error('Tasker process was not found')
    raise typer.Exit(code=1)


@core.command()
def kill_tasker():
    """
    To end the tasker process
    """
    isActive: bool = is_tasker_active()
    if isActive:
        kill_tasker_process()
        print_success('Tasker process was killed')
        raise typer.Exit()

    print_error('Tasker process was not found')
    raise typer.Exit(code=1)


@core.command()
def workspace_config(path: str = typer.Option(..., prompt=True)):
    """
    vert gen <set> 
    It works with an absolute path, so if you don't have 
    a set path, use this

    This works with an absolute path, by example:
    ~/workspace/projects
    or 
    /home/user/workspace/projects
    """
    config: dict = get_json(config_path)
    fixed_path: Union[str, bool] = check_and_fix_path(path)
    if fixed_path == False:
        print_warning('The workspace path was not correct')
        raise typer.Abort()

    config['path'] = fixed_path
    overwrite_json(config, config_path)
    print_success('The workspace path was changed successfully!')


@core.command()
def db_config(database: str = typer.Option(..., prompt=True), user: str = typer.Option(..., prompt=True),
                  password: str = typer.Option(..., prompt=True, hide_input=True), host: str = typer.Option('localhost', prompt=True),
                  port: int = typer.Option(5432, prompt=True)):
    """
    Don't configure this if you don't want to
    to use PostgreSQL as your data persistence mode
    """
    c: dict = get_json(config_path)
    c['dsn'] = 'dbname={} user={} password={} host={} port={}'\
        .format(database, user, password, host, port)

    overwrite_json(c, config_path)

    pong: int = DbConnection.ping()
    if pong != 1:
        print_error('There was no response from the database')
        raise typer.Exit()

    print_success('There was a successful response from the database!')
    raise typer.Exit()


@core.command()
def config(path: str = typer.Option(..., prompt='Workspace path'), database: str = typer.Option(..., prompt=True),
              user: str = typer.Option(..., prompt=True), password: str = typer.Option(..., prompt=True, hide_input=True),
              host: str = typer.Option('localhost', prompt=True), port: int = typer.Option(5432, prompt=True)):
    """
    The short command that joins your database connection
    settings and your workspace settings
    """
    c: dict = get_json(config_path)
    fixed_path: Union[str, bool] = check_and_fix_path(path)
    if fixed_path == False:
        print_warning('The workspace path was not correct')
        raise typer.Abort()

    c['dsn'] = 'dbname={} user={} password={} host={} port={}'\
        .format(database, user, password, host, port)

    overwrite_json(c, config_path)
    pong: int = DbConnection.ping()
    if pong != 1:
        print_error('There was no response from the database')
        raise typer.Exit(code=1)

    print_success('There was a successful response from the database')
    raise typer.Exit()
