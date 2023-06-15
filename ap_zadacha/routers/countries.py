from typing import List

from fastapi import APIRouter, status, HTTPException

from ap_zadacha.components.schemas import Country
from ap_zadacha.routers.utils import get_all_countries_data, get_single_country_data

router = APIRouter()


# status code 201, descr = add new country to the database, has request body
@router.post('/country')
async def create_country():
    pass


# status code 201, descr = delete the selected country using country ID, response = record was successfully deleted
@router.delete('/country/{country_id}')
async def delete_country():
    pass


# status code 200, descr = list of all countries and their vaccinations or filter using query, returns list
@router.get('/vaccinations', status_code=status.HTTP_200_OK, description='list of all countries and their vaccinations')
async def get_all_vaccinations() -> List[Country]:
    """Returns a list with information of all countries and data about their vaccinations."""
    countries_data = get_all_countries_data()
    return countries_data


# status code 200, descr = retrieve information about specific country using the country ID, response returns list
@router.get('/vaccinations/country/{country_id}', status_code=status.HTTP_200_OK)
async def get_country_data(country_id) -> Country:
    """Retrieve information about specific country through the provided country ID"""
    country_data = get_single_country_data(country_id)
    return country_data
