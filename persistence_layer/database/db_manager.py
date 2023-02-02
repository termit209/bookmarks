import sqlite3
from typing import Dict, Any, Optional


class DatabaseManager:
    def __init__(self, database_filename: str):
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement: str, values=[]):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values)
            return cursor

    def create_table(self, table_name: str, columns: Dict[str, Any]):
        columns_with_types = [
            f"{column_name} {data_type}"
            for column_name, data_type in columns.items()]
        statement = f'''
                    CREATE TABLE IF NOT EXISTS {table_name}
                    ({', '.join(columns_with_types)});
                    '''
        self._execute(statement)

    def add(self, table_name: str, data: Dict[str, Any]):
        columns = ', '.join(list(data.keys()))
        placeholder_str = ', '.join('?' * len(data))
        column_values = tuple(data.values())
        statement = f"""UPDATE sqlite_sequence SET seq=(SELECT COUNT(*) FROM '{table_name}')
         WHERE NAME = '{table_name}';"""
        self._execute(statement, [])
        statement = f'''INSERT INTO {table_name}
                        ({columns})
                        VALUES ({placeholder_str});
                     '''

        self._execute(statement, column_values)

    def delete(self, table_name: str, values: Dict[str, Any]):
        delete_criteria = ' AND '.join([f'{column} = ?'
                                        for column in values.keys()])

        statement = f'''DELETE FROM {table_name}
                        WHERE {delete_criteria};'''

        column_values = tuple(values.values())
        self._execute(statement, column_values)
        self._execute(f""" UPDATE '{table_name}' SET 'id' = rowid""")

    def select(self, table_name: str, values: Dict[str, Any] = {},
               order_by: Optional[str] = None):
        statement = f"""SELECT * FROM {table_name};"""
        column_values = []
        if values:
            criteria = ' AND '.join([f'{column} = ?'
                                    for column in values.keys()])
            column_values = tuple(values.values())
            statement.replace(";", f" WHERE {criteria};")

        if order_by:
            statement.replace(";", f" SORT BY {order_by};")

        return self._execute(statement, column_values)

    def update(self, table_name, values, data):
        self.delete(table_name, values)
        self.add(table_name, data)
