import typer

from utils.utils import print_success, open_vscode_or_not
from gen.staticgen import gen_static_project
from gen.gogen import gen_go_project
from gen.pygen import gen_py_project


gen: object = typer.Typer()


@gen.command()
def go(project_name=typer.Option(..., prompt=True, help='A new Go project will be created in your workspace path')):
    """
    vert gen go

    To generate a new Go project,
    just use it if you have your workspace set up
    """
    path: str = gen_go_project(project_name)
    print_success(f'Project ready in: {path}\n')
    open_vscode_or_not(path)

    raise typer.Exit()


@gen.command()
def py(project_name=typer.Option(..., prompt=True, help='A new Python project will be created in your workspace path')):
    """
    vert gen py

    To generate a new Python project,
    just use it if you have your workspace set up
    """
    path: str = gen_py_project(project_name)
    print_success(f'Project ready in: {path}\n')
    open_vscode_or_not(path)

    raise typer.Exit()


@gen.command()
def static(project_name=typer.Option(..., prompt=True, help='A new Python project will be created in your workspace path')):
    """
    vert gen static

    To generate a new Static project,
    just use it if you have your workspace set up
    """
    path: str = gen_static_project(project_name)
    print_success(f'Project ready in: {path}\n')
    open_vscode_or_not(path)

    raise typer.Exit()
