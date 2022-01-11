from typing import Union
import typer

from utils.utils import get_config, overwrite_config, check_and_fix_path
from utils.utils import print_success, print_warning


__version__: str = 'v0.8.0'
core: object = typer.Typer()


@core.command()
def version():
    """
    vert core version
    """
    print_success(f'Welcome!\n\nVert CLI: {__version__}')
    raise typer.Exit()


@core.command()
def config_workspace(path: str = typer.Option(..., prompt=True, help='Path example -> /home/luisnquin/workspace')):
    config: dict = get_config('./config.json')
    fixed_path: Union[str, bool] = check_and_fix_path(path)
    if fixed_path == False:
        print_warning('The workspace path was not correct')
        raise typer.Abort()

    config['path'] = fixed_path
    overwrite_config(config, './config.json')
    print_success('The workspace path was changed successfully!')


@core.command()
def config_dbconn(database: str = typer.Option(..., prompt=True), user: str = typer.Option(..., prompt=True),
                  password: str = typer.Option(..., prompt=True, hide_input=True), host: str = typer.Option('localhost', prompt=True),
                  port: int = typer.Option(5432, prompt=True)):

    c: dict = get_config('./config.json')
    c['database'], c['user'], c['password'], c['host'], c['port'] = database, user, password, host, port
    overwrite_config(c, './config.json')
    # Pending -> ping
    print_success('The database configuration was changed successfully!')


@core.command()
def configcli(path: str = typer.Option(..., prompt='Workspace path'), database: str = typer.Option(..., prompt=True),
              user: str = typer.Option(..., prompt=True), password: str = typer.Option(..., prompt=True, hide_input=True),
              host: str = typer.Option('localhost', prompt=True), port: int = typer.Option(5432, prompt=True)):

    c: dict = get_config('./config.json')
    fixed_path: Union[str, bool] = check_and_fix_path(path)
    if fixed_path == False:
        print_warning(
            'The workspace path was not correct, type -> vert core first-command')
        raise typer.Abort()

    c['path'], c['database'], c['user'], c['password'], c['host'], c['port'] = fixed_path, database, user, password, host, port
    overwrite_config(c, './config.json')
    # Pending -> ping
    print_success('Your configuration is valid!')
