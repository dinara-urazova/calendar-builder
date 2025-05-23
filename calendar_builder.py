from flask import Flask, abort, redirect, render_template, url_for, current_app
import calendar
from datetime import datetime
from config_reader import Settings
from event_storage_postgresql import EventStorageSqlAlchemy
from typing import cast

app = Flask(__name__)
app.config["event_storage"] = EventStorageSqlAlchemy()

env_config = Settings()

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


def validate_year_month(year: int, month: int | None = None):
    if year < 1 or year > 9999:
        abort(400, f"Invalid year number: {year}. Year must be between 1 and 9999.")
    if month is not None:
        if month < 1 or month > 12:
            abort(400, f"Invalid month number: {month}. Must be between 1 and 12.")


@app.route("/", methods=["GET"])
def root():
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    return redirect(
        url_for("get_calendar_month", year=current_year, month=current_month)
    )


@app.route("/calendar/<int:year>/<int:month>", methods=["GET"])
def get_calendar_month(year: int, month: int):
    # Проверка для года и месяца
    validate_year_month(year, month)
    month_start_day, month_days = calendar.monthrange(year, month)
    month_name = months[month]
    next_month = month + 1 if month < 12 else 1
    prev_month = month - 1 if month > 1 else 12
    next_year = year if month < 12 else year + 1
    prev_year = year if month > 1 else year - 1

    event_storage = cast(EventStorageSqlAlchemy, current_app.config["event_storage"])
    events = event_storage.get_events_calendar_view(year, month)

    return render_template(
        "calendar-month.html",
        month_name=month_name,
        month_days=month_days,
        first_day_class=f"first_day_of_month_is_{month_start_day + 1}",
        year=year,
        next_month=next_month,
        next_year=next_year,
        prev_month=prev_month,
        prev_year=prev_year,
        events=events,
    )


@app.route("/calendar/<int:year>", methods=["GET"])
def get_calendar_year(year: int):
    # Проверка для года
    validate_year_month(year)
    month_data = []
    for month in range(1, 13):
        month_start_day, month_days = calendar.monthrange(year, month)
        month_name = months[month]
        event_storage = cast(
            EventStorageSqlAlchemy, current_app.config["event_storage"]
        )
        events = event_storage.get_events_calendar_view(year, month)
        month_data.append(
            {
                "year": year,
                "month_name": month_name,
                "month_days": month_days,
                "first_day_class": f"first_day_of_month_is_{month_start_day + 1}",
                "events": events,
            }
        )
    next_year = year + 1
    prev_year = year - 1

    return render_template(
        "calendar-year.html",
        month_data=month_data,
        year=year,
        next_year=next_year,
        prev_year=prev_year,
    )
