import sqlite3

from config import BASE_DIR
from .exceptions import NoConnectionError

DATABASE_DIR = BASE_DIR / 'database'


class DBManager: 
    def connect(self, db_path: str) -> None:
        self.__connection = sqlite3.connect(db_path)
    
    def __check_connection(self) -> None:
        if not self.__connection:
            raise NoConnectionError()

    def close(self) -> None:
        self.__check_connection()
        self.__connection.close()
        self.__connection = None

    def execute(self, query: str, params: tuple[str] = (), many: bool = False) -> None:
        self.__check_connection()
        cursor = self.__connection.cursor()
        try:
            result = cursor.execute(query, params)
            if not result:
                return 
            if many:
                return result.fetchall()
            return result.fetchone()
        except sqlite3.Error as e:
            self.close()
            raise e

    def commit(self) -> None:
        self.__check_connection
        self.__connection.commit()


def get_db_manager() -> DBManager:
    db_manager = DBManager()
    db_manager.connect(BASE_DIR / 'dining_room.db')
    return db_manager


def create_tables() -> None:
    create_tables_file = DATABASE_DIR / 'create_tables.sql'
    with open(create_tables_file, 'r') as file:
        create_tables_script = file.read()
        connection = sqlite3.connect(BASE_DIR / 'dining_room.db')
        try:
            cursor = connection.cursor()
            cursor.executescript(create_tables_script)
            connection.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            connection.close()
