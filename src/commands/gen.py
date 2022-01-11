import typer

from utils.utils import print_success, get_config
from gen.staticgen import gen_static_project
from gen.gogen import gen_go_project
from gen.pygen import gen_py_project


gen: object = typer.Typer()


@gen.command()
def go(project_name=typer.Option(..., prompt=True, help='A new Go project will be created in your workspace path')):
    """
    vert gen go
    """
    gen_go_project(project_name)
    print_success('Project ready in: {}'
                  .format(get_config('./config.json')['path']))

    raise typer.Exit()


@gen.command()
def py(project_name=typer.Option(..., prompt=True, help='A new Python project will be created in your workspace path')):
    """
    vert gen py
    """
    gen_py_project(project_name)
    print_success('Project ready in: {}'
                  .format(get_config('./config.json')['path']))

    raise typer.Exit()


@gen.command()
def static(project_name=typer.Option(..., prompt=True, help='A new Python project will be created in your workspace path')):
    """
    vert gen static
    """
    gen_static_project(project_name)
    print_success('Project ready in: {}'
                  .format(get_config('./config.json')['path']))

    raise typer.Exit()
