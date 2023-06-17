import pytest

from ap_zadacha.db.database_utils import CountriesDatabase
from ap_zadacha.main import app
from ap_zadacha.tests import __version__
from fastapi.testclient import TestClient
from fastapi import status
import sqlite3


# Test database configuration
@pytest.fixture(scope="function")
def setup_database():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            name TEXT UNIQUE, iso_code TEXT, population INT, total_vaccinated INT, percentage_vaccinated real
        )
        """
    )
    yield conn


@pytest.fixture(scope='function')
def setup_test_data(setup_database):
    cursor = setup_database.cursor()
    cursor.execute("""
            INSERT INTO countries (name, iso_code, population, total_vaccinated, percentage_vaccinated)
            VALUES ('Aruba', 'ABW', 168196, 106766, 81.69), ('Bulgaria', 'BGR', 6900000, 1200000, 30.00)
            """)
    yield cursor


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client


def test_version():
    assert __version__ == '0.1.0'


def test_get_all_countries(client, setup_test_data):
    response = client.get("/vaccinations")
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list
    assert len(response.json()) == 2


def test_get_all_countries_empty_list(client):
    response = client.get("/vaccinations")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_country_by_id_success(client, setup_database):
    country_id = 2
    response = client.get(f"/vaccinations/country/{country_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == 'Bulgaria'
    assert response.json()['iso_code'] == 'BGR'


def test_get_country_by_id_raises_error(client, setup_database):
    country_id = 5
    response = client.get(f"/vaccinations/country/{country_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Country not found'


def test_get_country_by_id_invalid_value(client, setup_database):
    country_id = 'test'
    response = client.get(f"/vaccinations/country/{country_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "value is not a valid integer"


def test_create_country_success(client, setup_database):
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


def test_create_country_already_exists_raises_error(client, setup_database):
    payload = {
        "name": "Bulgaria",
        "iso_code": "BGR",
        "population": 6934015,
        "total_vaccinated": 4317192,
        "percentage_vaccinated": 62.27
    }
    response = client.post("/country", json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Country already exists"


def test_create_country_invalid_json(client):
    payload = {
        "name": "Bulgaria",
        "iso_code": "BGR",
        "population": 6934015,
    }
    response = client.post("/country", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_country_success(client, setup_database):
    country_id = 1
    response = client.delete(f"/country/{country_id}")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == 'Record was successfully deleted'


def test_delete_non_existing_country_raises_error(client):
    country_id = 555555
    response = client.delete(f"/country/{country_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Country not found'


def test_delete_country_invalid_value_id_type(client):
    country_id = 'test'
    response = client.delete(f"/country/{country_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "value is not a valid integer"
