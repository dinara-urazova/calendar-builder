from app import app
import pytest
import calendar
import re
from utils import StorageMock
from event_storage_postgresql import DayEvents
from typing import List
import html
from bs4 import BeautifulSoup

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

    def get_events_calendar_view_mock(year: int, month: int) -> List[DayEvents]:
        _, month_days = calendar.monthrange(year, month)
        events = [DayEvents(stars=0, day_class="None", is_amrita=False, moon=None, holiday=None) for _ in range(month_days)]
        events[0] = DayEvents(stars=5, day_class="dk", is_amrita=True, moon="ba", holiday="Special Day")
        return events

    app.config["event_storage"] = StorageMock({"get_events_calendar_view": get_events_calendar_view_mock})
    response = client.get(f"/calendar/{year}")
    assert response.status_code == 200

    content = html.unescape(response.data.decode("utf-8"))
    soup = BeautifulSoup(content, "html.parser")
    
    assert soup.find("h1").text == str(year)
    assert f'href="/calendar/{year-1}"' in content
    assert f'href="/calendar/{year + 1}"' in content

    # ensure that number of months is 12
    month_divs = soup.select("div.calendar-wrapper > div.month")
    assert len(month_divs) == 12

    # ensure month names are present 
    for index, month_div in enumerate(month_divs, start=1):
        month_name = months[index]
        assert month_div.find("h3").text == month_name

        # ensure first-day class + special event on day 1
        first_day = month_div.select_one(".calendar-container .day")
        start_day = calendar.monthrange(year, index)[0] + 1
        first_day_classes = first_day.get("class", [])
        assert f"first_day_of_month_is_{start_day}" in first_day_classes
        assert "dk" in first_day_classes

        # star count, Amrita, moon symbol checks in the first-day table
        tds = first_day.find_all("td")
        assert "⭐️5" in tds[0].text
        assert "ba" in tds[1].text
        assert tds[2].text.strip() == "A"

        # check if days num is correct
        tables = month_div.select(".calendar-container table")
        expected_days = calendar.monthrange(year, index)[1]
        assert len(tables) == expected_days
    
    # check special day is rendered correctly
    footer = soup.select_one("div.holidays p")
    assert "Special Day" in footer.text
