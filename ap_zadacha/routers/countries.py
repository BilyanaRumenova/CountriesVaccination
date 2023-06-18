from typing import List

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse

from ap_zadacha.components.schemas import Country
from ap_zadacha.db.database_utils import CountriesDatabase
from ap_zadacha.routers.utils import get_all_countries_data, delete_country_data, \
    add_country_to_db, get_country_by_id

router = APIRouter()


def get_database() -> CountriesDatabase:
    return CountriesDatabase()


@router.get('/vaccinations', status_code=status.HTTP_200_OK)
async def get_all_countries(db: CountriesDatabase = Depends(get_database)) -> List[Country]:
    """Returns a list of all countries and their vaccination data."""
    countries_data = get_all_countries_data(db)
    return countries_data


@router.get('/vaccinations/country/{country_id}', status_code=status.HTTP_200_OK)
async def get_country_data(country_id: str, db: CountriesDatabase = Depends(get_database)) -> Country:
    """Retrieve information about specific country through the provided country ID"""
    country_data = get_country_by_id(country_id, db)
    if not country_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Country not found')
    return country_data


@router.post('/country')
async def create_country(payload: Country, db: CountriesDatabase = Depends(get_database)):
    """Add new country to the database. Raises error if country with the same name already exists"""
    if get_country_by_id(payload.iso_code, db):
        raise HTTPException(detail='Country already exists',
                            status_code=status.HTTP_409_CONFLICT)
    await add_country_to_db(payload, db)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='Created')


@router.delete('/country/{country_id}')
async def delete_country(country_id: str, db: CountriesDatabase = Depends(get_database)):
    """Delete the selected country using country ID. Raises error if country does not exist"""
    if not get_country_by_id(country_id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Country not found')
    await delete_country_data(country_id, db)
    return JSONResponse(status_code=status.HTTP_200_OK, content='Record was successfully deleted')
