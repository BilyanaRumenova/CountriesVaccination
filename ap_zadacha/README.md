# Task

## Data Ingestion

1. From the country populations data [data/country_populations.csv](./data/country_populations.csv) export each country population (everyone, that DON'T start with an "OWID\_" prefix) for 2020.
2. From the vaccinations data file [data/vaccinations.csv](./data/vaccinations.csv) export the fully vaccinated population (`people_fully_vaccinated` column) for each of the countries defined in [data/country_populations.csv](./data/country_populations.csv) (without the regions defined with the "OWID\_" prefix). Use the coulmns - iso_code / Country Code. If there are countries that are not included in the vaccinations file fill their data with zeros (0).
3. Store/ write the information in the given table, following the predefined structure of the table:

```
Table 'countries':
name (text), iso_code (text), population (int), total_vaccinated (int), percentage_vaccinated(real)
```

**Notes:**

- [prepare.py](db/prepare.py) creates a `sqlite3` table with couple of records.

**Bonus:**

- Try to leave the predefined records intact, while just updating their values for population, total_vaccinated and percentage_vaccinated.
- Write tests cases for your code.

## REST API

Create REST API:

- using the architecture described in the [api.yaml](./api.yml).
- use Flask framework for the implementation

**Bonus:**

- find the invalid responses in the API architecture
- think about responses which are missing in the API architecture
- Write tests cases for your code.
