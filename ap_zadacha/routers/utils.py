from typing import List

from ap_zadacha.components.schemas import Country, CountryGet
from ap_zadacha.db.database_utils import CountriesDatabase
from ap_zadacha.db.prepare import DB_FILENAME


def get_all_countries_data() -> List[Country]:
    data = []
    with CountriesDatabase(DB_FILENAME) as cursor:
        cursor.execute('''SELECT * FROM countries''')
        result = cursor.fetchall()
        for country in result:
            data.append(Country(**country))
        return data


def get_country_by_id(country_id: str) -> Country:
    with CountriesDatabase(DB_FILENAME) as cursor:
        cursor.execute('''SELECT * FROM countries WHERE iso_code = ?''', (country_id,))
        country_data = cursor.fetchone()
        if country_data:
            return Country(**country_data)


async def delete_country_data(country_id: str) -> None:
    with CountriesDatabase(DB_FILENAME) as cursor:
        cursor.execute('''DELETE FROM countries WHERE iso_code = ?''', (country_id,))


async def add_country_to_db(payload: Country):
    with CountriesDatabase(DB_FILENAME) as cursor:
        cursor.execute('''
        INSERT INTO countries (name, iso_code, population, total_vaccinated, percentage_vaccinated) 
        VALUES (?,?,?,?,?)''',
                       (payload.name, payload.iso_code, payload.population, payload.total_vaccinated,
                        payload.percentage_vaccinated))
