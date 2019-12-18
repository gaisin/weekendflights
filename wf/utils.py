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
