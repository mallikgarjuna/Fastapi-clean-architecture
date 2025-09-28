from typing import Annotated

from fastapi import APIRouter, Query

from app.dependencies import HeroServiceDep
from app.models.hero_models import HeroCreate, HeroPublic, HeroUpdate

router = APIRouter()


@router.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, service: HeroServiceDep):
    db_hero = service.create(hero)
    return db_hero


@router.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    service: HeroServiceDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = service.read_many(offset, limit)
    return heroes


@router.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, service: HeroServiceDep):
    hero = service.read_one(hero_id)
    return hero


@router.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, service: HeroServiceDep):
    hero_db = service.update(hero_id, hero)
    return hero_db


@router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, service: HeroServiceDep):
    service.delete(hero_id)
    return {"ok": True}
