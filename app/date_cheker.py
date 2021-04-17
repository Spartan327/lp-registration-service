from calendar import Calendar
import datetime


def get_current_month():
    current_date = datetime.date.today()
    month = Calendar().monthdatescalendar(current_date.year, current_date.month)
    return month
