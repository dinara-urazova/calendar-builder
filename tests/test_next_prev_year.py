from app import app
import pytest
from datetime import datetime


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_next_prev_month(client):
    # tests validity of next/prev links
    year = 2023
    month = 10
    response = client.get(f"/calendar/{year}/{month}")

    assert b'href="/calendar/2023/11"' in response.data
    assert b'href="/calendar/2023/9"' in response.data
