from os import getenv, system, kill, getppid
from psutil import process_iter
from subprocess import Popen
from io import TextIOWrapper
from json import load, dump
from signal import SIGHUP
from typing import Union
from sys import platform
from re import match

from typer import echo, style, colors
from inquirer import prompt, List
from typing import Union


def print_error(error: str) -> None:
    echo(style(f'\nERROR:\n{error}', fg=colors.RED), err=True)


def print_fatal(error: str) -> None:
    echo(style(f'\nFATAL:\n{error}', fg=colors.RED,
         bg=colors.BRIGHT_WHITE), err=True)


def print_warning(msg: str) -> None:
    echo(style(f'\nWARNING:\n{msg}', fg=colors.MAGENTA))


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


def open_vscode_or_not(path: str = ...) -> None:
    options: list[str] = \
        ['Nothing', 'Close terminal and open in VSCode', 'Open VSCode']

    answer: Union[dict, None] = prompt(
        [List('action', message="What do you want to do with the project?", choices=options)])

    if answer['action'] == options[1]:
        system(f'code {path}')
        kill(getppid(), SIGHUP)

    elif answer['action'] == options[2]:
        system(f'code {path}')


def data_proccessing(value: str) -> str:
    if value.find('\'') != -1:
        value: str = value.replace('\'', '\'\'')

    return value


def is_tasker_active() -> bool:
    for proc in process_iter():
        if proc.name() == 'tasker' or proc.name() == 'tasker.exe':
            return True

    return False


def run_tasker_process(path: str) -> None:
    Popen(path)


def kill_tasker_process() -> None:
    for proc in process_iter():
        if proc.name() == 'tasker' or proc.name() == 'tasker.exe':
            proc.kill()
            return


if __name__ == '__main__':
    pass
