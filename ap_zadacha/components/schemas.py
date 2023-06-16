from pydantic import BaseModel


class Country(BaseModel):
    name: str
    iso_code: str
    population: int
    total_vaccinated: int
    percentage_vaccinated: float


class CountryGet(Country):
    id: int
