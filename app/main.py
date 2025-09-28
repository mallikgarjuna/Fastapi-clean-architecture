from fastapi import FastAPI

from app.db import create_db_and_tables
from app.routers import hero_router

app = FastAPI()

app.include_router(hero_router.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
