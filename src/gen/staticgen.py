from pathlib import Path
from os import system
from re import search

from typer import Abort

from utils.utils import alter_open, get_config, print_error, print_warning


PATH: str = get_config('./config.json')['path']


def gen_static_project(name: str) -> None:
    if search('\s', name) is not None:
        print_warning('No spaces. It would create two directories')
        raise Abort()

    try:
        Path(f'{PATH}/{name}').mkdir()
    except Exception as error:
        print_error(error)
        raise Abort()

    Path(f'{PATH}/{name}/.gitignore').touch()
    system(f'git init {PATH}/{name}')
    Path(f'{PATH}/{name}/src').mkdir()
    Path(f'{PATH}/{name}/src/index.html').touch()
    Path(f'{PATH}/{name}/src/tsconfig.json').touch()
    alter_open(f'{PATH}/{name}/src/tsconfig.json', """{
  "compilerOptions": {
    "target": "ES6",
    "useDefineForClassFields": true,
    "strict": true,
    "sourceMap": true,
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "noEmit": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true
  },
  "include": ["./src"]
}""")

    Path(f'{PATH}/{name}/src/ts').mkdir()
    Path(f'{PATH}/{name}/src/ts/main.ts').touch()
    Path(f'{PATH}/{name}/src/ts/modules').mkdir()
    Path(f'{PATH}/{name}/src/ts/utils').mkdir()

    Path(f'{PATH}/{name}/src/js').mkdir()
    Path(f'{PATH}/{name}/src/js/main.js').touch()
    Path(f'{PATH}/{name}/src/js/modules').mkdir()
    Path(f'{PATH}/{name}/src/js/utils').mkdir()

    Path(f'{PATH}/{name}/src/assets').mkdir()
    Path(f'{PATH}/{name}/src/assets/img').mkdir()
    Path(f'{PATH}/{name}/src/assets/fonts').mkdir()

    Path(f'{PATH}/{name}/src/css').mkdir()
    Path(f'{PATH}/{name}/src/css/styles.css').touch()
    Path(f'{PATH}/{name}/src/scss').mkdir()
    Path(f'{PATH}/{name}/src/scss/styles.scss').touch()
    Path(f'{PATH}/{name}/src/scss/_variables.scss').touch()
    Path(f'{PATH}/{name}/src/scss/_mixins.scss').touch()


if __name__ == '__main__':
    pass
