from typing import List

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from ap_zadacha.components.schemas import Country
from ap_zadacha.routers.utils import get_all_countries_data, delete_country_data, \
    add_country_to_db, get_country_by_id

router = APIRouter()


@router.get('/vaccinations', status_code=status.HTTP_200_OK)
async def get_all_countries() -> List[Country]:
    """Returns a list of all countries and their vaccination data."""
    countries_data = get_all_countries_data()
    return countries_data


@router.get('/vaccinations/country/{country_id}', status_code=status.HTTP_200_OK)
async def get_country_data(country_id: str) -> Country:
    """Retrieve information about specific country through the provided country ID"""
    country_data = get_country_by_id(country_id)
    if not country_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Country not found')
    return country_data


@router.post('/country')
async def create_country(payload: Country):
    """Add new country to the database. Raises error if country with the same name already exists"""
    if get_country_by_id(payload.iso_code):
        raise HTTPException(detail='Country already exists',
                            status_code=status.HTTP_409_CONFLICT)
    await add_country_to_db(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='Created')


@router.delete('/country/{country_id}')
async def delete_country(country_id: str):
    """Delete the selected country using country ID. Raises error if country does not exist"""
    if not get_country_by_id(country_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Country not found')
    await delete_country_data(country_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='Record was successfully deleted')
