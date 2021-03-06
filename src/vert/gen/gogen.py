from pathlib import Path
from sys import platform
from os import system
from re import search

from typer import Abort

from utils.utils import open_and_write, print_warning, print_error, user_config


def go_project(name: str) -> str:
    PATH: str = user_config('path', 'workspace')

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
    open_and_write(f'{PATH}/{name}/.gitignore', '.env')

    Path(f'{PATH}/{name}/src').mkdir()
    Path(f'{PATH}/{name}/src/requests').mkdir()
    system(f'git init {PATH}/{name}')
    Path(f'{PATH}/{name}/src/main.go').touch()
    open_and_write(f'{PATH}/{name}/src/main.go', 'package main')

    Path(f'{PATH}/{name}/src/models').mkdir()
    Path(f'{PATH}/{name}/src/models/models.go').touch()
    open_and_write(f'{PATH}/{name}/src/models/models.go', 'package models')

    Path(f'{PATH}/{name}/src/certificates').mkdir()
    Path(f'{PATH}/{name}/src/certificates/certificates.go').touch()
    open_and_write(
        f'{PATH}/{name}/src/certificates/certificates.go', 'package certificates')

    Path(f'{PATH}/{name}/src/utils').mkdir()
    Path(f'{PATH}/{name}/src/utils/utils.go').touch()
    open_and_write(f'{PATH}/{name}/src/utils/utils.go', 'package utils')

    Path(f'{PATH}/{name}/src/db').mkdir()
    Path(f'{PATH}/{name}/src/db/db.go').touch()
    open_and_write(f'{PATH}/{name}/src/db/db.go', 'package db')

    Path(f'{PATH}/{name}/src/middleware').mkdir()
    Path(f'{PATH}/{name}/src/middleware/middleware.go').touch()
    open_and_write(
        f'{PATH}/{name}/src/middleware/middleware.go', 'package middleware')

    Path(f'{PATH}/{name}/src/controllers').mkdir()
    Path(f'{PATH}/{name}/src/controllers/controllers.go').touch()
    open_and_write(
        f'{PATH}/{name}/src/controllers/controllers.go', 'package controllers')

    Path(f'{PATH}/{name}/src/routers').mkdir()
    Path(f'{PATH}/{name}/src/routers/routers.go').touch()
    open_and_write(f'{PATH}/{name}/src/routers/routers.go', 'package routers')

    if platform == 'linux' or platform == 'linux2':
        system('clear')

    return f'{PATH}/{name}'


if __name__ == '__main__':
    pass
