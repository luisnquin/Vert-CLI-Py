from pathlib import Path
from os import system, getcwd, mkdir
from re import search

import typer

from constants.constants import PROJECTS_PATH as PATH
from .utils import alternativeOpen


def GenerateGoProject(name: str):
    cwd = getcwd()
    if search("\s", name) is not None:
        typer.BadParameter('NO SPACES')
        typer.Exit()
        return

    mkdir(f'{PATH}/{name}')
    Path(f'{PATH}/{name}/.env').touch()
    Path(f'{PATH}/{name}/.env.example').touch()
    Path(f'{PATH}/{name}/.gitignore').touch()
    alternativeOpen(f'{PATH}/{name}/.gitignore', '.env')

    mkdir(f'{PATH}/{name}/src')
    mkdir(f'{PATH}/{name}/src/requests')
    system(f'git init {PATH}/name')
    Path(f'{PATH}/{name}/src/main.go').touch()
    alternativeOpen(f'{PATH}/{name}/src/main.go', 'package main')

    mkdir(f'{PATH}/{name}/src/models')
    Path(f'{PATH}/{name}/src/models/models.go').touch()
    alternativeOpen(f'{PATH}/{name}/src/models/models.go', 'package models')

    mkdir(f'{PATH}/{name}/src/certificates')
    Path(f'{PATH}/{name}/src/certificates/certificates.go').touch()
    alternativeOpen(
        f'{PATH}/{name}/src/certificates/certificates.go', 'package certificates')

    mkdir(f'{PATH}/{name}/src/utils')
    Path(f'{PATH}/{name}/src/utils/utils.go').touch()
    alternativeOpen(f'{PATH}/{name}/src/utils/utils.go', 'package utils')

    mkdir(f'{PATH}/{name}/src/db')
    Path(f'{PATH}/{name}/src/db/db.go').touch()
    alternativeOpen(f'{PATH}/{name}/src/db/db.go', 'package db')

    mkdir(f'{PATH}/{name}/src/middleware')
    Path(f'{PATH}/{name}/src/middleware/middleware.go').touch()
    alternativeOpen(
        f'{PATH}/{name}/src/middleware/middleware.go', 'package middleware')

    mkdir(f'{PATH}/{name}/src/controllers')
    Path(f'{PATH}/{name}/src/controllers/controllers.go').touch()
    alternativeOpen(
        f'{PATH}/{name}/src/controllers/controllers.go', 'package controllers')

    mkdir(f'{PATH}/{name}/src/routers')
    Path(f'{PATH}/{name}/src/routers/routers.go').touch()
    alternativeOpen(f'{PATH}/{name}/src/routers/routers.go', 'package routers')

    system(f'cd {PATH}/{name}/src')
    system(f'go mod init github.com/luisnquin/{name}/src')
    system('git add --all')
    system('git commit -m "first commit"')
    system(f'cd {cwd}')
