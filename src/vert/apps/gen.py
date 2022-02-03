from typer import Typer, Option, Exit

from utils.utils import print_success, open_vscode
from gen.staticgen import static_project
from gen.gogen import go_project
from gen.pygen import py_project


gen: object = Typer()


@gen.command()
def go(project_name: str = Option(..., prompt=True)):
    """
    vert gen go

    To generate a new Go project,
    just use it if you have your workspace set up
    """
    path: str = go_project(project_name)
    print_success(f'Project ready in: {path}\n')
    open_vscode(path)

    raise Exit()


@gen.command()
def py(project_name: str = Option(..., prompt=True)):
    """
    vert gen py

    To generate a new Python project,
    just use it if you have your workspace set up
    """
    path: str = py_project(project_name)
    print_success(f'Project ready in: {path}\n')
    open_vscode(path)

    raise Exit()


@gen.command()
def static(project_name: str = Option(..., prompt=True)):
    """
    vert gen static

    To generate a new Static project,
    just use it if you have your workspace set up
    """
    path: str = static_project(project_name)
    print_success(f'Project ready in: {path}\n')
    open_vscode(path)

    raise Exit()
