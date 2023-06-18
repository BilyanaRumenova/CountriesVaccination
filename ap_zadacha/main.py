from fastapi import FastAPI
import uvicorn

from ap_zadacha.db.database_utils import CountriesDatabase
from ap_zadacha.routers import countries
from ap_zadacha.routers import ingestion

app = FastAPI()

app.include_router(router=countries.router)
app.include_router(router=ingestion.router)


@app.on_event("startup")
async def startup_event():
    """Event handler to check if table countries exists and if not - creates and populates it with the initial
    values on app startup"""
    CountriesDatabase()
    print("Table populated")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')