from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.db import engine
from app.services.hero_service import HeroService


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_hero_service(session: SessionDep) -> HeroService:
    return HeroService(session=session)


HeroServiceDep = Annotated[HeroService, Depends(get_hero_service)]
