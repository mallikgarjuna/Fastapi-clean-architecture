from sqlmodel import Session, select

from app.models.hero_models import Hero


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

    def update(self, hero_db: Hero, hero_data: dict) -> Hero:
        hero_db.sqlmodel_update(hero_data)
        self.session.add(hero_db)
        self.session.commit()
        self.session.refresh(hero_db)
        return hero_db

    def delete(self, hero) -> None:
        self.session.delete(hero)
        self.session.commit()
