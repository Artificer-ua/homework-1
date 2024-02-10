from unittest.mock import Mock

import pytest
from sqlalchemy import select

from src.conf import messages
from src.entity.models import User
from tests.conftest import TestingSessionLocal

user_data = {
    "username": "NewUser",
    "email": "newuser@example.com",
    "password": "87654321",
}


def test_signup(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("api/auth/signup", json=user_data)
    assert response.status_code == 201, response.text
    data = response.json()
    # to see output print pytest -s | pytest -vs
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "password" not in data
    assert mock_send_email.called


def test_repeat_signup(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("api/auth/signup", json=user_data)
    assert response.status_code == 409, response.text
    data = response.json()
    # to see output print pytest -s | pytest -vs
    assert data["detail"] == messages.ACCOUNT_EXISTS


def test_login_not_confirmed_email(client):
    # data -> client form
    response = client.post(
        "api/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    # to see output print pytest -s | pytest -vs
    assert data["detail"] == messages.EMAIL_NOT_CONFIRMED


@pytest.mark.asyncio
async def test_login(client):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(
            select(User).where(User.email == user_data.get("email"))
        )
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.confirmed = True
            await session.commit()

    # data -> client form
    response = client.post(
        "api/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data


def test_wrong_password(client):
    response = client.post(
        "api/auth/login",
        data={"username": user_data["email"], "password": "some_string"},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    # to see output print pytest -s | pytest -vs
    assert data["detail"] == messages.INVALID_PASSWORD


def test_wrong_email(client):
    response = client.post(
        "api/auth/login",
        data={"username": "email@email.com", "password": user_data["password"]},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    # to see output print pytest -s | pytest -vs
    assert data["detail"] == messages.INVALID_EMAIL


def test_validation_error(client):
    response = client.post("api/auth/login", data={"password": user_data["password"]})
    assert response.status_code == 422, response.text
    data = response.json()
    assert "detail" in data
