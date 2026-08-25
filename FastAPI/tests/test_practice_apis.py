from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from app.apis import practice_apis
from app.main import app


user_list = practice_apis.user_list
INITIAL_USERS = deepcopy(user_list)
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_user_list() -> None:
    user_list.clear()
    user_list.extend(deepcopy(INITIAL_USERS))
    practice_apis._next_user_id = max(user["id"] for user in user_list) + 1


def test_get_users_hides_passwords() -> None:
    response = client.get("/practice_api/users")

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert all("password" not in user for user in response.json())


def test_get_user() -> None:
    response = client.get("/practice_api/users/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "홍길동",
        "age": 24,
        "email": "gildong24@example.com",
    }


def test_get_unknown_user_returns_404() -> None:
    response = client.get("/practice_api/users/999")

    assert response.status_code == 404


def test_create_user_assigns_next_id_and_hides_password() -> None:
    response = client.post(
        "/practice_api/users",
        json={
            "name": "김학생",
            "age": 20,
            "email": "student@example.com",
            "password": "StrongPass!",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 4,
        "name": "김학생",
        "age": 20,
        "email": "student@example.com",
    }
    assert user_list[-1]["password"] == "StrongPass!"


def test_create_user_does_not_reuse_deleted_id() -> None:
    client.delete("/practice_api/users/3")

    response = client.post(
        "/practice_api/users",
        json={
            "name": "김학생",
            "age": 20,
            "email": "student@example.com",
            "password": "StrongPass!",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == 4


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("name", "김"),
        ("age", 13),
        ("email", "not-an-email"),
        ("password", "nouppercase!"),
        ("password", "NOLOWERCASE!"),
        ("password", "NoSpecial123"),
        ("password", "Short!A"),
    ],
)
def test_create_user_rejects_invalid_input(field: str, value: str | int) -> None:
    payload = {
        "name": "김학생",
        "age": 20,
        "email": "student@example.com",
        "password": "StrongPass!",
    }
    payload[field] = value

    response = client.post("/practice_api/users", json=payload)

    assert response.status_code == 422


def test_create_user_rejects_duplicate_email_case_insensitively() -> None:
    response = client.post(
        "/practice_api/users",
        json={
            "name": "김학생",
            "age": 20,
            "email": "GILDONG24@EXAMPLE.COM",
            "password": "StrongPass!",
        },
    )

    assert response.status_code == 409


def test_update_only_given_fields() -> None:
    response = client.patch(
        "/practice_api/users/1",
        json={"age": 25},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "홍길동",
        "age": 25,
        "email": "gildong24@example.com",
    }
    assert user_list[0]["password"] == "Password1234!!"


def test_update_with_empty_body_returns_400() -> None:
    response = client.patch("/practice_api/users/1", json={})

    assert response.status_code == 400


def test_update_rejects_explicit_null() -> None:
    response = client.patch("/practice_api/users/1", json={"age": None})

    assert response.status_code == 422


def test_update_unknown_user_returns_404() -> None:
    response = client.patch("/practice_api/users/999", json={"age": 20})

    assert response.status_code == 404


def test_update_rejects_another_users_email() -> None:
    response = client.patch(
        "/practice_api/users/1",
        json={"email": "moonluck12@example.com"},
    )

    assert response.status_code == 409


def test_delete_user() -> None:
    response = client.delete("/practice_api/users/2")

    assert response.status_code == 204
    assert all(user["id"] != 2 for user in user_list)


def test_delete_unknown_user_returns_404() -> None:
    response = client.delete("/practice_api/users/999")

    assert response.status_code == 404
