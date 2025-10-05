import pytest

from app.models.hero_models import Hero, HeroCreate, HeroUpdate
from app.repositories.hero_repository import HeroRepository
from app.services.hero_service import HeroService


# Unit tests for app.services.hero_service.HeroService
# 'mocker' fixture comes from `pytest-mock` plugin of `pytest` library - both installed
def test_create(mocker):
    """calls repo and returns hero"""
    # def create(self, hero: HeroCreate) -> Hero:
    #     db_hero = Hero.model_validate(hero)
    #     db_hero = self.repo.create(db_hero)
    #     return db_hero

    # Arrange
    repo_mock = mocker.Mock(spec=HeroRepository)
    service = HeroService(repo=repo_mock)
    fake_db_hero = Hero(
        id=1, name="Deadpond", secret_name="Dive Wilson", age=None, gender=None
    )

    mocker.patch.object(Hero, "model_validate", return_value=fake_db_hero)
    repo_mock.create.return_value = fake_db_hero

    hero_in = HeroCreate(name="Deadpond", secret_name="Dive Wilson")
    # Act
    result = service.create(hero_in)

    # Assert
    assert result is fake_db_hero
    repo_mock.create.assert_called_once_with(fake_db_hero)


def test_read_many(mocker):
    """calls repo and returns list of heroes"""
    # def read_many(self, offset: int = 0, limit: int = 100):
    # heroes = self.repo.read_many(offset, limit)
    # return heroes

    # Arrange
    repo_mock = mocker.Mock(spec=HeroRepository)
    repo_mock.read_many.return_value = [
        Hero(id=1, name="Deadpond", secret_name="Dive Wilson", age=None, gender=None),
        Hero(id=2, name="Deadpond", secret_name="Dive Wilson", age=None, gender=None),
    ]
    service = HeroService(repo=repo_mock)

    # Act
    result = service.read_many(offset=0, limit=100)

    # Assert
    assert len(result) == 2
    repo_mock.read_many.assert_called_once_with(0, 100)
    assert isinstance(result, list)


def test_read_one_success(mocker):
    # def read_one(self, hero_id: int) -> Hero:
    # hero = self.repo.read_one(hero_id)
    # if not hero:
    #     raise HTTPException(status_code=404, detail="Hero not found")
    # return hero

    # Arrange
    repo_mock = mocker.Mock(spec=HeroRepository)
    fake_hero = Hero(
        id=1, name="Deadpond", secret_name="Dive Wilson", age=None, gender=None
    )
    repo_mock.read_one.return_value = fake_hero
    service = HeroService(repo=repo_mock)

    # Act
    result = service.read_one(1)

    # Assert
    assert result is fake_hero
    repo_mock.read_one.assert_called_once_with(1)


def test_read_one_not_found_raises(mocker):
    # Arrange
    repo_mock = mocker.Mock(spec=HeroRepository)
    service = HeroService(repo=repo_mock)

    repo_mock.read_one.return_value = None  # simulate not found

    # Act
    with pytest.raises(Exception) as excinfo:
        service.read_one(999)  # read some random hero id

    # Assert
    assert getattr(excinfo.value, "status_code") == 404
    assert getattr(excinfo.value, "detail") == "Hero not found"
    assert excinfo.type.__name__ == "HTTPException"


def test_update_success(mocker):
    # def update(self, hero_id: int, hero: HeroUpdate) -> Hero:
    #     hero_db = self.repo.read_one(hero_id)
    #     if not hero_db:
    #         raise HTTPException(status_code=404, detail="Hero not found")
    #     hero_data = hero.model_dump(exclude_unset=True)
    #     hero_db = self.repo.update(hero_db, hero_data)

    #     return hero_db

    # Arrange
    repo_mock = mocker.Mock(spec=HeroRepository)
    service = HeroService(repo=repo_mock)

    fake_hero_db = Hero(
        id=1, name="Deadpond", secret_name="Dive Wilson", age=None, gender=None
    )
    repo_mock.read_one.return_value = fake_hero_db
    repo_mock.update.return_value = fake_hero_db

    hero_update_mock = mocker.Mock(spec=HeroUpdate)
    hero_update_mock.model_dump.return_value = {"secret_name": "Updated Name"}

    # Act
    result = service.update(1, hero_update_mock)

    # Assert
    assert result is fake_hero_db
    repo_mock.read_one.assert_called_once_with(1)
    repo_mock.update.assert_called_once_with(
        fake_hero_db, {"secret_name": "Updated Name"}
    )


def test_update_not_found_raises(mocker):
    # Arrange
    repo_mock = mocker.Mock(spec=HeroRepository)
    service = HeroService(repo=repo_mock)

    hero_update_mock = mocker.Mock(spec=HeroUpdate)

    repo_mock.read_one.return_value = None  # simulate not found

    # Act
    with pytest.raises(Exception) as excinfo:
        service.update(111, hero_update_mock)  # give random hero id

    # Assert
    assert excinfo.type.__name__ == "HTTPException"
    assert getattr(excinfo.value, "status_code") == 404


def test_delete_success_and_not_found_raises(mocker):
    # def delete(self, hero_id: int) -> None:
    #     hero = self.repo.read_one(hero_id)
    #     if not hero:
    #         raise HTTPException(status_code=404, detail="Hero not found")
    #     self.repo.delete(hero)

    # ==== ==== Success case ==== ====
    # Arrange
    repo_mock = mocker.Mock(spec=HeroRepository)
    service = HeroService(repo=repo_mock)

    fake_hero_db = Hero(
        id=1, name="Deadpond", secret_name="Dive Wilson", age=None, gender=None
    )
    repo_mock.read_one.return_value = fake_hero_db

    # Act
    service.delete(1)

    # Assert
    repo_mock.delete.assert_called_once_with(fake_hero_db)

    # ==== ==== Not Found Raises case ==== ====
    # Arrange
    repo_mock.read_one.return_value = None  # simulate not found

    # Act
    with pytest.raises(Exception) as excinfo:
        service.delete(999)  # call with random hero id

    # Assert
    assert excinfo.type.__name__ == "HTTPException"
    assert getattr(excinfo.value, "status_code") == 404
