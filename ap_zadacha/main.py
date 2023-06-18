from fastapi import FastAPI
import uvicorn

from ap_zadacha.db.database_utils import CountriesDatabase
from ap_zadacha.db.prepare import DB_FILENAME
from ap_zadacha.routers import countries
from ap_zadacha.routers import injection

app = FastAPI()

app.include_router(router=countries.router)
app.include_router(router=injection.router)


# Event handler to check if table countries exists and if not - creates and populates it with the
# initial values on app startup
@app.on_event("startup")
async def startup_event():
    CountriesDatabase(DB_FILENAME)
    print("Table populated")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')