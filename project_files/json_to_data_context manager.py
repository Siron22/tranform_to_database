import json
import os
import re
import sqlite3


class MovieData:

    def __init__(self, file_path: str):
        self.data_list = self._file_parser(file_path)
        self.db_name = self._db_name_make(file_path)
        self.columns = self._parse_columns_names(self.data_list)
        self.table_name = None
        self.connection = None
        self.cursor = None

    @staticmethod
    def _file_parser(file_path):
        pattern_json = r'^.*\.(json)$'
        if re.search(pattern_json, file_path):
            with open(file_path, 'r') as f:
                json_obj = json.load(f)
        else:
            print("Wrong file format")
            exit()

        return json_obj

    @staticmethod
    def _db_name_make(file_path):
        return os.path.splitext(os.path.basename(file_path))[0] + ".db"

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self


    @staticmethod
    def _parse_columns_names(data: dict):
        return [k for k in data[0].keys()]

    @staticmethod
    def _verify_input_data(table_name):
        return ''.join(s for s in table_name if s.isalnum())

    @staticmethod
    def _make_columns_from_list(data):
        return ", ".join(data)

    def _create_new_table(self, table_name: str):
        self.table_name = self._verify_input_data(table_name)
        columns = self._make_columns_from_list(self.columns)
        sql_script = f"CREATE TABLE IF NOT EXISTS {self.table_name}({columns})"
        try:
            self.cursor.execute(sql_script)
        except sqlite3.OperationalError as e:
            create = f"Error: {e}"
        else:
            create = f'Table {self.table_name} is created with columns: {columns}'
        print(create)

    def _insert_data(self):
        values = [":" + c for c in self.columns]
        columns = self._make_columns_from_list(values)
        sql_script = f"INSERT INTO {self.table_name} VALUES({columns})"
        self.cursor.executemany(sql_script, self.data_list)
        self.connection.commit()

    def make_table_with_data(self, table_name: str):
        self._create_new_table(table_name)
        self._insert_data()

    def user_search(self, parametr: str, value: str,):
        par = self._verify_input_data(parametr)
        data = (value,)
        sql_script = f"SELECT * FROM {self.table_name} WHERE {par}=?"
        self.cursor.execute(sql_script, data)
        result = self.cursor.fetchall()
        for film in result:
            print(film)
        return result

    def __exit__(self, exc_class, exc, traceback):
        self.connection.commit()
        self.connection.close()


if __name__ == "__main__":
    with MovieData('movies.json') as m:
        m.make_table_with_data('my_movies')
        m.user_search('genre', 'Horror')



















