from os import getenv, system, kill, getppid
from timeago import format as dt_format
from urllib.request import urlopen
from psutil import process_iter
from bs4 import BeautifulSoup
from datetime import datetime
from subprocess import Popen
from io import TextIOWrapper
from json import load, dump
from signal import SIGHUP
from typing import Union
from sys import platform
from re import match

from typer import echo, style, Exit
from inquirer import prompt, List
from typing import Union

from constants.constants import config_path, src_path


def print_error(error: str) -> None:
    echo(style(f'\nERROR:\n{error}', fg='red'), err=True)


def print_fatal(error: str) -> None:
    echo(style(f'\nFATAL:\n{error}',
               fg='red', bg='bright_white'), err=True)


def print_warning(msg: str) -> None:
    echo(style(f'\nWARNING:\n{msg}', fg='magenta'))


def print_prompt(msg: str) -> None:
    echo(style(f'\n{msg}', fg='bright_yellow'))


def print_success(msg: str) -> None:
    echo(style(f'\n{msg}', fg='bright_green'))


def get_json(path: str) -> dict:
    try:
        file: TextIOWrapper = open(path, 'r')
        content: dict = load(file)
        file.close()
        return content

    except Exception as error:
        print_error(error)
        raise Exit(code=1)


def isUsingSQL() -> bool:
    try:
        file: TextIOWrapper = open(config_path, 'r')
        config: dict = load(file)
        file.close()
        return config['isUsingSQL']

    except Exception as error:
        print_error(error)
        raise Exit(code=1)


def overwrite_json(json: dict, path: str) -> None:
    try:
        file: TextIOWrapper = open(path, 'w', encoding='UTF-8')
        dump(json, file, indent=4)
        file.close()
        return

    except Exception as error:
        print_error(error)
        raise Exit(code=1)


def alter_open(path: str, to_write: str) -> None:
    file: TextIOWrapper = open(path, 'w', encoding='UTF-8')
    file.write(to_write)
    file.close()
    return


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

            if path.find('/') != -1:
                path: str = path.replace('/', '\\')

            return path

        return False

    return path


def open_vscode_or_not(path: str = ...) -> None:
    options: list[str] = \
        ['Nothing', 'Close terminal and open in VSCode', 'Open VSCode']

    answer: Union[dict, None] \
        = prompt([List('action', message="What do you want to do with the project?", choices=options)])

    if answer['action'] == options[1]:
        system(f'code {path}')
        kill(getppid(), SIGHUP)
        return

    if answer['action'] == options[2]:
        system(f'code {path}')
        return


def prepare_sql_value(value: str) -> str:
    if value.find('\'') != -1:
        value: str = value.replace('\'', '\'\'')

    return value


def is_tasker_active() -> bool:
    for proc in process_iter():
        if proc.name() == 'tasker' or proc.name() == 'tasker.exe':
            return True

    return False


def run_tasker_process(path: str) -> None:
    Popen([path, "-abs-path", src_path])


def kill_tasker_process() -> None:
    for proc in process_iter():
        if proc.name() == 'tasker' or proc.name() == 'tasker.exe':
            proc.kill()
            return


def html_title_extractor(url: str) -> Union[str, bool]:
    try:
        soup = BeautifulSoup(urlopen(url), features='html5lib')
        return soup.title.get_text()

    except Exception as error:
        if error:
            return False


def relative_dt(dt: str) -> str:
    return dt_format(datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f'), now=datetime.now())


if __name__ == '__main__':
    pass
