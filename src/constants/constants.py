from pathlib import Path


config_path: str = str(Path('vert-cli/src/config.json').resolve())
tasker_path: str = str(Path('vert-cli/src/tasker/tasker').resolve())
queries_path: str = str(Path('vert-cli/src/db/sql/db.sql').resolve())
json_db_path: str = str(Path('vert-cli/src/db/json/db.json').resolve())
src_path: str = str(Path('vert-cli/src').resolve())


"""
from os import getcwd

if getcwd() == '/home/luisnquin/workspace/projects/vert-cli/src':
    config_path: str = str(Path('./config.json').resolve())
    tasker_path: str = str(Path('./tasker/tasker').resolve())
    queries_path: str = str(Path('./db/sql/db.sql').resolve())
    json_db_path: str = str(Path('./db/json/db.json').resolve())
    src_path: str = str(Path('.').resolve())
"""
