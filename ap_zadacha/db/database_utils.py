import sqlite3

from ap_zadacha.db.prepare import DB_FILENAME, load_data_to_db


class CountriesDatabase:
    def __init__(self, file=DB_FILENAME):
        self.file = file
        # if not check_table_exists():
        load_data_to_db()

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, _type, value, traceback):
        self.conn.commit()
        self.conn.close()
