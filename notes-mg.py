# tests/services/test_hero_service.py
# Unit tests for app.services.hero_service.HeroService
# We use pytest + pytest-mock (mocker fixture) to replace the repository with a mock.

import pytest  # used for raises/assert helpers

from app.models.hero_models import Hero, HeroCreate, HeroUpdate  # models used in tests
from app.repositories.hero_repository import HeroRepository  # used as spec for mock
from app.services.hero_service import HeroService  # class under test


def make_hero_instance(
    id: int = 1, name: str = "Deadpond", secret_name: str = "Dive Wilson"
):
    # Helper to build a Hero instance quickly for return values from mocks.
    # Using the actual SQLModel `Hero` here makes assertions simple (attributes exist).
    return Hero(id=id, name=name, secret_name=secret_name, age=None, gender=None)


def test_create_calls_repo_and_returns_hero(mocker):
    # Arrange -------------------------------------------------------------
    # Create a mock repo that only exposes the methods of HeroRepository
    repo_mock = mocker.Mock(spec=HeroRepository)  # typed mock for safety
    fake_db_hero = make_hero_instance()  # what repo.create should return

    # Patch Hero.model_validate (called by service.create) so it returns our fake instance
    # This isolates the service logic from Pydantic/SQLModel internals.
    mocker.patch.object(Hero, "model_validate", return_value=fake_db_hero)

    # Configure repo mock to return fake_db_hero when create(...) is called
    repo_mock.create.return_value = fake_db_hero

    # Instantiate service with the mocked repo
    service = HeroService(repo=repo_mock)

    # Create an input object matching the service signature
    hero_in = HeroCreate(name="Deadpond", secret_name="Dive Wilson")

    # Act -----------------------------------------------------------------
    result = service.create(hero_in)  # call the service method

    # Assert --------------------------------------------------------------
    repo_mock.create.assert_called_once_with(
        fake_db_hero
    )  # repo.create called with model_validate result
    assert result is fake_db_hero  # service returns the repo result


def test_read_many_returns_list(mocker):
    # Arrange -------------------------------------------------------------
    repo_mock = mocker.Mock(spec=HeroRepository)  # mock repo
    repo_mock.read_many.return_value = [
        make_hero_instance(id=1),
        make_hero_instance(id=2),
    ]
    service = HeroService(repo=repo_mock)

    # Act -----------------------------------------------------------------
    result = service.read_many(offset=0, limit=10)

    # Assert --------------------------------------------------------------
    repo_mock.read_many.assert_called_once_with(0, 10)  # verify args passed through
    assert isinstance(result, list)  # result is a list
    assert len(result) == 2


def test_read_one_success(mocker):
    # Arrange -------------------------------------------------------------
    repo_mock = mocker.Mock(spec=HeroRepository)
    hero = make_hero_instance(id=123)
    repo_mock.read_one.return_value = hero
    service = HeroService(repo=repo_mock)

    # Act -----------------------------------------------------------------
    result = service.read_one(123)

    # Assert --------------------------------------------------------------
    repo_mock.read_one.assert_called_once_with(123)
    assert result is hero  # same object returned


def test_read_one_not_found_raises(mocker):
    # Arrange -------------------------------------------------------------
    repo_mock = mocker.Mock(spec=HeroRepository)
    repo_mock.read_one.return_value = None  # simulate not found
    service = HeroService(repo=repo_mock)

    # Act / Assert --------------------------------------------------------
    with pytest.raises(Exception) as excinfo:
        service.read_one(999)

    # service raises a FastAPI HTTPException with 404
    assert excinfo.type.__name__ == "HTTPException"
    assert getattr(excinfo.value, "status_code") == 404
    assert getattr(excinfo.value, "detail") == "Hero not found"


def test_update_success(mocker):
    # Arrange -------------------------------------------------------------
    repo_mock = mocker.Mock(spec=HeroRepository)
    hero_db = make_hero_instance(id=10)
    repo_mock.read_one.return_value = hero_db  # existing DB object
    repo_mock.update.return_value = hero_db  # update returns the same object

    # Create a mock for HeroUpdate that provides model_dump(exclude_unset=True)
    hero_update = mocker.Mock(spec=HeroUpdate)
    hero_update.model_dump.return_value = {
        "secret_name": "Updated Name"
    }  # what service will pass to repo.update

    service = HeroService(repo=repo_mock)

    # Act -----------------------------------------------------------------
    result = service.update(10, hero_update)

    # Assert --------------------------------------------------------------
    repo_mock.read_one.assert_called_once_with(10)
    repo_mock.update.assert_called_once_with(hero_db, {"secret_name": "Updated Name"})
    assert result is hero_db


def test_update_not_found_raises(mocker):
    # Arrange -------------------------------------------------------------
    repo_mock = mocker.Mock(spec=HeroRepository)
    repo_mock.read_one.return_value = None  # hero not in DB
    hero_update = mocker.Mock(spec=HeroUpdate)
    hero_update.model_dump.return_value = {"secret_name": "x"}
    service = HeroService(repo=repo_mock)

    # Act / Assert --------------------------------------------------------
    with pytest.raises(Exception) as excinfo:
        service.update(123, hero_update)

    assert excinfo.type.__name__ == "HTTPException"
    assert getattr(excinfo.value, "status_code") == 404


def test_delete_success_and_not_found(mocker):
    # Arrange & success case ----------------------------------------------
    repo_mock = mocker.Mock(spec=HeroRepository)
    hero_db = make_hero_instance(id=1)
    repo_mock.read_one.return_value = hero_db
    service = HeroService(repo=repo_mock)

    # Act: delete existing
    service.delete(1)

    # Assert: delete called with the object
    repo_mock.delete.assert_called_once_with(hero_db)

    # Arrange: not-found case
    repo_mock.read_one.return_value = None

    # Act / Assert: delete should raise HTTPException for missing hero
    with pytest.raises(Exception) as excinfo:
        service.delete(999)

    assert excinfo.type.__name__ == "HTTPException"
    assert getattr(excinfo.value, "status_code") == 404
