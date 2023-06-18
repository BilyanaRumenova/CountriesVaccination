# Data Ingestion

## FastAPI applications that extracts data from csv files about countries, their population and vaccination rates.
1. Each time the app is started, an event is triggered that checks whether the table `countries` exists and if not, it is created and populated with a couple of records.
2. If we want to populate the table with the values from csv files, and endpoint called `/import` is created.
   - From the country populations data [data/country_populations.csv](./data/country_populations.csv) each country population for 2020 (each one, that DOESN'T start with an "OWID\_" prefix) is extracted.
   - From the vaccinations data file [data/vaccinations.csv](./data/vaccinations.csv) the fully vaccinated population (`people_fully_vaccinated` column) for each of the countries defined in [data/country_populations.csv](./data/country_populations.csv) is extracted (without the regions defined with the "OWID\_" prefix). The columns iso_code / Country Code are used. The data for countries that are not included in the vaccinations file is filled with zeros (0).
3. The extracted information is stored/written in the table `countries`, following this structure:

```
Table 'countries':
iso_code (text), name (text), population (int), total_vaccinated (int), percentage_vaccinated(real)
```

**Notes:**

- [prepare.py](db/prepare.py) creates a `sqlite3` table with a couple of records.
- The predefined records are left intact, only their values for population, total_vaccinated and percentage_vaccinated are updated when `/import` endpoint is hit.
- Unit tests are provided as well.

## REST API

Create REST API:

- The application follows the architecture described in the [api.yaml](./api.yml).
- For implementation of the task is used FastAPI framework

Steps to install dependencies and run the task:
- run `cd ap_zadacha/`
- run `poetry install`
- for starting up the app: `uvicorn main:app --reload`
- navigate to `localhost:8000/docs`
- for running the tests: `poetry run pytest`
- in order to populate the table with data from csv files, hit endpoint `/import`

