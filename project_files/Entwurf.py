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

    def _db_name_make(self, file_path):
        return os.path.splitext(os.path.basename(file_path))[0] + ".db"

    def _connecting(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_new_table(self, table_name:str, *column_names: str):
        #qmark_counter = ', '.join('?' for x in column_names)
        #sql_script = f"CREATE TABLE ? ({qmark_counter})"
        col = column_names
        try:
            self.cursor.execute("CREATE TABLE  movie(?, ?)", col)
        except sqlite3.OperationalError as e:
            create = f"Error: {e}"
        else:
            create = f'Table {table_name} is created with columns: {column_names}'
        print(create)

    def insert_data(self, table_name: str):
        sql_script = f"INSERT INTO {table_name} VALUES(:genre, :title)"
        self.cursor.executemany(sql_script, self.movie_list)
        self.connection.commit()


    def user_search(self, parametr:str, value:str):
        data = (parametr, value)
        data = tuple(data)
        sql_script = "SELECT * FROM movie WHERE ?=?"
        print('search sql:', sql_script)
        self.cursor.execute(sql_script, data)
        result = self.cursor.fetchall()
        print('Result:', result)
        for film in result:
            print(film)
        return result

    def con_close(self):
        self.connection.close()


m = MovieData('movies.json')
m.create_new_table('movie', 'genre', 'title')
m.insert_data('movie')
m.user_search('genre', 'Drama')
m.con_close()