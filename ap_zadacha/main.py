from fastapi import FastAPI
import uvicorn

from ap_zadacha.routers.countries import router

app = FastAPI()

app.include_router(router=router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')