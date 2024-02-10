from datetime import datetime
from unittest.mock import AsyncMock, patch

from src.services.auth import auth_service
from tests.conftest import test_contact as conf_test_contact

test_contact = {
    "firstname": "Thefirstname",
    "lastname": "thelastname",
    "email": "testcontact@example.com",
    "phone": "0631234567",
    "bday": str(datetime.strptime("1999-01-19", "%Y-%m-%d").date()),
    "notes": "",
}
test_contact_updated = {
    "firstname": "NewName",
    "lastname": "NewLast",
    "email": "testcontact@example.com",
    "phone": "0631234567",
    "bday": str(datetime.strptime("1999-01-19", "%Y-%m-%d").date()),
    "notes": "",
}


def test_get_contacts(client, get_token, monkeypatch):
    # redis mock
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None

        # fastapi limiter mock
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())

        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1


def test_get_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None

        # fastapi limiter mock
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())

        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts/1", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert "id" in data
        assert data["firstname"] == conf_test_contact["firstname"]
        assert data["lastname"] == conf_test_contact["lastname"]
        assert data["email"] == conf_test_contact["email"]
        assert data["phone"] == conf_test_contact["phone"]
        assert data["bday"] == str(conf_test_contact["bday"])


def test_create_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None

        # fastapi limiter mock
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())

        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("api/contacts", json=test_contact, headers=headers)
        assert response.status_code == 201, response.text
        data = response.json()
        assert "id" in data
        assert data["firstname"] == test_contact["firstname"]
        assert data["lastname"] == test_contact["lastname"]
        assert data["email"] == test_contact["email"]
        assert data["phone"] == test_contact["phone"]
        assert data["bday"] == test_contact["bday"]


def test_update_contact(client, get_token):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.put(
            "api/contacts/2", json=test_contact_updated, headers=headers
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert "id" in data
        assert data["firstname"] == test_contact_updated["firstname"]
        assert data["lastname"] == test_contact_updated["lastname"]
        assert data["email"] == test_contact_updated["email"]
        assert data["phone"] == test_contact_updated["phone"]
        assert data["bday"] == test_contact_updated["bday"]


def test_update_contact_not_found(client, get_token):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.put(
            "api/contacts/3", json=test_contact_updated, headers=headers
        )
        assert response.status_code == 404, response.text


def test_delete_contact(client, get_token):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.delete("api/contacts/2", headers=headers)
        assert response.status_code == 204, response.text


def test_search_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None

        # fastapi limiter mock
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())

        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        search_keyword = "last"
        response = client.get(f"api/contacts/search/{search_keyword}", headers=headers)

        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        assert "id" in data[0]
        assert data[0]["firstname"] == conf_test_contact["firstname"]
        assert data[0]["lastname"] == conf_test_contact["lastname"]
        assert data[0]["email"] == conf_test_contact["email"]
        assert data[0]["phone"] == conf_test_contact["phone"]
        assert data[0]["bday"] == str(conf_test_contact["bday"])
