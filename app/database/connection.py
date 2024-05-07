import psycopg2
from contextlib import contextmanager
from typing import Any, Iterator, List, Optional
from config import Config

from app.database.db_connection import PGConnection

# DATABASE_PATH = Config.DATABASE_PATH

connectionDB = PGConnection()

@contextmanager
def __get_cursor() -> Iterator[psycopg2.extensions.cursor]:
    connection = connectionDB
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def _fetch_one(query: str, parameters: Optional[List[str]] = None) -> Any:
    if parameters is None:
        parameters = []

    with __get_cursor() as cursor:
        cursor.execute(query, parameters)
        return cursor.fetchone()


def _fetch_all(query: str, parameters: Optional[List[str]] = None) -> List:
    if parameters is None:
        parameters = []

    with __get_cursor() as cursor:
        cursor.execute(query, parameters)
        return cursor.fetchall()


def _fetch_none(query: str, parameters: Optional[List[str]] = None) -> None:
    if parameters is None:
        parameters = []

    with __get_cursor() as cursor:
        cursor.execute(query, parameters)


def _fetch_lastrow_id(query: str, parameters: Optional[List[str]] = None) -> int:
    if parameters is None:
        parameters = []

    with __get_cursor() as cursor:
        cursor.execute(query, parameters)
        return cursor.lastrowid
