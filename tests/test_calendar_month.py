from calendar_builder import app
from utils import StorageMock
import pytest
import calendar
from event_storage_postgresql import DayEvents
from typing import List
import html
from bs4 import BeautifulSoup

@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_get_calendar_month(client):
    year = 2024
    month = 10

    def get_events_calendar_view_mock(year: int, month: int) -> List[DayEvents]:
        events = [DayEvents(stars=0, day_class="bm", is_amrita=False, moon=None, holiday=None) for _ in range(31)]
        events[0] = DayEvents(stars=5, day_class="dk", is_amrita=True, moon="ba", holiday="Special Day")
        return events


    app.config["event_storage"] = StorageMock({"get_events_calendar_view": get_events_calendar_view_mock})

    response = client.get(f"/calendar/{year}/{month}")

    assert response.status_code == 200
    # общая проверка
    content = html.unescape(response.data.decode("utf-8"))
    soup = BeautifulSoup(content, "html.parser")
    assert soup.find("h3").text.strip() == f"Октябрь {year}"

    assert f'href="/calendar/{year}/{month-1}"' in content  # ссылка 'Назад' на пред месяц
    assert f'href="/calendar/{year}/{month+1}"' in content  # ссылка 'Вперед' на след месяц
    
    _, month_days = calendar.monthrange(year, month)
    start_day = calendar.monthrange(year, month)[0] + 1
    
    # check if month days is correct
    day_tables = soup.select("div.day")
    assert len(day_tables) == month_days
    
    first_day_class = f"first_day_of_month_is_{start_day}"
    first_day_div = day_tables[0]
    first_day_classes = first_day_div.get("class", [])

    assert first_day_class in first_day_classes
    assert "dk" in first_day_classes

    tds = first_day_div.find_all("td")
    assert "⭐️5" in tds[0].text
    assert "ba" in tds[1].text
    assert tds[2].text.strip() == "A"
 
     # Check the holiday in the footer
    footer = soup.select_one("div.holidays p")
    assert "Special Day" in footer.text