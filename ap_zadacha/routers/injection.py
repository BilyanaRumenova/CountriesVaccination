from typing import List
import csv
from fastapi import APIRouter, status, HTTPException
import sqlite3

router = APIRouter()
#
# # Connect to the database
# conn = sqlite3.connect("mydatabase.db")
# cursor = conn.cursor()
#
# # Create the table if it doesn't exist
# cursor.execute(
#     """
#     CREATE TABLE IF NOT EXISTS population_vaccinations (
#         country TEXT PRIMARY KEY,
#         country_code TEXT,
#         total_population INTEGER
#     )
#     """
# )
# conn.commit()


# Endpoint
@router.get("/import")
def import_data():
    # Read the CSV file and extract the required data
    country_populations = {}
    with open("data/country_populations.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            country_name = row["Country Name"]
            country_code = row["Country Code"]
            if not country_code.startswith("OWID_"):
                population = int(row["2020"]) if row["2020"] != "" else 0
                country_populations[country_code] = (country_name, population)
    print(len(country_populations))

    # Read vaccinations data
    vaccinations = {}
    with open("data/vaccinations.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            country_code = row["iso_code"]
            if not country_code.startswith("OWID_"):
                fully_vaccinated = int(row["people_fully_vaccinated"]) if row["people_fully_vaccinated"] else 0
                vaccinations[country_code] = fully_vaccinated
    print(len(vaccinations))

    # Populate the table
    for country_code, values in country_populations.items():
        fully_vaccinated = vaccinations.get(country_code, 0)
        #TODO need to be calculated
        percentage_vaccinated = ''
        cursor.execute(
            "INSERT INTO countries (name, iso_code, population, total_vaccinated, percentage_vaccinated) "
            "VALUES (?, ?, ?, ?, ?)",
            (values[0], country_code, values[1], fully_vaccinated, percentage_vaccinated),
        )
    conn.commit()

    return {"message": "Data imported successfully"}

# # Endpoint
# @router.get("/population_vaccinations")
# def get_population_vaccinations():
#     cursor.execute("SELECT * FROM population_vaccinations")
#     result = cursor.fetchall()
#
#     data = [{"country": row[0], "total_population": row[1], "fully_vaccinated": row[2]} for row in result]
#     return {"data": data}