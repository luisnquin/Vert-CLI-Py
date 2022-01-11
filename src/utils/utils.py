from io import TextIOWrapper
from json import load, dump
from typing import Union
from sys import platform
from os import getenv
from re import match

from typer import echo, style, colors


def print_error(error: str) -> None:
    echo(style(f'\nERROR: {error}', fg=colors.RED), err=True)


def print_fatal(error: str) -> None:
    echo(style(f'\nFATAL: {error}', fg=colors.RED,
         bg=colors.BRIGHT_WHITE), err=True)


def print_warning(msg: str) -> None:
    echo(style(f'\nWARNING: {msg}', fg=colors.MAGENTA))


def print_prompt(msg: str) -> None:
    echo(style(f'\n{msg}', fg=colors.BRIGHT_YELLOW))


def print_success(msg: str) -> None:
    echo(style(f'\n{msg}', fg=colors.BRIGHT_GREEN))


def get_config(path: str) -> dict:
    file: TextIOWrapper = open(path, 'r')
    content: dict = load(file)
    file.close()

    return content


def overwrite_config(content: dict, path: str) -> None:
    file: TextIOWrapper = open(path, 'w', encoding='UTF-8')
    dump(content, file, indent=4)
    file.close()


def alter_open(path: str, to_write: str) -> None:
    file: TextIOWrapper = open(path, 'w', encoding='UTF-8')
    file.write(to_write)
    file.close()


# I don't know the pattern of Mac, so, this
def check_and_fix_path(path: str) -> Union[str, bool]:
    if platform == 'linux' or platform == 'linux2':
        if bool(match(r'[~](\/\w+)+', path)):
            path: str = path[1:]
            path: str = getenv('HOME') + path

        elif bool(match(r'home\/\w+\/', path)):
            if path[0] != '/':
                path: str = '/' + path

            if path.find(getenv('HOME'), 0) != 0:
                return False

        return path

    elif platform == 'win32':
        if bool(match(r'[A-z]:([\\]?[\/]?\w+)+', path)):
            if path[-1] == '/' or path[-1] == '\\':
                path: str = path[:-1]

            return path

    return path


if __name__ == '__main__':
    pass
