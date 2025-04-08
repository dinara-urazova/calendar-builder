from app import app
import pytest


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_invalid_month(client):
    response = client.get("/calendar/2024/0")
    assert response.status_code == 400
    assert b"Invalid month number: 0. Must be between 1 and 12." in response.data

    response = client.get("/calendar/2024/13")  # Неверный месяц (13)
    assert response.status_code == 400
    assert b"Invalid month number: 13. Must be between 1 and 12." in response.data
