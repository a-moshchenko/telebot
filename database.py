from typing import Dict, List
import psycopg2
from logging_seting import logger
from main import config

name = config.get('Postgresql', 'db')
user = config.get('Postgresql', 'user')
password = config.get('Postgresql', 'password')
host = config.get('Postgresql', 'host')
conn = psycopg2.connect(
    database=name,
    user=user,
    password=password,
    host=host,
    port=5432
)
logger.info('Postgresql database opened succsesfuly')
cursor = conn.cursor()


def insert(values: Dict) -> None:
    cursor.execute("INSERT INTO screenshot(name, url) "
                   "VALUES(%s, %s);", (values['name'], values['url']))
    conn.commit()


def delete(row_name: str) -> None:
    cursor.execute(f"DELETE FROM screenshot WHERE name = '{row_name}';")
    conn.commit()


def fetchall() -> List[Dict]:
    columns = ['name', 'url']
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM screenshot")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def _init_db() -> None:
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.execute(sql)
    conn.commit()


def check_db_exists() -> None:
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT * FROM information_schema.tables "
                   "WHERE table_name='screenshot'")
    if bool(cursor.rowcount):
        return
    _init_db()

check_db_exists()
