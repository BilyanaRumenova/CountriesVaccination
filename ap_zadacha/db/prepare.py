import sqlite3

DB_FILENAME = "./countries.db"


def load_initial_data_to_db() -> None:
    con = sqlite3.connect(DB_FILENAME)
    cur = con.cursor()
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS countries
                       (iso_code text PRIMARY KEY, name text, population int, 
                       total_vaccinated int, percentage_vaccinated real)''')
        cur.execute('''INSERT INTO countries
                       (iso_code, name, population, total_vaccinated, percentage_vaccinated) VALUES
                       ('USA', 'United States of America', '328329953', '12', '0.00000365485'),
                       ('BRA', 'Brazilia', '92746607','5000','0.00539103279'),
                       ('HOL', 'Holland', '17441139','10000','0.05733570496'),
                       ('OWID_CEB','Central Europe and the Baltics', '102253057','500000','0.48898293573')''')
        con.commit()
        con.close()
    except ValueError:
        print("Table already exists")



