from app import app
import pytest
from datetime import datetime


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_root(client):
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    response = client.get("/")

    assert response.status_code == 302
    assert (
        response.headers.get("Location") == f"/calendar/{current_year}/{current_month}"
    )
