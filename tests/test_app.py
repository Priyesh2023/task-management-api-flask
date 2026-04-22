import sys
import os
import pytest

# Project root path add
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client


# 1. Register Test
def test_register(client):
    response = client.post("/register", json={
        "name": "Test User",
        "email": "test@gmail.com",
        "password": "1234"
    })

    assert response.status_code == 201


# 2. Login Test
def test_login(client):
    client.post("/register", json={
        "name": "Test User",
        "email": "test@gmail.com",
        "password": "1234"
    })

    response = client.post("/login", json={
        "email": "test@gmail.com",
        "password": "1234"
    })

    assert response.status_code == 200
    assert "token" in response.get_json()


# 3. Create Task Test
def test_create_task(client):
    client.post("/register", json={
        "name": "User1",
        "email": "user1@gmail.com",
        "password": "1234"
    })

    login = client.post("/login", json={
        "email": "user1@gmail.com",
        "password": "1234"
    })

    token = login.get_json()["token"]

    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Testing"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201


# 4. Get Tasks Test
def test_get_tasks(client):
    client.post("/register", json={
        "name": "User2",
        "email": "user2@gmail.com",
        "password": "1234"
    })

    login = client.post("/login", json={
        "email": "user2@gmail.com",
        "password": "1234"
    })

    token = login.get_json()["token"]

    client.post(
        "/tasks",
        json={
            "title": "Task 1",
            "description": "Demo"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


# 5. Delete Task Test
def test_delete_task(client):
    client.post("/register", json={
        "name": "User3",
        "email": "user3@gmail.com",
        "password": "1234"
    })

    login = client.post("/login", json={
        "email": "user3@gmail.com",
        "password": "1234"
    })

    token = login.get_json()["token"]

    client.post(
        "/tasks",
        json={
            "title": "Delete Me",
            "description": "Demo"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.delete(
        "/tasks/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200