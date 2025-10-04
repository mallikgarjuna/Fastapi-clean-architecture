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


def test_create_hero(client: TestClient):
    response = client.post(
        "/heroes",
        json={"name": "Deadpond", "secret_name": "Dive Wilson"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpond"
    # create_hero() returns HeroPublic which doesn't have 'secret_name';
    # assert data["secret_name"] == "Dive Wilson" # raises KeyError
    # assert data["secret_name"] is None  # raises KeyError
    # check that "secret_name" doesn’t exist in the dictionary:
    assert "secret_name" not in data  # key must not exist
    # or
    assert data.get("secret_name") is None  # key may be missing or explicitly null
    assert data["age"] is None
    assert data["gender"] is None
    assert data["id"] is not None
