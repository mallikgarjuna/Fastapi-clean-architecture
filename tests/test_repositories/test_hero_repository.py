from app.models.hero_models import Hero
from app.repositories.hero_repository import HeroRepository


# Integration style tests for HeroRepository using the `session` fixture from `tests/conftest.py`
# `session` fixture is taken from the tests/conftest.py automatically by `pytest`
def test_create(session):
    """Commits and refreshes"""
    # def create(self, db_hero: Hero) -> Hero:
    #     self.session.add(db_hero)
    #     self.session.commit()
    #     self.session.refresh(db_hero)
    #     return db_hero

    # Arrange
    repo = HeroRepository(session)
    hero_db = Hero(
        name="Deadpond", secret_name="Dive Wilson"
    )  # no id at at this stage yet

    # Act
    # with this: db should add > commit > refresh > and return hero object with id
    result = repo.create(hero_db)

    # Assert
    # id assigned by db after commit + refresh
    assert getattr(result, "id", None) is not None
    assert session.get(Hero, result.id) is not None
    assert session.get(Hero, result.id).name == "Deadpond"
    assert session.get(Hero, result.id).secret_name == "Dive Wilson"
    assert session.get(Hero, result.id).age is None  # b/c it was not set during create
