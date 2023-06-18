import csv
from fastapi import APIRouter, status

from ap_zadacha.db.database_utils import CountriesDatabase

router = APIRouter()


@router.post("/import", status_code=status.HTTP_201_CREATED)
async def import_data_from_csv() -> dict:
    """Import data extracted from csv files into already created table countries"""
    country_populations = await extract_country_population()
    vaccinations = await extract_country_vaccination_data()

    # Populate countries table with the extracted data
    with CountriesDatabase() as cursor:
        for country_code, values in country_populations.items():
            country_name = values[0]
            population = values[1]
            total_vaccinated = vaccinations.get(country_code, 0)
            if not total_vaccinated == 0:
                percentage_vaccinated = f'{(total_vaccinated / population) * 100:.2f}'
            else:
                percentage_vaccinated = 0

            cursor.execute('''
                INSERT OR REPLACE INTO countries (iso_code, name, population, total_vaccinated, percentage_vaccinated)
                VALUES (?,?,?,?,?)''',
                           (country_code, country_name, population, total_vaccinated, percentage_vaccinated))

    return {"message": "Data imported successfully"}


async def extract_country_population():
    """Read the CSV file and extract the required data(country name, country code and population for 2020)
    from the country_populations.csv """
    country_populations = {}
    with open("data/country_populations.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            country_name = row["Country Name"]
            country_code = row["Country Code"]
            if not country_code.startswith("OWID_"):
                population = int(row["2020"]) if row["2020"] != "" else 0
                country_populations[country_code] = (country_name, population)
    return country_populations


async def extract_country_vaccination_data():
    """Read the CSV file and extract the required data from the vaccinations.csv"""
    vaccinations = {}
    with open("data/vaccinations.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            country_code = row["iso_code"]
            if not country_code.startswith("OWID_"):
                fully_vaccinated = int(row["people_fully_vaccinated"]) if row["people_fully_vaccinated"] else 0
                vaccinations[country_code] = fully_vaccinated
    return vaccinations
