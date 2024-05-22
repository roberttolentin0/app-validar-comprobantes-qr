import os
import traceback
import psycopg2

from contextlib import contextmanager
from typing import Any, Iterator, List, Optional
from ..utils.Logger import Logger

from dotenv import load_dotenv

load_dotenv()


class Connection:

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn = None


    def connect(self):
        try:
            conn_params = {
                "host": self.host,
                "database": self.database,
                "user": self.user,
                "password": self.password,
                "port": self.port
            }
            self.conn = psycopg2.connect(**conn_params)
            return self.conn
        except psycopg2.Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            # print("Error, connect db: ", str(e))


    def close(self):
        if self.conn is not None:
            self.conn.close()
            print("Conexión cerrada")

    @contextmanager
    def __get_cursor(self) -> Iterator[psycopg2.extensions.cursor]:
        connection = self.connect()
        cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    def _fetch_one(self, query: str, parameters: Optional[List[str]] = None) -> Any:
        if parameters is None:
            parameters = []

        with self.__get_cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchone()


    def _fetch_all(self, query: str, parameters: Optional[List[str]] = None) -> List:
        if parameters is None:
            parameters = []

        with self.__get_cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchall()

    def _fetch_none(self, query: str, parameters: Optional[List[str]] = None) -> None:
        if parameters is None:
            parameters = []

        with self.__get_cursor() as cursor:
            cursor.execute(query, parameters)

    def _fetch_lastrow_id(self, query: str, parameters: Optional[List[str]] = None) -> int:
        if parameters is None:
            parameters = []
        with self.__get_cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchone()[0]


class DBConnection(Connection):
    def __init__(self):
        host = os.getenv('DB_HOST')
        database = os.getenv('DB_DATABASE')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        port = os.getenv('DB_PORT')
        super().__init__(host, database, user, password, port)
