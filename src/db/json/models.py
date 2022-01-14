from datetime import datetime
from typing import Union

from constants.constants import json_db_path
from utils.utils import overwrite_json, get_json


class Tasks:
    @classmethod
    def get(cls) -> Union[list[dict], str]:
        return get_json(json_db_path)['tasks']

    @classmethod
    def clean(cls) -> str:
        json: dict[list[dict]] = get_json(json_db_path)
        for i, task in enumerate(json['tasks']):
            if task['status'] == '\u2713':
                json['tasks'].pop(i)

        overwrite_json(json, json_db_path)
        return 'Cleaned'

    def __init__(self, id: int = None, name: str = None, status: int = None, category: str = None) -> object:
        self.id: int = id
        self.name: str = name
        self.category: int = category
        self.status: str = status
        self.datetime: str = str(datetime.now())

    def add(self) -> str:
        json: dict[list[dict]] = get_json(json_db_path)

        try:
            id: int = max({value['id'] for value in json['tasks']}) + 1
        except ValueError:
            id: int = 1

        json['tasks'].append({
            'id': id,
            'name': self.name,
            'status': '✗',
            'category': self.category,
            'datetime': self.datetime
        })

        overwrite_json(json, json_db_path)

        return 'Modified!'

    def update_status(self) -> str:
        json: dict[list[dict]] = get_json(json_db_path)
        if self.status == 1:
            self.status:str = '✓'
        elif self.status == 0:
            self.status:str = '✗'

        for i, task in enumerate(json['tasks']):
            if task['id'] == self.id:
                json['tasks'][i]['status'] = self.status
                overwrite_json(json, json_db_path)
                return 'Status modified!'

        return 'Task not found'

    def remove(self) -> str:
        json: dict[list[dict]] = get_json(json_db_path)

        for i, task in enumerate(json['tasks']):
            if task['id'] == self.id:
                json['tasks'].pop(i)
                overwrite_json(json, json_db_path)
                return 'Removed!'

        return 'Task not found'


class Categories:
    @classmethod
    def get(cls) -> Union[list[dict], str]:
        return get_json(json_db_path)['categories']

    def __init__(self, id: int = None, name: str = None) -> object:
        self.id: int = id
        self.name: str = name

    def add(self) -> str:
        json: dict[list[dict]] = get_json(json_db_path)

        try:
            id: int = max({value['id'] for value in json['categories']}) + 1
        except ValueError:
            id: int = 1

        json['categories'].append(
            {'id': id,
             'name': self.name}
        )

        overwrite_json(json, json_db_path)

        return 'Modified!'

    def remove(self) -> str:
        json: dict[list[dict]] = get_json(json_db_path)

        for i, category in enumerate(json['categories']):
            if category['id'] == self.id:
                json['categories'].pop(i)

                for i, task in enumerate(json['tasks']):
                    if task['category'] == category['name']:
                        json['tasks'].pop(i)

                overwrite_json(json, json_db_path)

                return 'Removed!'

        return 'Category not found'


class Urls:
    @classmethod
    def get(cls) -> Union[list[dict], str]:
        return get_json(json_db_path)['urls']

    def __init__(self, id: int = None, title: str = None, url: str = None) -> object:
        self.id: int = id
        if title:
            self.title: str = title
        else:
            self.title: str = 'Unknown'
        self.url: str = url
        self.datetime: str = str(datetime.now())

    def add(self) -> str:
        json: dict[list[dict]] = get_json(json_db_path)

        try:
            id: int = max({value['id'] for value in json['urls']}) + 1
        except ValueError:
            id: int = 1

        json['urls'].append({
            'id': id,
            'title': self.title,
            'url': self.url,
            'datetime': self.datetime
        })
        overwrite_json(json, json_db_path)

        return 'Modified!'

    def remove(self) -> str:
        json: dict[list[dict]] = get_json(json_db_path)

        for i, url in enumerate(json['urls']):
            if url['id'] == self.id:
                json['urls'].pop(i)
                overwrite_json(json, json_db_path)

                return 'Removed!'

        return 'URL not found'


class Ideas:
    @classmethod
    def get(cls) -> list[dict]: return get_json(json_db_path)['ideas']

    def __init__(self, id: int = None, name: str = None) -> object:
        self.id: int = id
        self.name: str = name
        self.datetime: str = str(datetime.now())

    def add(self) -> str:
        json: dict[list[dict]] = get_json(json_db_path)

        try:
            id: int = max({value['id'] for value in json['ideas']}) + 1
        except ValueError:
            id: int = 1

        json['ideas'].append({
            'id': id,
            'name': self.name,
            'datetime': self.datetime
        })
        overwrite_json(json, json_db_path)

        return 'Modified!'

    def remove(self) -> str:
        json: dict[list[dict]] = get_json(json_db_path)

        for i, idea in enumerate(json['ideas']):
            if idea['id'] == self.id:
                json['ideas'].pop(i)

                overwrite_json(json, json_db_path)

                return 'Removed!'

        return 'Not found'
