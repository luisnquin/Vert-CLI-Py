from os import getenv, getppid, kill, system
from configparser import ConfigParser
from typing import Union, Optional
from psutil import process_iter
from datetime import datetime
from subprocess import Popen
from signal import SIGHUP
from pathlib import Path
from sys import platform
from re import match

from typer import Abort, echo, style
from inquirer import prompt, List
from urllib.request import urlopen
from bs4 import BeautifulSoup
from appdirs import AppDirs


def print_error(error: str) -> None:
    echo(style(f'\nERROR:\n%s' % (error), fg='red'), err=True)


def print_fatal(error: str) -> None:
    echo(style(f'\nFATAL:\n%s' % (error), fg='red', bg='bright_white'), err=True)


def print_warning(msg: str) -> None:
    echo(style(f'\nWARNING:\n%s' % (msg), fg='magenta'))


def print_prompt(msg: str) -> None:
    echo(style(f'\n%s' % (msg), fg='bright_yellow'))


def print_success(msg: str) -> None:
    echo(style(f'\n%s' % (msg), fg='bright_green'))


def open_and_write(path: str, content: str) -> None:
    with open(path, 'w', encoding='UTF-8') as file:
        file.write(content)


def check_and_fix_path(path: str) -> Union[str, bool]:
    path_copy: str = path
    if platform == 'linux' or platform == 'linux2':
        if bool(match(r'[~](\/\w+)+', path)):
            path: str = path[1:]
            path: str = getenv('HOME') + path

        elif bool(match(r'home\/\w+\/', path)):
            if path[0] != '/':
                path: str = '/' + path

            if path.find(getenv('HOME'), 0) != 0:
                return False

    if Path(path).exists():
        return path

    return path_copy


def open_vscode(path: str) -> None:
    options: tuple[str] = (
        'Nothing',
        'Close terminal and open it in VSCode',
        'Open VSCode'
    )

    answer: dict\
        = prompt([List(name='action', message="What do you want to do with the project?", choices=options)])

    if answer['action'] == options[1]:
        system(f'code {path}')
        kill(getppid(), SIGHUP)

    elif answer['action'] == options[2]:
        system(f'code {path}')


def check_and_put_singlequotes(value: str) -> str:
    if value is not None:
        if value.find('\'') != -1:
            value: str = value.replace('\'', '\'\'')

    return value


def reload_tasker_process() -> None:
    pid: int = int(user_config('processes', 'tasker'))
    for proc in process_iter():
        if proc.pid == pid:
            proc.kill()
            try:
                user_config(
                    section='processes',
                    option='tasker',
                    element='%d' % Popen(['/usr/sbin/vert/tasker']).pid,
                    write=True
                )
                return

            except Exception as error:
                print_fatal(error)

    print_warning('Tasker process was not found')
    raise Abort()


def run_tasker_process() -> None:
    pid: int = int(user_config('processes', 'tasker'))
    for proc in process_iter():
        if proc.pid == pid:
            print_warning('Is already running, make more process would target your performance')
            raise Abort()
    try:
        user_config(
            section='processes',
            option='tasker',
            element='%d' % Popen(['/usr/sbin/vert/tasker']).pid,
            write=True
        )
        return

    except Exception as error:
        print_fatal(error)


def kill_tasker_process() -> None:
    pid: int = int(user_config('processes', 'tasker'))
    for proc in process_iter():
        if proc.pid == pid:
            proc.kill()
            return

    print_warning('Tasker process was not found')
    raise Abort()


def html_title_extractor(url: str) -> Union[str, bool]:
    try:
        soup = BeautifulSoup(urlopen(url), features='html5lib')
        return soup.title.get_text()
    except Exception as _:
        return False


def user_config(section: str, option: str, element: Optional[str] = None, write: Optional[bool] = False) -> Union[str, None]:
    config: object = ConfigParser()
    appdir: object = AppDirs()
    appdir.appname = 'vert'
    ini_file: str = '%s/config.ini' % (appdir.user_config_dir)

    if Path(appdir.user_config_dir).exists() and Path(ini_file).exists():
        config.read(ini_file)
        if not write:
            return config[section][option]

        if section not in config.sections():
            config.add_section(section)

        if element and option:
            config.set(section, option, element)
            with open(ini_file, 'w', encoding='UTF-8') as file:
                config.write(file)

    else:
        if not Path(appdir.user_config_dir).exists():
            Path(appdir.user_config_dir).mkdir()

        Path(ini_file).touch()
        config.read(appdir.user_config_dir)
        config.add_section('database')
        config.set('database', 'dsn',
                   'dbname=<> user=<> password=<> host=<> port=<>')

        config.add_section('path')
        config.set('path', 'workspace', '/home/user/path/to/workspace')

        with open(ini_file, 'w', encoding='UTF-8') as file:
            config.write(file)

        config(section, option, element, write)


def date_format(dt: Union[datetime, str]) -> str:
    if type(dt) is str:
        return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f').strftime('%B %m, %Y')

    return dt.strftime('%B %m, %Y')


def time_format(dt: Union[datetime, str]) -> str:
    if type(dt) is str:
        return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f').strftime('%H:%M')

    return dt.strftime('%H:%M')


if __name__ == '__main__':
    pass
