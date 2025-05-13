from calendar_builder import app
import pytest


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_invalid_year(client):
    # Тест для недопустимого года (значение больше 9999)
    response = client.get("/calendar/10000")
    assert response.status_code == 400
    assert b"<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad Request</h1>\n<p>Invalid year number:10000. Year must be between 1 and 9999.</p>\n"
