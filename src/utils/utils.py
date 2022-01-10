from io import TextIOWrapper
from json import load, dump

from typer import echo, style, colors


def printError(error: str) -> None:
    echo(style(error, fg=colors.RED), err=True)


def printFatal(error: str) -> None:
    echo(style(error, fg=colors.WHITE, bg=colors.RED), err=True)


def printWarning(msg: str) -> None:
    echo(style(msg, fg=colors.MAGENTA))


def printSuggestion(msg: str) -> None:
    echo(style(msg, fg=colors.BRIGHT_YELLOW))


def printSuccess(msg: str) -> None:
    echo(style(msg, fg=colors.BRIGHT_GREEN))


def overwriteconfigJSON(content: dict, path: str) -> None:
    file = open(path, 'w', encoding='UTF-8')
    dump(content, file, indent=4)
    file.close()


def getconfigJSON(configpath: str) -> dict:
    file: TextIOWrapper = open(configpath, 'r')
    content: dict = load(file)
    file.close()

    return content


def alternativeOpen(path: str, to_write: str) -> None:
    file: TextIOWrapper = open(path, 'w', encoding='UTF-8')
    file.write(to_write)
    file.close()


# CheckPathWithRegex


# CheckdbconfigWithRegex
