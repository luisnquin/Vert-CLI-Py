from pathlib import Path
from os import system
from re import search

from typer import Abort

from utils.utils import alternativeOpen, getconfigJSON, printWarning


PATH: str = getconfigJSON('./config.json')['path']


def GeneratePyProject(name: str) -> None:
    if search("\s", name) is not None:
        printWarning('No spaces, please, It would create two directories')
        raise Abort()

    Path(f'{PATH}/{name}').mkdir()
    Path(f'{PATH}/{name}/.env').touch()
    Path(f'{PATH}/{name}/.env.example').touch()
    Path(f'{PATH}/{name}/.gitignore').touch()
    alternativeOpen(f'{PATH}/{name}/.gitignore', '.env')

    Path(f'{PATH}/{name}/src').mkdir()
    system(f'git init {PATH}/{name}')
    Path(f'{PATH}/{name}/src/main.py').touch()

    Path(f'{PATH}/{name}/src/schemas').mkdir()
    Path(f'{PATH}/{name}/src/schemas/schemas.py').touch()
    Path(f'{PATH}/{name}/src/schemas/__init__.py').touch()

    Path(f'{PATH}/{name}/src/utils').mkdir()
    Path(f'{PATH}/{name}/src/utils/utils.py').touch()
    Path(f'{PATH}/{name}/src/utils/__init__.py').touch()
    system(f'virtualenv {PATH}/{name}/venv')


if __name__ == '__main__':
    pass
