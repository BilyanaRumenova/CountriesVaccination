import pytest
from ap_zadacha.main import app
from ap_zadacha.routers.utils import get_country_by_name
from ap_zadacha.tests import __version__
from fastapi.testclient import TestClient
from fastapi import status
from sqlmodel.pool import StaticPool
from sqlmodel import create_engine, SQLModel, Session

# client = TestClient(app)


# @pytest.fixture(scope="session", name="session")
# def session_fixture():
#     engine = create_engine(
#         "sqlite:///testing.db", connect_args={"check_same_thread": False}, poolclass=StaticPool
#     )
#     SQLModel.metadata.create_all(engine)
#     with Session(engine) as session:
#         yield session
#
#
# @pytest.fixture(scope="function")
# def db(session_fixture):
#     connection = session_fixture.connect()
#     # begin a non-ORM transaction
#     transaction = connection.begin()
#     # bind an individual Session to the connection
#     db = Session(bind=connection)
#     yield db
#
#     db.rollback()
#     connection.close()


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


def test_version():
    assert __version__ == '0.1.0'


def test_get_all_countries(client):
    response = client.get("/vaccinations")
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_country_by_id_success(client):
    country_id = 2
    response = client.get(f"/vaccinations/country/{country_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == 'Brazilia'
    assert response.json()['iso_code'] == 'BRA'


def test_get_country_by_id_raises_error(client):
    country_id = 5
    response = client.get(f"/vaccinations/country/{country_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Country not found'


def test_get_country_by_id_invalid_value(client):
    country_id = 'test'
    response = client.get(f"/vaccinations/country/{country_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_country_success(client):
    payload = {
        "name": "JamaicaJJJJJJ",
        "iso_code": "JAM",
        "population": 2961161,
        "total_vaccinated": 164703,
        "percentage_vaccinated": 5.05
    }
    response = client.post("/country", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == "Created"


def test_create_country_already_exists_raises_error(client):
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


def test_delete_country_success(client):
    payload = {
        "name": "JamaicaJJJJJJ",
        "iso_code": "JAM",
        "population": 2961161,
        "total_vaccinated": 164703,
        "percentage_vaccinated": 5.05
    }
    client.post("/country", json=payload)
    country = get_country_by_name(payload["name"])
    country_id = country.id
    response = client.delete(f"/country/{country_id}")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == 'Record was successfully deleted'


def test_delete_non_existing_country_raises_error(client):
    country_id = 555555555
    response = client.delete(f"/country/{country_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Country not found'


def test_delete_country_invalid_value_id_type(client):
    country_id = 'test'
    response = client.delete(f"/country/{country_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
