import sqlite3

from ap_zadacha.db.config import Config
from ap_zadacha.db.prepare import load_initial_data_to_db


class CountriesDatabase:
    def __init__(self):
        self.file = Config.get_database_file()
        if not self.check_table_exists() and not self.file == 'testing.db':
            load_initial_data_to_db()

    def check_table_exists(self) -> bool:
        with sqlite3.connect(self.file) as conn:
            cur = conn.cursor()
            cur.execute("""SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'countries'""")
            if cur.fetchone()[0] == 1:
                return True
            return False

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()
