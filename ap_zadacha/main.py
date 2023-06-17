from fastapi import FastAPI
import uvicorn

from ap_zadacha.routers import countries
from ap_zadacha.routers import injection

app = FastAPI()

app.include_router(router=countries.router)
app.include_router(router=injection.router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')