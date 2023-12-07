import json
import os
import re
import sqlite3


class MovieData:

    def __init__(self, file_path: str):
        self.movie_list = self._file_parser(file_path)
        self.db_name = self._db_name_make(file_path)

        self.connection = None
        self.cursor = None
        self._connecting()

    def _file_parser(self, file_path):

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

    def _connecting(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    @staticmethod
    def _verify_table_name(table_name):
        return ''.join(chr for chr in table_name if chr.isalnum())

    def create_new_table(self, table_name:str, *column_names: str):
        columns = ", ".join(column_names)
        name = self._verify_table_name(table_name)
        sql_script = f"CREATE TABLE IF NOT EXISTS {table_name}({columns})"
        try:
            self.cursor.execute(sql_script)
        except sqlite3.OperationalError:
            create = f"Table {name} already exists"
        else:
            create = f'Table {name} is created with columns: {columns}'
        print(create)

    def insert_data(self, table_name:str):
        name = self._verify_table_name(table_name)
        sql_script = f"INSERT INTO {name} VALUES(:genre, :title)"
        self.cursor.executemany(sql_script, self.movie_list)
        self.connection.commit()


    def user_search(self, parametr:str, value:str):
        data = (value, )
        sql_script = f"SELECT * FROM movie WHERE {parametr}=?"
        self.cursor.execute(sql_script, data)
        result = self.cursor.fetchall()
        for film in result:
            print(film)
        return result

    def con_close(self):
        self.connection.close()

if __name__ == "__main__":
    m = MovieData('movies.json')
    m.create_new_table('movie', 'genre', 'title')
    m.insert_data('movie')
    m.user_search('genre', 'Horror')
    m.con_close()