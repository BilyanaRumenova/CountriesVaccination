from pydantic import BaseModel


class Country(BaseModel):
    name: str
    iso_code: str
    population: int
    total_vaccinated: int
    percentage_vaccinated: float

    class Config:
        schema_extra = {
            "example": {
                "name": "Chile",
                "iso_code": "CHL",
                "population": 19116209,
                "total_vaccinated": 17283367,
                "percentage_vaccinated": 90.41,
            }
        }
