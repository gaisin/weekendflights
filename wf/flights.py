""""Tools to work with flights.

flight model: {
    destination: basestring, e.g. "Ufa"
    price: integer, e.g. 4200
    departure_date: basestring, e.g. "2019-12-28"
    arrival_date: basestring, e.g. "2020-01-07"
    found_at: integer, e.g. 15844858457847
}
"""

import logging
import os
import requests

from datetime import datetime, timedelta

from pymongo.errors import DuplicateKeyError

import wf.db
import wf.utils

from wf.iata_converters import CITY_CODE_TO_NAME

TRAVELPAYOUTS_TOKEN = os.environ['TRAVELPAYOUTS_TOKEN']

LOG = logging.getLogger(__name__)


def get_latest(destination_codes, months):
    """Get flights found for last 48 hours.
    Documentation: https://support.travelpayouts.com/hc/ru/articles/203956163#02

    :param destination_codes: list of codes of airports, cities or counrties.
    :param months: list of months, when flights are searched.
        Months are presented as the dict of months name and the first date of the month,
        e.g. months = {
            'march': '2019-03-01',
            'april': '2019-04-01',
            'may': '2019-05-01',
        }
        Note: first date should be in YYYY-MM-DD format.
    :param trip_duration: trip duration in weeks, needed for Travelpayouts API
    """

    LOG.info('Getting latest flights...')
    LOG.debug(f"\tlooking for flights to {destination_codes} for {months.keys()}")

    travelpayouts_api_url = 'http://api.travelpayouts.com/v2/prices/latest'

    found_flights = []

    for key in months:
        for destination_code in destination_codes:
            LOG.debug('\tsearching for flights MOW - %s at %s', destination_code, key)
            payload = {
                'token': TRAVELPAYOUTS_TOKEN,
                'origin': 'MOW',
                'destination': destination_code,
                'beginning_of_period': months[key],
                'period_type': 'month',
                'limit': 1000,
                'show_to_affiliates': False,
            }
            response = requests.get(travelpayouts_api_url, params=payload)
            flights_data = response.json()['data']
            found_flights += flights_data

    LOG.info(f"\tfound {len(found_flights)} latest flights")
    return found_flights
