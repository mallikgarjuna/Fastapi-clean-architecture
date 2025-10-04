from fastapi.testclient import TestClient

from app.main import app


def test_create_hero():
    client = TestClient(app=app)

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
