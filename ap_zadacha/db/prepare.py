from pathlib import Path
import sqlite3

DB_FILENAME = "../zadacha.db"


def init_db(filename: str = DB_FILENAME) -> None:
    if not Path(filename).is_file():
        Path(filename).touch()


def load_data_to_db() -> None:
    init_db(DB_FILENAME)
    con = sqlite3.connect(DB_FILENAME)
    cur = con.cursor()
    try:
        cur.execute("""CREATE TABLE countries
                       (id int PRIMARY KEY AUTOINCREMENT , name text, iso_code text, population int, total_vaccinated int, percentage_vaccinated real)""")
        cur.execute("""INSERT INTO countries
                       (name, iso_code, population, total_vaccinated, percentage_vaccinated) VALUES
                       ('United States of America', 'USA', '328329953', '12', '0.00000365485'),
                       ('Brazilia','BRA','92746607','5000','0.00539103279'),
                       ('Holland','HOL','17441139','10000','0.05733570496 '),
                       ('Central Europe and the Baltics','OWID_CEB','102253057','500000','0.48898293573 ')""")
        # cur.execute("""CREATE TABLE country_populations
        #                 (id int PRIMARY KEY AUTOINCREMENT , country_name text, country_code text,
        #                 indicator text, indicator_code text , '1960' int , '1961' int, '1962' int, '1963' int,
        #                 '1964' int, '1965' int, '1966' int, '1967' int, '1968' int, '1969' int, '1970' int, '1971' int,
        #                 '1972' int, '1973' int, '1974' int, '1975' int, '1976' int, '1977' int, '1978' int, '1979' int,
        #                 '1980' int, '1981' int, '1982' int, '1983' int, '1984' int, '1985' int, '1986' int, '1987' int,
        #                 '1988' int, '1989' int, '1990' int, '1991' int, '1992' int, '1993' int, '1994' int, '1995' int,
        #                 '1996' int, '1997' int, '1998' int, '1999' int, '2000' int, '2001' int, '2002' int, '2003' int,
        #                 '2004' int, '2005' int, '2006' int, '2007' int, '2008' int, '2009' int, '2010' int, '2011' int,
        #                 '2012' int, '2013' int, '2014' int, '2015' int, '2016' int, '2017' int, '2018' int, '2019' int,
        #                 '2020' int)""")

        con.commit()
        con.close()
    except ValueError:
        print("Table already exists")


def check_table_exists() -> bool:
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    x = cursor.execute("""
    SELECT * FROM countries WHERE name='Brazilia' AND iso_code='BRA'
    """)
    return cursor.fetchone()



# def load_csv_to_db() -> None:
#     init_db(DB_FILENAME)
#     conn = sqlite3.connect(DB_FILENAME)
#     vaccinations_data = pd.read_csv('data/vaccinations.csv')
#     vaccinations_data.columns = COLUMNS
#     try:
#         vaccinations_data.to_sql('vaccinations', conn, if_exists='fail', index=False)
#     except ValueError:
#         print("Table already exists")

# con = sqlite3.connect('zadacha.db')

# cur = con.cursor()
# cur.execute('''CREATE TABLE countries
#                (name text, iso_code text, population int, total_vaccinated int, percentage_vaccinated real)''')
# cur.execute('''INSERT INTO countries
#                (name, iso_code, population, total_vaccinated, percentage_vaccinated) VALUES
#                ('United States of America', 'USA', '328329953', '12', '0.00000365485'),
#                ('Brazilia','BRA','92746607','5000','0.00539103279'),
#                ('Holland','HOL','17441139','10000','0.05733570496 '),
#                ('Central Europe and the Baltics','OWID_CEB','102253057','500000','0.48898293573 ')''')
#
# con.commit()
# con.close()
