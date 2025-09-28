from typing import Annotated

from fastapi import HTTPException, Query
from sqlmodel import Session, select

from app.models.hero_models import Hero, HeroCreate, HeroUpdate
from app.repositories.hero_repository import (
    HeroRepository,
    create_repo,
    delete_repo,
    read_many_repo,
    read_one_repo,
    update_repo,
)


class HeroService:
    def __init__(self, repo: HeroRepository) -> None:
        self.repo = repo

    def create(self, hero: HeroCreate) -> Hero:
        db_hero = Hero.model_validate(hero)
        # db_hero = create_repo(db_hero, self.session)
        db_hero = self.repo.create(db_hero)
        return db_hero

    def read_many(self, offset: int = 0, limit: int = 100):
        # heroes = read_many_repo(self.session, offset, limit)
        heroes = self.repo.read_many(offset, limit)
        return heroes

    def read_one(self, hero_id: int) -> Hero:
        # hero = read_one_repo(self.session, hero_id)
        hero = self.repo.read_one(hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero

    def update(self, hero_id: int, hero: HeroUpdate) -> Hero:
        # hero_db = read_one_repo(self.session, hero_id)
        hero_db = self.repo.read_one(hero_id)
        if not hero_db:
            raise HTTPException(status_code=404, detail="Hero not found")
        hero_data = hero.model_dump(exclude_unset=True)
        # hero_db = update_repo(self.session, hero_db, hero_data)
        hero_db = self.repo.update(hero_db, hero_data)
        # hero_db.sqlmodel_update(hero_data)
        # self.session.add(hero_db)
        # self.session.commit()
        # self.session.refresh(hero_db)
        return hero_db

    def delete(self, hero_id: int) -> None:
        # hero = read_one_repo(self.session, hero_id)
        hero = self.repo.read_one(hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        # delete_repo(self.session, hero)
        self.repo.delete(hero)


# def create_hero_service(hero: HeroCreate, session: SessionDep):
#     db_hero = Hero.model_validate(hero)
#     session.add(db_hero)
#     session.commit()
#     session.refresh(db_hero)
#     return db_hero


# def read_heroes_service(
#     session: SessionDep,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ):
#     heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#     return heroes


# def read_hero_service(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     return hero


# def update_hero_service(hero_id: int, hero: HeroUpdate, session: SessionDep):
#     hero_db = session.get(Hero, hero_id)
#     if not hero_db:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     hero_data = hero.model_dump(exclude_unset=True)
#     hero_db.sqlmodel_update(hero_data)
#     session.add(hero_db)
#     session.commit()
#     session.refresh(hero_db)
#     return hero_db


# def delete_hero_service(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
