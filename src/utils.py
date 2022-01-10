import json

from typer import echo, style, colors


def printError(error):
    echo(style(error, fg=colors.RED), err=True)


def printWarning(msg):
    echo(style(msg, fg=colors.MAGENTA), err=True)


def printSpecial(msg):
    echo(style(msg, fg=colors.BRIGHT_GREEN))


def overwriteconfigJSON(content: dict, path: str):
    file = open(path, 'w', encoding='UTF-8')
    json.dump(content, file, indent=4)
    file.close()


def getconfigJSON(configpath: str):
    file = open(configpath, 'r')
    content = json.load(file)
    file.close()

    return content
