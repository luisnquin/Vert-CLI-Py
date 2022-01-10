import json


def alternativeOpen(path: str, to_write: str):
    file = open(path, 'w', encoding='UTF-8')
    file.write(to_write)
    file.close()

def getconfigJSON(configpath: str):
    file = open(configpath, 'r')
    content = json.load(file)
    file.close()

    return content


if __name__ == '__main__':
    pass