from pathlib import Path
from os import system
from re import search

from typer import Abort

from utils.utils import alternativeOpen, getconfigJSON, printWarning


PATH: str = getconfigJSON('./config.json')['path']


def GenerateGoProject(name: str) -> None:
    if search("\s", name) is not None:
        printWarning('No spaces, please, It would create two directories')
        raise Abort()

    Path(f'{PATH}/{name}').mkdir()
    Path(f'{PATH}/{name}/.env').touch()
    Path(f'{PATH}/{name}/.env.example').touch()
    Path(f'{PATH}/{name}/.gitignore').touch()
    alternativeOpen(f'{PATH}/{name}/.gitignore', '.env')

    Path(f'{PATH}/{name}/src').mkdir()
    Path(f'{PATH}/{name}/src/requests').mkdir()
    system(f'git init {PATH}/{name}')
    Path(f'{PATH}/{name}/src/main.go').touch()
    alternativeOpen(f'{PATH}/{name}/src/main.go', 'package main')

    Path(f'{PATH}/{name}/src/models').mkdir()
    Path(f'{PATH}/{name}/src/models/models.go').touch()
    alternativeOpen(f'{PATH}/{name}/src/models/models.go', 'package models')

    Path(f'{PATH}/{name}/src/certificates').mkdir()
    Path(f'{PATH}/{name}/src/certificates/certificates.go').touch()
    alternativeOpen(
        f'{PATH}/{name}/src/certificates/certificates.go', 'package certificates')

    Path(f'{PATH}/{name}/src/utils').mkdir()
    Path(f'{PATH}/{name}/src/utils/utils.go').touch()
    alternativeOpen(f'{PATH}/{name}/src/utils/utils.go', 'package utils')

    Path(f'{PATH}/{name}/src/db').mkdir()
    Path(f'{PATH}/{name}/src/db/db.go').touch()
    alternativeOpen(f'{PATH}/{name}/src/db/db.go', 'package db')

    Path(f'{PATH}/{name}/src/middleware').mkdir()
    Path(f'{PATH}/{name}/src/middleware/middleware.go').touch()
    alternativeOpen(
        f'{PATH}/{name}/src/middleware/middleware.go', 'package middleware')

    Path(f'{PATH}/{name}/src/controllers').mkdir()
    Path(f'{PATH}/{name}/src/controllers/controllers.go').touch()
    alternativeOpen(
        f'{PATH}/{name}/src/controllers/controllers.go', 'package controllers')

    Path(f'{PATH}/{name}/src/routers').mkdir()
    Path(f'{PATH}/{name}/src/routers/routers.go').touch()
    alternativeOpen(f'{PATH}/{name}/src/routers/routers.go', 'package routers')


if __name__ == '__main__':
    pass
