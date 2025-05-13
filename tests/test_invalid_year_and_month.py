from calendar_builder import app
import pytest


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_invalid_year_and_month(client):
    # Тест для недопустимого года (при указании с месяцем)
    response = client.get("/calendar/0/12")
    assert response.status_code == 400
    assert b"Invalid year number: 0. Year must be between 1 and 9999." in response.data

    # Тест для недопустимого года (год больше допустимого, при указании с месяцем)
    response = client.get("/calendar/10000/5")
    assert response.status_code == 400
    assert b"<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad Request</h1>\n<p>Invalid year number: 10000. Year must be between 1 and 9999.</p>\n"

    # Тест для недопустимого года и недопустимого месяца
    response = client.get("/calendar/0/13")
    assert response.status_code == 400
    assert b"<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad Request</h1>\n<p>Invalid year number: 0. Year must be between 1 and 9999.</p>\n"
