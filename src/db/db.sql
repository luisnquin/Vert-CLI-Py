CREATE TABLE categories(
    id SERIAL PRIMARY KEY,
    name VARCHAR(25) NOT NULL UNIQUE
);

INSERT INTO categories(name) VALUES('Programming'), ('Projects'), ('Work'), ('Homework');

CREATE TABLE status (
    id SERIAL PRIMARY KEY NOT NULL,
    symbol CHAR(1)
);

INSERT INTO status VALUES(0, '✗'), (1, '✓');

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category VARCHAR(25) NOT NULL,
    status INTEGER NOT NULL,
    datetime VARCHAR(26) NOT NULL,
    CONSTRAINT fk_category_categories FOREIGN KEY(category) REFERENCES categories(name) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_status_status FOREIGN KEY(status) REFERENCES status(id) ON UPDATE RESTRICT ON DELETE RESTRICT
);


CREATE TABLE ideas (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    datetime VARCHAR(26) NOT NULL
);
