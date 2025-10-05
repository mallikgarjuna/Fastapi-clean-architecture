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


def test_read_many(session):
    # def read_many(self, offset: int = 0, limit: int = 100):
    #     heroes = self.session.exec(select(Hero).offset(offset).limit(limit)).all()
    #     return heroes

    # Arrange
    repo = HeroRepository(session)

    # create some rows in db
    hero_db_1 = Hero(name="Deadpond1", secret_name="Dive Wilson 1")
    hero_db_2 = Hero(name="Deadpond2", secret_name="Dive Wilson 2")
    hero_db_3 = Hero(name="Deadpond3", secret_name="Dive Wilson 3")
    repo.create(hero_db_1)
    repo.create(hero_db_2)
    repo.create(hero_db_3)

    # Act
    result = repo.read_many(offset=0, limit=100)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 3  # only 3 b/c a new session is created for every fixure call


def test_read_one(session):
    # def read_one(self, hero_id: int):
    #     hero = self.session.get(Hero, hero_id)
    #     return hero

    # Arrange
    repo = HeroRepository(session)

    # create 1 row
    hero_created = repo.create(Hero(name="Deadpond", secret_name="Dive Wilson"))

    # Act
    result = repo.read_one(hero_created.id)

    # Assert
    assert result is not None
    assert result.id == hero_created.id


def test_update(session):
    """Test update persists changes"""
    # def update(self, hero_db: Hero, hero_data: dict) -> Hero:
    #     hero_db.sqlmodel_update(hero_data)
    #     self.session.add(hero_db)
    #     self.session.commit()
    #     self.session.refresh(hero_db)
    #     return hero_db

    # Arrange
    repo = HeroRepository(session)

    # create 1 row before updating it
    hero_created = repo.create(Hero(name="Deadpond", secret_name="Dive Wilson"))

    hero_data = {"secret_name": "Updated Dive Wilson"}

    # Act
    result = repo.update(hero_created, hero_data)
    # Note: assuming `sqlmodel_update()` exists for hero_created (Hero) model
    # Can also manually implement/define this helper for hero_created instance of Hero model

    # Assert
    assert result.secret_name == "Updated Dive Wilson"  # returned result
    assert session.get(Hero, result.id).secret_name == "Updated Dive Wilson"  # stored


def test_delete(session):
    """Test delete removes row"""
    # def delete(self, hero) -> None:
    #     self.session.delete(hero)
    #     self.session.commit()

    # Arrange
    repo = HeroRepository(session)

    # create 1 row for deleting it
    hero_created = repo.create(Hero(name="Deadpond", secret_name="Dive Wilson"))

    # Act
    repo.delete(hero_created)

    # Assert
    assert session.get(Hero, hero_created.id) is None  # no row after deletion
