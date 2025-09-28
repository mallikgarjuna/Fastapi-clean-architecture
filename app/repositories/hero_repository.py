from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.hero_models import Hero, HeroUpdate


class HeroRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, db_hero: Hero) -> Hero:
        self.session.add(db_hero)
        self.session.commit()
        self.session.refresh(db_hero)
        return db_hero

    def read_many(self, offset: int = 0, limit: int = 100):
        heroes = self.session.exec(select(Hero).offset(offset).limit(limit)).all()
        return heroes

    def read_one(self, hero_id: int):
        hero = self.session.get(Hero, hero_id)
        return hero

    def update_repo(self, hero_db: Hero, hero_data: dict) -> Hero:
        hero_db.sqlmodel_update(hero_data)
        self.session.add(hero_db)
        self.session.commit()
        self.session.refresh(hero_db)
        return hero_db

    def delete(self, hero) -> None:
        self.session.delete(hero)
        self.session.commit()


def create_repo(db_hero, session):
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


def read_many_repo(session, offset: int = 0, limit: int = 100):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


def read_one_repo(session, hero_id: int):
    hero = session.get(Hero, hero_id)
    return hero


def update_repo(session, hero_db: Hero, hero_data: dict) -> Hero:
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


def delete_repo(session, hero) -> None:
    session.delete(hero)
    session.commit()
