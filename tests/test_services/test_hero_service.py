from app.models.hero_models import Hero, HeroCreate
from app.repositories.hero_repository import HeroRepository
from app.services.hero_service import HeroService


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
