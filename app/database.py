import sqlite3
from typing import Any, List, Tuple, Optional

class Database:
    def __init__(self, db_name: str):
        """Инициализация класса, создание соединения с базой данных."""
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name: str, columns: str):
        """
        Создает таблицу.
        :param table_name: Имя таблицы.
        :param columns: Строка с определением столбцов, например "id INTEGER PRIMARY KEY, name TEXT".
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.connection.commit()

    def insert_data(self, table_name: str, columns: str, values: Tuple[Any]):
        """
        Добавляет запись в таблицу.
        :param table_name: Имя таблицы.
        :param columns: Столбцы, в которые будут добавлены данные, например "id, name".
        :param values: Кортеж с данными.
        """
        placeholders = ", ".join(["?" for _ in values])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()

    def update_data(self, table_name: str, set_clause: str, condition: str, values: Tuple[Any]):
        """
        Обновляет записи в таблице.
        :param table_name: Имя таблицы.
        :param set_clause: Условие изменения, например "name = ?".
        :param condition: Условие выбора строк, например "id = ?".
        :param values: Кортеж с данными для set_clause и condition.
        """
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_data(self, table_name: str, condition: str, values: Tuple[Any]):
        """
        Удаляет записи из таблицы.
        :param table_name: Имя таблицы.
        :param condition: Условие выбора строк, например "id = ?".
        :param values: Кортеж с данными для condition.
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query, values)
        self.connection.commit()

    def fetch_data(self, query: str, values: Optional[Tuple[Any]] = None) -> List[Tuple[Any]]:
        """
        Выполняет SELECT-запрос.
        :param query: Текст SQL-запроса.
        :param values: Кортеж с параметрами запроса.
        :return: Список кортежей с результатами запроса.
        """
        with self.connection:
            cursor = self.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            return cursor.fetchall()

    def __del__(self):
        """Закрывает соединение при удалении объекта."""
        self.close_connection()

    def close_connection(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            self.connection.close()
            self.connection = None