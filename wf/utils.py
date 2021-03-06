# -*- coding: utf-8 -*-
"""Various tools for the project.

TODO:
    * add make_weekend_tuples to make tuples with weekend dates pairs
    * add tools to convert cities and countries names
"""

import logging
import logging.handlers
import sys

from datetime import date, timedelta, datetime
from calendar import month_name


LOG = logging.getLogger(__name__)

WEEKDAYS = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

WEEKDAYS_RU = {
    "Monday": "понедельник",
    "Tuesday": "вторник",
    "Wednesday": "среда",
    "Thursday": "четверг",
    "Friday": "пятница",
    "Saturday": "суббота",
    "Sunday": "воскресенье",
}

MONTHS = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря',
}


def set_logger():
    """Sets logging configuration."""

    # create logger and set logging level
    logger = logging.getLogger("wf")
    logger.setLevel(logging.DEBUG)

    # create rotating file handler
    max_log_size_in_megabytes = 2
    fh = logging.handlers.RotatingFileHandler(
        '/var/log/wf.log',
        maxBytes=max_log_size_in_megabytes*1024*1024,
        backupCount=5
    )

    # create stream handler
    sh = logging.StreamHandler(stream=sys.stdout)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(sh)

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

    if arrival_month_num < departure_month_num:
        january = 1
        december = 12
        new_date_to_write = _fill_months(months, date_to_write, departure_month_num, december)
        _fill_months(months, new_date_to_write, january, arrival_month_num)
    else:
        _fill_months(months, date_to_write, departure_month_num, arrival_month_num)

    return months


def _fill_months(months, date_to_write, departure_month_num, arrival_month_num):

    for month_num in range(departure_month_num, arrival_month_num+1):
        name = month_name[month_num]
        months[name] = str(date_to_write)
        next_year, next_month = nextmonth(date_to_write.year, date_to_write.month)
        date_to_write = date_to_write.replace(year=next_year, month=next_month)

    return date_to_write


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
    2) on_weekends=False, departure_date='2020-04-01', arrival_date='2020-05-06',
       trip_min_length=7, trip_max_length=14
        Func returns all existing pairs of dates from departure date until arrival dates
        in tuples with minimum seven days of trip, and maximum 14 days of trip
    """
    if ((next_x_months is not None and (departure_date is not None or arrival_date is not None)) or
            (next_x_months is None and (departure_date is None or arrival_date is None))):
        raise ValueError("Either next_x_months or both departure_date and arrival_date "
                         "has to be specified, but not all of them.")

    if next_x_months is not None:
        departure_date = date.today()
        arrival_month = (departure_date.year, departure_date.month)
        for i in range(next_x_months):
            arrival_month = nextmonth(*arrival_month)
        arrival_date = date(*arrival_month, 1)
    else:
        departure_date = date(*[int(elem) for elem in departure_date.split('-')])
        arrival_date = date(*[int(elem) for elem in arrival_date.split('-')])
        if arrival_date < date.today():
            raise ValueError("Given dates already passed")
        if departure_date < date.today():
            departure_date = date.today()
        if arrival_date <= departure_date:
            raise ValueError("Departure date must be sooner than arrival date.")

    result = []

    one_day = timedelta(days=1)
    while departure_date <= arrival_date:
        if on_weekends:
            week_day = WEEKDAYS[departure_date.weekday()]

            if week_day == "Wednesday":
                departure_date += one_day
                continue

            diff = timedelta(days=trip_min_length)
            while departure_date + diff < get_next_wednesday(str(departure_date)):
                date_pair = (str(departure_date), str(departure_date + diff))
                result.append(date_pair)
                diff += timedelta(days=1)

        else:
            for trip_length in range(trip_min_length-1, trip_max_length+1):
                trip_length = timedelta(days=trip_length)
                if departure_date + trip_length <= arrival_date:
                    date_pair = (str(departure_date), str(departure_date + trip_length))
                    result.append(date_pair)

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


def get_readable_date(date):
    """Changes date format from '2020-02-02' to readable '2 февраля'."""

    _, month, day = date.split('-')

    return ' '.join([day, MONTHS[int(month)]])


def translate_weekday(weekday):
    """Returns name of weekday translated to Russian ."""

    return WEEKDAYS_RU[weekday]
