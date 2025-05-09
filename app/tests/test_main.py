import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_register_user():
    response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_user():
    client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "testuser@example.com",
            "password": "password123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_create_task():
    register_response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )
    access_token = register_response.json()["access_token"]

    response = client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "priority": 1
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["priority"] == 1

def test_get_tasks():
    register_response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )
    access_token = register_response.json()["access_token"]

    client.post(
        "/tasks/",
        json={
            "title": "Test Task 1",
            "description": "This is the first test task",
            "priority": 1
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    client.post(
        "/tasks/",
        json={
            "title": "Test Task 2",
            "description": "This is the second test task",
            "priority": 2
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Test Task 1"
    assert data[1]["title"] == "Test Task 2"
