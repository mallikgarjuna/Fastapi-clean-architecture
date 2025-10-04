from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from app.dependencies import get_session
from app.main import app


def test_create_hero():
    test_filename = "testing.db"
    project_root = Path(__file__).resolve().parent.parent.parent
    test_file_path = project_root / test_filename
    sqlite_url = f"sqlite:///{test_file_path}"

    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app=app)

        response = client.post(
            "/heroes",
            json={"name": "Deadpond", "secret_name": "Dive Wilson"},
        )
        app.dependency_overrides.clear()

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
