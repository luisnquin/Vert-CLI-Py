
def alternativeOpen(path: str, to_write: str):
    file = open(path, 'w', encoding='UTF-8')
    file.write(to_write)
    file.close()
