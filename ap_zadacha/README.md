# CountriesVaccination

## Data Ingestion

A REST API application that extracts data from csv files about countries populations and statistics about their vaccination rates:
1. When starting up the application, an event handler is triggered that checks whether the table `countries` exists and if not, it is created and populated with some initial values. 
2. In order to ingest more data into `countries` table, we need to hit endpoint called `/import` which:
    - From the country population data [data/country_populations.csv](./data/country_populations.csv) each country population (everyone, that DON'T start with an "OWID\_" prefix) for 2020 is exported.
    - From the vaccination data file [data/vaccinations.csv](./data/vaccinations.csv) the fully vaccinated population (`people_fully_vaccinated` column) for each of the countries defined in [data/country_populations.csv](./data/country_populations.csv) (without the regions defined with the "OWID\_" prefix) is exported. The columns iso_code / Country Code are used for this purpose. If there are countries that are not included in the vaccinations file their data is filled with zeros (0).
    - The extracted information is stored in the table `countries`, following this structure:
```
Table 'countries':
iso_code (text), name (text), population (int), total_vaccinated (int), percentage_vaccinated(real)
```

**Notes:**

- [prepare.py](db/prepare.py) creates a `sqlite3` table with couple of records. It is used when starting up the application.
- The predefined records are left intact, only their values for population, total_vaccinated and percentage_vaccinated are updated when we hit `/import`.
- Unit tests are provided as well.

## REST API

Create REST API:

- the architecture is the REST API is described in the [api.yaml](./api.yml).
- the implementation is made using FastAPI framework

## STARTING UP THE APP

1. First step: 
    - `cd ap_zadacha/`
    
2. In order to install dependencies: 
   - run `poetry install`

3. For starting up the FastAPI app:
    - run `uvicorn main:app --reload`

4. For running the tests:
    - run `poetry run pytest`
    
