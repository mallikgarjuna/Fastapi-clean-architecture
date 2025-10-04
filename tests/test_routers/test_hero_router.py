import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlmodel import Session, SQLModel

from app.dependencies import get_session
from app.main import app
from app.models.hero_models import Hero


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


def test_create_hero_incomplete(client: TestClient):
    # No secret_name
    response = client.post("/heroes", json={"name": "Deadpond"})

    assert response.status_code == 422  # not 400


def test_create_hero_invalid(client: TestClient):
    response = client.post(
        "/heroes",
        json={
            "name": "Deadpond",
            "secret_name": {"message": "This is a wrong data type for secret_name."},
        },
    )

    assert response.status_code == 422


def test_read_heroes(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpon", secret_name="Dive Wilson")
    hero_2 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    session.add(hero_1)
    session.add(hero_2)
    session.commit()

    response = client.get("/heroes")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == hero_1.name
    # assert data[0]["secret_name"] == hero_1.secret_name
    assert data[0].get("secret_name") is None
    assert "secret_name" not in data[0]
    assert data[0]["age"] == hero_1.age
    assert data[0]["gender"] == hero_1.gender
    assert data[0]["id"] == hero_1.id
    assert data[1]["name"] == hero_2.name
    # assert data[1]["secret_name"] == hero_2.secret_name
    assert data[1].get("secret_name") is None
    assert "secret_name" not in data[1]
    assert data[1]["age"] == hero_2.age
    assert data[1]["gender"] == hero_2.gender
    assert data[1]["id"] == hero_2.id


def test_read_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.get(f"/heroes/{hero_1.id}")
    data = response.json()

    assert response.status_code == 200

    assert data["name"] == "Deadpond"
    assert data.get("secret_name") is None
    assert "secret_name" not in data
    assert data["age"] == hero_1.age
    assert data["gender"] == hero_1.gender
    assert data["id"] == hero_1.id


def test_update_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.patch(f"/heroes/{hero_1.id}", json={"name": "Deadpuddle"})
    data = response.json()

    assert response.status_code == 200

    assert data["name"] == "Deadpuddle"
    assert data.get("secret_name") is None
    assert "secret_name" not in data
    assert data["age"] == hero_1.age
    assert data.get("age") == hero_1.age
    assert data.get("age") is None
    assert data.get("id") == hero_1.id


def test_delete_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.delete(f"/heroes/{hero_1.id}")

    hero_in_db = session.get(Hero, hero_1.id)
    assert response.status_code == 200
    assert hero_in_db is None
