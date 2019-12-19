# -*- coding: utf-8 -*-
"""Various tools for the project."""

import logging
import logging.handlers

from datetime import date, timedelta, datetime
from calendar import nextmonth, month_name


LOG = logging.getLogger(__name__)

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
