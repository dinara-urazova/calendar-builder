from app import app
import pytest
import calendar
import re


months = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_get_calendar_year(client):
    year = 2024
    response = client.get(f"/calendar/{year}")

    html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert f"{year}" in html

    # Extract the month data from the rendered HTML
    for month in range(1, 13):
        month_name = months[month] 
        month_start_day, month_days = calendar.monthrange(year, month)
        assert month_name in html

        # Find the section for the specific month
        month_section = html.split(f'<div class="month">')[month]
        
        # Extract the divs for the days of the month  
        day_divs = re.findall(r'<div>(\d+)</div>', month_section)

       # as in calendar month, find the highest div num aka last month day
        last_day = max(int(day) for day in day_divs)
        assert last_day == month_days

        # Ensure the first day of the month has the correct CSS class
        first_day_class = f"first_day_of_month_is_{month_start_day + 1}"
        assert first_day_class in month_section

    assert f'href="/calendar/{year-1}"' in html
    assert f'href="/calendar/{year + 1}"' in html
