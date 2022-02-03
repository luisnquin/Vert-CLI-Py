from typing import Union, Optional, Callable
from datetime import datetime
from random import choice
from os import getcwd

from faker import Faker


fake: object = Faker()

categories: list[str] = []


def gen(rounds: int, stmt: str, stmt_complement: Optional[str] = None, mock_data: Optional[tuple[any]] = None, function: Optional[Callable] = None) -> str:
    if function:
        for _ in range(rounds * 10):
            stmt += function()
        stmt += ';'
        stmt = stmt.replace(')(', '), (')
        return stmt

    for _ in range(rounds * 10):
        stmt += \
            stmt_complement % tuple((element() if hasattr(element, '__call__')
                                     else element for element in mock_data))
    stmt += ';'
    stmt = stmt.replace(')(', '), (')
    return stmt


def main(rounds: int) -> None:
    def category_body():
        category: str = fake.word().capitalize()
        categories.append(category)
        stmt: str = '(\'%s\')' % (category)
        return stmt

    stmts: list[str] = []

    stmts.append(gen(rounds=rounds, stmt='INSERT INTO categories(name) VALUES',
                 function=category_body)[:-1] + ' ON CONFLICT (name) DO NOTHING;')

    stmts.append(gen(rounds=rounds, stmt='INSERT INTO urls(url, datetime) VALUES',
                     stmt_complement='(\'%s\', \'%s\')', mock_data=(lambda: fake.url(), lambda: datetime.now())))

    stmts.append(gen(rounds=rounds, stmt='INSERT INTO tasks(name, category, status, datetime) VALUES',
                     stmt_complement='(\'%s\', \'%s\', 0, \'%s\')', mock_data=(lambda: fake.text().replace('\n', ' '), lambda: choice(categories), lambda: datetime.now())))

    stmts.append(gen(rounds=rounds, stmt='INSERT INTO ideas(name, datetime) VALUES',
                     stmt_complement='(\'%s\', \'%s\')', mock_data=(lambda: fake.name().capitalize(), lambda: datetime.now())))

    stmts.append(gen(rounds=rounds, stmt='INSERT INTO notifications(title, message, datetime) VALUES',
                     stmt_complement='(\'%s\', \'%s\', \'%s\')', mock_data=(lambda: fake.name(), lambda: fake.text().replace('\n', ' '), lambda: datetime.now())))

    trnct_stmts: tuple[str] = ('TRUNCATE TABLE categories RESTART IDENTITY CASCADE;', 'TRUNCATE TABLE urls RESTART IDENTITY CASCADE;',
                               'TRUNCATE TABLE tasks RESTART IDENTITY CASCADE;', 'TRUNCATE TABLE ideas RESTART IDENTITY CASCADE;',
                               'TRUNCATE TABLE notifications RESTART IDENTITY CASCADE;')

    if getcwd().find("/src/tools") != -1:
        with open('./../test/statements.sql', 'w', encoding='UTF-8') as file:
            for stmt in trnct_stmts:
                file.write('%s\n' % (stmt))
            for stmt in stmts:
                file.write('%s\n' % (stmt))

    elif getcwd().find("/src") != -1:
        with open('./test/statements.sql', 'w', encoding='UTF-8') as file:
            for stmt in trnct_stmts:
                file.write('%s\n' % (stmt))
            for stmt in stmts:
                file.write('%s\n' % (stmt))
    else:
        print(stmts)


if __name__ == '__main__':
    main(rounds=5)
