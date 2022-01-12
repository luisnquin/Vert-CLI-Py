from typing import Union
import typer

from utils.utils import get_config, is_tasker_active, overwrite_config, check_and_fix_path, print_error, run_tasker_process
from utils.utils import print_success, print_warning, kill_tasker_process
from constants.constants import config_path, tasker_path
from db.conn import DbConnection

__version__: str = 'v0.9.0'
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
    pong: int = DbConnection.ping()
    if pong != 1:
        print_error('There was no response from the database')
        raise typer.Exit()

    print_success('Success!')
    raise typer.Exit()


@core.command()
def start_tasker():
    isActive: bool = is_tasker_active()
    if isActive:
        print_warning('Is already running, make more process would target your performance')
        raise typer.Exit(code=1)

    run_tasker_process(tasker_path)
    print_success('Tasker is running')
    raise typer.Exit()


@core.command()
def reload_tasker():
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
    isActive: bool = is_tasker_active()
    if isActive:
        kill_tasker_process()
        print_success('Tasker process was killed')
        raise typer.Exit()

    print_error('Tasker process was not found')
    raise typer.Exit(code=1)


@core.command()
def config_workspace(path: str = typer.Option(..., prompt=True, help='Path example -> /home/luisnquin/workspace')):
    config: dict = get_config('./config.json')
    fixed_path: Union[str, bool] = check_and_fix_path(path)
    if fixed_path == False:
        print_warning('The workspace path was not correct')
        raise typer.Abort()

    config['path'] = fixed_path
    overwrite_config(config, config_path)
    print_success('The workspace path was changed successfully!')


@core.command()
def config_dbconn(database: str = typer.Option(..., prompt=True), user: str = typer.Option(..., prompt=True),
                  password: str = typer.Option(..., prompt=True, hide_input=True), host: str = typer.Option('localhost', prompt=True),
                  port: int = typer.Option(5432, prompt=True)):

    c: dict = get_config(config_path)
    c['database'], c['user'], c['password'], c['host'], c['port'] = database, user, password, host, port
    overwrite_config(c, config_path)

    pong: int = DbConnection.ping()
    if pong != 1:
        print_error('There was no response from the database')
        raise typer.Exit()

    print_success('There was a successful response from the database!')
    raise typer.Exit()


@core.command()
def configcli(path: str = typer.Option(..., prompt='Workspace path'), database: str = typer.Option(..., prompt=True),
              user: str = typer.Option(..., prompt=True), password: str = typer.Option(..., prompt=True, hide_input=True),
              host: str = typer.Option('localhost', prompt=True), port: int = typer.Option(5432, prompt=True)):

    c: dict = get_config(config_path)
    fixed_path: Union[str, bool] = check_and_fix_path(path)
    if fixed_path == False:
        print_warning('The workspace path was not correct')
        raise typer.Abort()

    c['path'], c['database'], c['user'], c['password'], c['host'], c['port'] = fixed_path, database, user, password, host, port
    overwrite_config(c, config_path)
    pong: int = DbConnection.ping()
    if pong != 1:
        print_error('There was no response from the database')
        raise typer.Exit()

    print_success('There was a successful response from the database')
    raise typer.Exit()
