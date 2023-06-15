from typing import List

from fastapi import HTTPException, status

from ap_zadacha.components.schemas import Country
from ap_zadacha.db.database_utils import CountriesDatabase
from ap_zadacha.db.prepare import DB_FILENAME


def get_all_countries_data() -> List[Country]:
    data = []
    with CountriesDatabase(DB_FILENAME) as cursor:
        cursor.execute('''SELECT * FROM countries''')
        countries_data = cursor.fetchall()
        for country in countries_data:
            data.append(Country(**country))
    return data


def get_single_country_data(country_id) -> Country:
    with CountriesDatabase(DB_FILENAME) as cursor:
        cursor.execute('''SELECT * FROM countries WHERE id = ?''', (country_id, ))
        country_data = cursor.fetchone()
        if not country_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Country(**country_data)
