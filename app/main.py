import logging

from fastapi import FastAPI

from app.db import create_db_and_tables
from app.routers import hero_router

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s | %(levelname)s : %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()
logger.info("API is ready.")

app.include_router(hero_router.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    logger.info("Connected database and created tables.")
