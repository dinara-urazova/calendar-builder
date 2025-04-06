from app import app
import pytest
import calendar
import re


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_get_calendar_month(client):
    year = 2024
    month = 10
    response = client.get(f"/calendar/{year}/{month}")

    assert response.status_code == 200

    html = response.data.decode("utf-8")
    assert "Октябрь 2024" in html

    start_day, month_days = calendar.monthrange(year, month)
    # Extract all the divs with day numbers (i.e., <div>1</div>, <div>2</div>, ...)
    day_divs = re.findall(r"<div>(\d+)</div>", html)  
    # results in a list of strings from 2 to 31 (as start day is treated differently) like ['2', ...'31']

    last_day = max(int(day) for day in day_divs)
    assert last_day == month_days

    first_day_class = f"first_day_of_month_is_{start_day + 1}"
    assert first_day_class in html

    assert f'href="/calendar/{year}/{month-1}"' in html  # ссылка 'Назад' на пред месяц
    assert f'href="/calendar/{year}/{month+1}"' in html  # ссылка 'Вперед' на след месяц
