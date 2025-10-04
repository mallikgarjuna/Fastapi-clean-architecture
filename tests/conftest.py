# NOTE:
# conftest.py is a special, conventional name in pytest
# It’s not a module you import manually; pytest automatically discovers it.
# It stores fixtures, hooks, and test configuration that you want
# to share across multiple test files.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlmodel import Session, SQLModel

from app.dependencies import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    sqlite_url = "sqlite://"  # In-memory db

    engine = create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app=app)
    yield client
    app.dependency_overrides.clear()
