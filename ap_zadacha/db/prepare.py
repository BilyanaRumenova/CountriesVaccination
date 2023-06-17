from pathlib import Path
import sqlite3

import pandas as pd

DB_FILENAME = "./zadacha.db"


def init_db(filename: str = DB_FILENAME) -> None:
    if not Path(filename).is_file():
        Path(filename).touch()


def load_data_to_db() -> None:
    init_db(DB_FILENAME)
    con = sqlite3.connect(DB_FILENAME)
    cur = con.cursor()
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS countries
                       (id integer PRIMARY KEY AUTOINCREMENT, name text unique , iso_code text, population int, 
                       total_vaccinated int, percentage_vaccinated real)''')
        cur.execute('''INSERT INTO countries
                       (name, iso_code, population, total_vaccinated, percentage_vaccinated) VALUES
                       ('United States of America', 'USA', '328329953', '12', '0.00000365485'),
                       ('Brazilia','BRA','92746607','5000','0.00539103279'),
                       ('Holland','HOL','17441139','10000','0.05733570496 '),
                       ('Central Europe and the Baltics','OWID_CEB','102253057','500000','0.48898293573 ')''')
        con.commit()
        con.close()
    except ValueError:
        print("Table already exists")


def check_table_exists() -> bool:
    import sqlite3
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()
    cur.execute("""
            SELECT count(name)
            FROM sqlite_master
            WHERE type = 'table' AND name = 'countries'
            """)
    if cur.fetchone()[0] == 1:
        conn.close()
        return True
    cur.close()
    return False


def load_csv_to_db() -> None:
    init_db(DB_FILENAME)
    conn = sqlite3.connect(DB_FILENAME)
    vaccinations_data = pd.read_csv('data/vaccinations.csv')
    COLUMNS = ['location', 'iso_code', 'date', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated',
               'total_boosters', 'daily_vaccinations_raw', 'daily_vaccinations', 'total_vaccinations_per_hundred',
               'people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred',
               'daily_vaccinations_per_million', 'daily_people_vaccinated', 'daily_people_vaccinated_per_hundred']

    vaccinations_data.columns = COLUMNS
    try:
        vaccinations_data.to_sql('vaccinations', conn, if_exists='fail', index=False)
    except ValueError:
        print("Table already exists")
