from app import app
import pytest
from datetime import datetime


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_next_prev_year(client):
    year = 2023
    response = client.get(f"/calendar/{year}")

    assert b'href="/calendar/2024"' in response.data
    assert b'href="/calendar/2022"' in response.data
