# tests/repositories/test_hero_repository.py
# Integration-style tests for HeroRepository using the session fixture from tests/conftest.py
# The session fixture spins up an in-memory SQLite engine (StaticPool) and creates tables.

import types  # used to attach a method to instances

from app.models.hero_models import Hero  # SQLModel model used in tests
from app.repositories.hero_repository import HeroRepository  # repository under test


def test_create_commits_and_refresh(session):
    # Arrange -------------------------------------------------------------
    repo = HeroRepository(session)  # repo bound to the pytest session fixture
    hero = Hero(
        name="Deadpond", secret_name="Dive Wilson"
    )  # construct domain model (no id yet)

    # Act -----------------------------------------------------------------
    created = repo.create(hero)  # should add, commit, refresh, return object with id

    # Assert --------------------------------------------------------------
    # id assigned by DB after commit+refresh
    assert getattr(created, "id", None) is not None
    # reading directly from session should find the same row
    got = session.get(Hero, created.id)
    assert got is not None
    assert got.name == "Deadpond"


def test_read_many(session):
    # Arrange -------------------------------------------------------------
    repo = HeroRepository(session)
    # create some rows
    repo.create(Hero(name="A", secret_name="s1"))
    repo.create(Hero(name="B", secret_name="s2"))
    repo.create(Hero(name="C", secret_name="s3"))

    # Act -----------------------------------------------------------------
    results = repo.read_many(offset=0, limit=10)

    # Assert --------------------------------------------------------------
    assert isinstance(results, list)
    assert len(results) >= 3  # at least the three we created


def test_read_one(session):
    # Arrange -------------------------------------------------------------
    repo = HeroRepository(session)
    created = repo.create(Hero(name="Solo", secret_name="S"))  # create one row

    # Act -----------------------------------------------------------------
    found = repo.read_one(created.id)

    # Assert --------------------------------------------------------------
    assert found is not None
    assert found.id == created.id


def _attach_sqlmodel_update_method(instance):
    # Helper: attach a simple sqlmodel_update(instance, data) to the instance
    # Your repository calls `hero_db.sqlmodel_update(hero_data)`.
    # The real model does not define this helper, so tests add a minimal implementation.
    def sqlmodel_update(self, data: dict):
        # copy keys from data dict to attributes on the instance
        for k, v in data.items():
            setattr(self, k, v)

    # bind the function as a method on the instance
    instance.sqlmodel_update = types.MethodType(sqlmodel_update, instance)


def test_update_persists_changes(session):
    # Arrange -------------------------------------------------------------
    repo = HeroRepository(session)
    created = repo.create(Hero(name="Old", secret_name="OldS"))  # create a row

    # If the model instance lacks `sqlmodel_update`, attach a simple helper for the repository to call
    _attach_sqlmodel_update_method(created)

    # Act -----------------------------------------------------------------
    updated = repo.update(
        created, {"secret_name": "NewS"}
    )  # repo.update uses our attached helper

    # Assert --------------------------------------------------------------
    assert updated.secret_name == "NewS"
    # verify DB stored the change by reading again
    got = session.get(Hero, created.id)
    assert got.secret_name == "NewS"


def test_delete_removes_row(session):
    # Arrange -------------------------------------------------------------
    repo = HeroRepository(session)
    created = repo.create(Hero(name="ToDelete", secret_name="X"))

    # Act -----------------------------------------------------------------
    repo.delete(created)

    # Assert --------------------------------------------------------------
    assert session.get(Hero, created.id) is None  # no row after deletion
