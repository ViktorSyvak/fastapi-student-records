import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import models
from database import Base, get_db
from main import app


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# this is a helper, and this will automatically create a test user
# logs the user in 
# gets the JWT token and 
# returns the Authorization header

def get_auth_headers():
    user_data = {
        "username": "testuser",
        "password": "password123"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data = {
            "username": "testuser",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

def get_admin_headers():
    headers = get_auth_headers()

    db = TestingSessionLocal()

    user = db.query(models.UserModel).filter(
        models.UserModel.username == "testuser"
    ).first()

    user.is_admin = True

    db.commit()
    db.close()

    return headers


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Student Records System API"
    }


def test_get_students():
    response = client.get("/students")

    assert response.status_code == 200
    assert response.json() == []


def test_create_student():
    headers = get_admin_headers()
    student_data = {
        "name": "Michael Ryan",
        "age": 21,
        "course": "Computing",
        "grade": 3.5,
        "year": 3
    }


    response = client.post(
        "/students", 
        json=student_data,
        headers=headers
    )

    assert response.status_code == 201
    data = response.json() 

    assert data["name"] == "Michael Ryan"
    assert data["age"] == 21 
    assert data["course"] == "Computing"
    assert data["grade"] == 3.5
    assert data["year"] == 3 
    assert "id" in data


def test_get_student_by_id():
    headers = get_admin_headers()
    student_data = {
        "name": "Emma Murphy", 
        "age": 22, 
        "course": "Computing", 
        "grade": 3.8,
        "year": 4
    }

    create_response = client.post(
        "/students",
        json=student_data,
        headers=headers
    )

    student_id = create_response.json()["id"]

    response = client.get(f"/students/{student_id}")

    assert response.status_code == 200

    data = response.json() 
    assert data["id"] == student_id 
    assert data["name"] == "Emma Murphy"
    assert data["course"] == "Computing"

def test_student_not_found():
    response = client.get("/students/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student not found"
    }

def test_invalid_student():
    headers = get_admin_headers()

    invalid_student = {
        "name": "", 
        "age": -5,
        "course": "", 
        "grade": 10.0,
        "year": 8
    }

    response = client.post(
        "/students",
        json=invalid_student,
        headers=headers
    )

    assert response.status_code == 422

def test_update_student():
    headers = get_admin_headers()


    student_data = {
        "name": "Emma Murphy",
        "age": 22,
        "course": "Computing",
        "grade": 3.5,
        "year": 3
    }

    create_response = client.post(
        "/students",
        json=student_data,
        headers=headers
    )

    student_id = create_response.json()["id"]

    updated_data = {
        "name": "Emma Murphy",
        "age": 23,
        "course": "Computing",
        "grade": 3.9,
        "year": 4
    }

    response = client.put(
        f"/students/{student_id}",
        json=updated_data,
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student_id
    assert data["age"] == 23
    assert data["grade"] == 3.9
    assert data["year"] == 4

def test_delete_student():
    headers = get_admin_headers()

    student_data = {
        "name": "John Smith",
        "age": 20, 
        "course": "Computing",
        "grade": 3.2, 
        "year": 2
    }

    create_response = client.post(
        "/students",
        json=student_data,
        headers=headers
    )

    student_id = create_response.json()["id"]

    response = client.delete(f"/students/{student_id}",
            headers=headers)

    assert response.status_code == 204

    get_response = client.get(f"/students/{student_id}")

    assert get_response.status_code == 404


def test_filter_students_by_year():
        headers = get_admin_headers()

        student_one = {
            "name": "Emma Murphy",
            "age": 22,
            "course": "Computing",
            "grade": 3.8,
            "year": 4
        }

        student_two = {
            "name": "John Smith",
            "age": 20,
            "course": "Computing",
            "grade": 3.1,
            "year": 2
        }

        client.post("/students", 
                    json=student_one, 
                    headers=headers)
        client.post("/students", 
                    json=student_two, 
                    headers=headers)

        response = client.get("/students?year=4")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["name"] == "Emma Murphy"
        assert data[0]["year"] == 4


def test_create_student_requires_authentication():
    student_data = {
        "name": "Daniel Kelly",
        "age": 21,
        "course": "Computing",
        "grade": 3.4,
        "year": 3
    }

    response = client.post("/students", json=student_data)

    assert response.status_code == 401 

def test_normal_user_cannot_create_student():
    headers = get_auth_headers()

    student_data = {
        "name": "Daniel Kelly",
        "age": 21,
        "course": "Computing",
        "grade": 3.4,
        "year": 3
    }

    response = client.post(
        "/students",
        json=student_data,
        headers=headers
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Admin access required"
    }