from typing import List

from ap_zadacha.components.schemas import Country
from ap_zadacha.db.database_utils import CountriesDatabase


def get_all_countries_data(db: CountriesDatabase) -> List[Country]:
    data = []
    with db as cursor:
        cursor.execute('''SELECT * FROM countries ORDER BY iso_code''')
        result = cursor.fetchall()
        for country in result:
            data.append(Country(**country))
        return data


def get_country_by_id(country_id: str, db: CountriesDatabase) -> Country:
    with db as cursor:
        cursor.execute('''SELECT * FROM countries WHERE iso_code = ?''', (country_id,))
        country_data = cursor.fetchone()
        if country_data:
            return Country(**country_data)


async def delete_country_data(country_id: str, db: CountriesDatabase) -> None:
    with db as cursor:
        cursor.execute('''DELETE FROM countries WHERE iso_code = ?''', (country_id,))


async def add_country_to_db(payload: Country, db: CountriesDatabase):
    with db as cursor:
        cursor.execute('''
        INSERT INTO countries (name, iso_code, population, total_vaccinated, percentage_vaccinated) 
        VALUES (?,?,?,?,?)''',
                       (payload.name, payload.iso_code, payload.population, payload.total_vaccinated,
                        payload.percentage_vaccinated))
