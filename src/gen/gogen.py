from pathlib import Path
from sys import platform
from os import system
from re import search

from typer import Abort

from utils.utils import alter_open, get_config, print_warning, print_error


PATH: str = get_config('./config.json')['path']


def gen_go_project(name: str) -> str:
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
    Path(f'{PATH}/{name}/src/requests').mkdir()
    system(f'git init {PATH}/{name}')
    Path(f'{PATH}/{name}/src/main.go').touch()
    alter_open(f'{PATH}/{name}/src/main.go', 'package main')

    Path(f'{PATH}/{name}/src/models').mkdir()
    Path(f'{PATH}/{name}/src/models/models.go').touch()
    alter_open(f'{PATH}/{name}/src/models/models.go', 'package models')

    Path(f'{PATH}/{name}/src/certificates').mkdir()
    Path(f'{PATH}/{name}/src/certificates/certificates.go').touch()
    alter_open(
        f'{PATH}/{name}/src/certificates/certificates.go', 'package certificates')

    Path(f'{PATH}/{name}/src/utils').mkdir()
    Path(f'{PATH}/{name}/src/utils/utils.go').touch()
    alter_open(f'{PATH}/{name}/src/utils/utils.go', 'package utils')

    Path(f'{PATH}/{name}/src/db').mkdir()
    Path(f'{PATH}/{name}/src/db/db.go').touch()
    alter_open(f'{PATH}/{name}/src/db/db.go', 'package db')

    Path(f'{PATH}/{name}/src/middleware').mkdir()
    Path(f'{PATH}/{name}/src/middleware/middleware.go').touch()
    alter_open(
        f'{PATH}/{name}/src/middleware/middleware.go', 'package middleware')

    Path(f'{PATH}/{name}/src/controllers').mkdir()
    Path(f'{PATH}/{name}/src/controllers/controllers.go').touch()
    alter_open(
        f'{PATH}/{name}/src/controllers/controllers.go', 'package controllers')

    Path(f'{PATH}/{name}/src/routers').mkdir()
    Path(f'{PATH}/{name}/src/routers/routers.go').touch()
    alter_open(f'{PATH}/{name}/src/routers/routers.go', 'package routers')

    if platform == 'linux' or platform == 'linux2':
        system('clear')
    elif platform == 'win32':
        system('cls')

    return f'{PATH}/{name}'


if __name__ == '__main__':
    pass
