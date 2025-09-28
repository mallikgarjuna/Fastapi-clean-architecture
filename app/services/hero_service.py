from fastapi import HTTPException

from app.models.hero_models import Hero, HeroCreate, HeroUpdate
from app.repositories.hero_repository import HeroRepository


class HeroService:
    def __init__(self, repo: HeroRepository) -> None:
        self.repo = repo

    def create(self, hero: HeroCreate) -> Hero:
        db_hero = Hero.model_validate(hero)
        db_hero = self.repo.create(db_hero)
        return db_hero

    def read_many(self, offset: int = 0, limit: int = 100):
        heroes = self.repo.read_many(offset, limit)
        return heroes

    def read_one(self, hero_id: int) -> Hero:
        hero = self.repo.read_one(hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero

    def update(self, hero_id: int, hero: HeroUpdate) -> Hero:
        hero_db = self.repo.read_one(hero_id)
        if not hero_db:
            raise HTTPException(status_code=404, detail="Hero not found")
        hero_data = hero.model_dump(exclude_unset=True)
        hero_db = self.repo.update(hero_db, hero_data)

        return hero_db

    def delete(self, hero_id: int) -> None:
        hero = self.repo.read_one(hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        self.repo.delete(hero)
