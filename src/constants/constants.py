from os import getenv

DBNAME = getenv("vert_dbname")
DBUSER = getenv("vert_dbuser")
DBPWD = getenv("vert_dbpwd")
DBHOST = getenv("vert_dbhost")
DBPORT = getenv("vert_dbport")

DSN = f'dbname={DBNAME} user={DBUSER} password={DBPWD} host={DBHOST} port={DBPORT}'
