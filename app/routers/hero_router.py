from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db import get_session
from app.dependencies import SessionDep
from app.models.hero_models import Hero, HeroCreate, HeroPublic, HeroUpdate
from app.services.hero_service import (
    create_hero_service,
    delete_hero_service,
    read_hero_service,
    read_heroes_service,
    update_hero_service,
)

router = APIRouter()


@router.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = create_hero_service(hero, session)
    return db_hero


@router.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = read_heroes_service(session, offset, limit)
    return heroes


@router.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = read_hero_service(hero_id, session)
    return hero


@router.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = update_hero_service(hero_id, hero, session)
    return hero_db


@router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    delete_hero_service(hero_id, session)
    return {"ok": True}
