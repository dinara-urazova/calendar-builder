from flask import Flask, redirect, render_template, url_for
import calendar
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    return redirect(url_for('get_calendar', year=current_year, month=current_month))

months = [
    "", 
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь"
]

@app.route("/calendar/<int:year>/<int:month>", methods=["GET"])
def get_calendar(year: int, month: int):
    month_start_day, month_days = calendar.monthrange(year, month)
    month_name = months[month]
    next_month = month + 1 if month < 12 else 1
    prev_month = month - 1 if month > 1 else 12
    next_year = year if month < 12 else year + 1
    prev_year = year if month > 1 else year - 1

    return render_template(
        "calendar-month.html",
        month_name=month_name,
        month_days=month_days,
        month_start_day=month_start_day + 1,
        year=year,
        month=month,
        next_month=next_month,
        next_year=next_year,
        prev_month=prev_month, 
        prev_year=prev_year,

    )


