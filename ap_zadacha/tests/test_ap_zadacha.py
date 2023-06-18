import os

import pytest

from ap_zadacha.db.database_utils import CountriesDatabase
from ap_zadacha.tests import __version__
from ap_zadacha.main import app
from fastapi.testclient import TestClient
from fastapi import status

client = TestClient(app)


@pytest.fixture
def setup_test_database(request):
    os.environ['ENVIRONMENT'] = 'testing'
    with CountriesDatabase() as cursor:
        # Remove existing data from the table
        cursor.execute("DROP TABLE IF EXISTS countries")
        cursor.execute(
            """
            CREATE TABLE countries (
                iso_code TEXT PRIMARY KEY,
                name TEXT,
                population INT,
                total_vaccinated INT,
                percentage_vaccinated REAL
            )
            """
        )
        cursor.connection.commit()
    request.addfinalizer(drop_test_database_table)


def drop_test_database_table():
    with CountriesDatabase() as cursor:
        cursor.execute("DROP TABLE IF EXISTS countries")
        cursor.connection.commit()


def test_version():
    assert __version__ == '0.1.0'


def test_get_all_countries_empty_list(setup_test_database):
    response = client.get("/vaccinations")
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list
    assert response.json() == []


def test_get_all_countries_non_empty_list(setup_test_database):
    with CountriesDatabase() as cursor:
        cursor.execute(
            """
            INSERT INTO countries (iso_code, name, population, total_vaccinated, percentage_vaccinated) VALUES 
            ('USA', 'United States of America', '328329953', '12', '0.00000365485'),
            ('BRA', 'Brazilia', '92746607','5000','0.00539103279')
            """
        )
        cursor.connection.commit()
    response = client.get("/vaccinations")
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list
    assert len(response.json()) == 2


def test_get_country_by_id_success(setup_test_database):
    with CountriesDatabase() as cursor:
        cursor.execute(
            """
            INSERT INTO countries (iso_code, name, population, total_vaccinated, percentage_vaccinated) VALUES 
            ('USA', 'United States of America', '328329953', '12', '0.00000365485')
            """
        )
        cursor.connection.commit()
    country_id = 'USA'
    response = client.get(f"/vaccinations/country/{country_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "name": "United States of America",
        "iso_code": "USA",
        "population": 328329953,
        "total_vaccinated": 12,
        "percentage_vaccinated": 0.00000365485
    }


def test_get_country_by_id_raises_error(setup_test_database):
    country_id = 'BGR'
    response = client.get(f"/vaccinations/country/{country_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Country not found'


def test_get_country_by_id_invalid_value(setup_test_database):
    country_id = 555
    response = client.get(f"/vaccinations/country/{country_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_country_success(setup_test_database):
    payload = {
        "name": "Jamaica",
        "iso_code": "JAM",
        "population": 2961161,
        "total_vaccinated": 164703,
        "percentage_vaccinated": 5.05
    }
    response = client.post("/country", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == "Created"


def test_create_country_already_exists_raises_error(setup_test_database):
    with CountriesDatabase() as cursor:
        cursor.execute(
            """
            INSERT INTO countries (iso_code, name, population, total_vaccinated, percentage_vaccinated) VALUES 
            ('BGR', 'Bulgaria', '6900000', '4300000', '0.00000365485')
            """
        )
        cursor.connection.commit()
    payload = {
        "name": "Bulgaria",
        "iso_code": "BGR",
        "population": 6934015,
        "total_vaccinated": 4317192,
        "percentage_vaccinated": 62.27
    }
    response = client.post("/country", json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_country_invalid_json(setup_test_database):
    payload = {
        "name": "Bulgaria",
        "iso_code": "BGR",
        "population": "invalid value",
        "total_vaccinated": 4317192,
        "percentage_vaccinated": 62.27
    }
    response = client.post("/country", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == 'value is not a valid integer'
    assert response.json()['detail'][0]['type'] == 'type_error.integer'


def test_create_country_invalid_data(setup_test_database):
    payload = {
        "name": "Bulgaria",
        "iso_code": "BGR",
        "population": 6934015,
    }
    response = client.post("/country", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][1]['msg'] == 'field required'


def test_delete_country_success(setup_test_database):
    with CountriesDatabase() as cursor:
        cursor.execute(
            """
            INSERT INTO countries (iso_code, name, population, total_vaccinated, percentage_vaccinated) VALUES 
            ('USA', 'United States of America', '328329953', '12', '0.00000365485')
            """
        )
        cursor.connection.commit()
    country_id = 'USA'
    response = client.delete(f"/country/{country_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 'Record was successfully deleted'


def test_delete_non_existing_country_raises_error(setup_test_database):
    country_id = 'BGR'
    response = client.delete(f"/country/{country_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Country not found'


def test_delete_country_invalid_value_id_type(setup_test_database):
    country_id = 555444
    response = client.delete(f"/country/{country_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
