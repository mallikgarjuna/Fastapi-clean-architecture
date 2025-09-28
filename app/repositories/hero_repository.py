from fastapi import HTTPException
from sqlmodel import select

from app.models.hero_models import Hero, HeroUpdate


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
