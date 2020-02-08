# -*- coding: utf-8 -*-
"""Various tools for the project.

TODO:
    * add make_weekend_tuples to make tuples with weekend dates pairs
    * add tools to convert cities and countries names
"""

import logging
import logging.handlers

from datetime import date, timedelta, datetime
from calendar import month_name


LOG = logging.getLogger(__name__)

WEEKDAYS = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thirsday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}


def set_logger():
    """Sets logging configuration."""

    # create logger and set logging level
    logger = logging.getLogger("wf")
    logger.setLevel(logging.DEBUG)

    # create rotating file handler
    max_log_size_in_megabytes = 2
    fh = logging.handlers.RotatingFileHandler(
        'logs/wf.log',
        maxBytes=max_log_size_in_megabytes*1024*1024,
        backupCount=5
    )
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def get_next_months(months_number):
    """Returns dictionary of next X months from today (including current month)
    in {'name': 'first date'} format, e.g.
    months = {
        'november': '2019-11-01',
        'december': '2019-12-01',
    }
    """
    months = {}

    date_to_write = date.today().replace(day=1)

    for i in range(months_number):
        name = month_name[date_to_write.month]
        months[name] = str(date_to_write)
        next_year, next_month = nextmonth(date_to_write.year, date_to_write.month)
        date_to_write = date_to_write.replace(year=next_year, month=next_month)

    return months


def get_months_from_dates(departure_date, arrival_date):
    """Returns dictionary of months between departure_date and arrival_date
    in {'name': 'first date'} format, e.g. 2020-04-23 and 2020-05-11:
    months = {
        'april': '2020-04-01',
        'may': '2020-05-01',
    }
    """
    months = {}

    departure_month_num = int(departure_date.split('-')[1])
    arrival_month_num = int(arrival_date.split('-')[1])

    date_to_write = date(*(int(i) for i in departure_date.split('-'))).replace(day=1)

    for month_num in range(departure_month_num, arrival_month_num+1):
        name = month_name[month_num]
        months[name] = str(date_to_write)
        next_year, next_month = nextmonth(date_to_write.year, date_to_write.month)
        date_to_write = date_to_write.replace(year=next_year, month=next_month)

    return months


def get_next_wednesday(from_date=None):
    """Return next Wednesday from today or from given date.
    If given date is Wednesday, returns given date.
    """
    if from_date is None:
        today = date.today()
    else:
        today = date(*[int(elem) for elem in from_date.split('-')])

    day = today.weekday()
    if day < 2:
        diff = timedelta(days=(2 - day))
    elif day > 2:
        diff = timedelta(days=(7 - day + 2))
    else:
        diff = timedelta(days=0)

    return today + diff


def get_date_pairs(departure_date=None, arrival_date=None,
                   on_weekends=False, next_x_months=None,
                   trip_min_length=3, trip_max_length=7):
    """Return all existing pairs of dates according to given conditions.

    If on_weekends == True, return only weekend pairs - from thirsday to tuesday.
    If on weekend == False, trip_max_length should be specified to return all available
    pairs of dates on month from 'start_date' parameter.

    Cases:
    1) on_weekends=True, departure_date='2019-12-01', arrival_date='2020-02-28'
        Func returns all existing pairs of dates for weekends
        from departure date until arrival dates
        in tuples with minimum three days of trip:
            (2019-12-5, 2019-12-8),
            (2019-12-5, 2019-12-9),
            (2019-12-5, 2019-12-10),
            (2019-12-6, 2019-12-9),
            (2019-12-6, 2019-12-10),
            (2019-12-7, 2019-12-10),
            ...
    TODO:
    2) on_weekends=False, departure_date='2020-04-01', arrival_date='2020-05-06',
       trip_min_length=7, trip_max_length=14
        Func returns all existing pairs of dates from departure date until arrival dates
        in tuples with minimum seven days of trip, and maximum 14 days of trip
    """
    if next_x_months is None:
        departure_date = date(*[int(elem) for elem in departure_date.split('-')])
        arrival_date = date(*[int(elem) for elem in arrival_date.split('-')])
    else:
        departure_date = date.today()
        arrival_month = (departure_date.year, departure_date.month)
        for i in range(next_x_months):
            arrival_month = nextmonth(*arrival_month)
        arrival_date = date(*arrival_month, 1)

    result = []

    one_day = timedelta(days=1)
    while departure_date <= arrival_date:
        week_day = WEEKDAYS[departure_date.weekday()]

        if on_weekends:
            if week_day == "Wednesday":
                departure_date += one_day
                continue

            diff = timedelta(days=trip_min_length)
            while departure_date + diff < get_next_wednesday(str(departure_date)):
                date_pair = (str(departure_date), str(departure_date + diff))
                result.append(date_pair)
                diff += timedelta(days=1)

        departure_date += one_day

    return result


def create_aviasales_link(origin, departure_date, destination, arrival_date):
    """"Creates link to aviasales flights serach on given params,
    and adds travelpayouts marker.

    Since the aviasales search available only for next 12 months,
    it is possible just to send depart and arrival dates' month and day.
    """
    departure_date_formatted = ''.join(reversed(departure_date[5:].split('-')))
    arrival_date_formatted = ''.join(reversed(arrival_date[5:].split('-')))

    link = 'https://www.aviasales.ru/search/{}{}{}{}1?marker=207849'.format(
        origin,
        departure_date_formatted,
        destination,
        arrival_date_formatted,
    )
    return link


def get_weekday(date_string):
    """Returns weekday of given date.
    Date should be in YYYY-MM-DD format.
    """
    date_elems = [int(i) for i in date_string.split('-')]
    date_in_datetime = datetime(*date_elems)
    weekday_num = date_in_datetime.weekday()
    return WEEKDAYS[weekday_num]


def nextmonth(year, month):
    """Returns next pair of year and month."""

    if month == 12:
        return year+1, 1
    else:
        return year, month+1
