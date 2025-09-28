from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.db import engine
from app.repositories.hero_repository import HeroRepository
from app.services.hero_service import HeroService


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_hero_repository(session: SessionDep) -> HeroRepository:
    return HeroRepository(session=session)


HeroRepoDep = Annotated[HeroRepository, Depends(get_hero_repository)]


def get_hero_service(repo: HeroRepoDep) -> HeroService:
    return HeroService(repo=repo)


HeroServiceDep = Annotated[HeroService, Depends(get_hero_service)]
