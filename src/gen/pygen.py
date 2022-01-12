from time import sleep
from pathlib import Path
from sys import platform
from os import system
from re import search

from typer import Abort

from utils.utils import alter_open, get_config, print_warning, print_error


PATH: str = get_config('./config.json')['path']


def gen_py_project(name: str) -> str:
    if search("\s", name) is not None:
        print_warning('No spaces. It would create two directories')
        raise Abort()

    try:
        Path(f'{PATH}/{name}').mkdir()
    except Exception as error:
        print_error(error)
        raise Abort()

    Path(f'{PATH}/{name}/.env').touch()
    Path(f'{PATH}/{name}/.env.example').touch()
    Path(f'{PATH}/{name}/.gitignore').touch()
    alter_open(f'{PATH}/{name}/.gitignore', '.env')

    Path(f'{PATH}/{name}/src').mkdir()
    system(f'git init {PATH}/{name}')
    system(f'virtualenv {PATH}/{name}/venv')
    sleep(5)
    if platform == 'linux' or platform == 'linux2':
        system(f'source {PATH}/{name}/venv/bin/activate.csh')
    elif platform == 'win32':
        system(f'./{PATH}/{name}/venv/scripts/activate')

    Path(f'{PATH}/{name}/src/main.py').touch()

    Path(f'{PATH}/{name}/src/schemas').mkdir()
    Path(f'{PATH}/{name}/src/schemas/schemas.py').touch()
    Path(f'{PATH}/{name}/src/schemas/__init__.py').touch()

    Path(f'{PATH}/{name}/src/utils').mkdir()
    Path(f'{PATH}/{name}/src/utils/utils.py').touch()
    Path(f'{PATH}/{name}/src/utils/__init__.py').touch()

    if platform == 'linux' or platform == 'linux2':
        system('clear')
    elif platform == 'win32':
        system('cls')

    return f'{PATH}/{name}'


if __name__ == '__main__':
    pass
