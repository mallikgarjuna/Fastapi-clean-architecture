from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from app.db import create_db_and_tables, get_session
from app.models.hero_models import Hero, HeroCreate, HeroPublic, HeroUpdate
from app.routers import hero_router

app = FastAPI()

app.include_router(hero_router.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
