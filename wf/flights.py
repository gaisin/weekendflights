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


def filter_flights(flights_data, date_pairs, max_price,
                   max_hours_passed=6, unwilling_destinations=None):
    """Filter given flights list according to settings.
    For each flights in flights_data

    :flights_data: list of flights, each flights is a dictionary
    :date_pairs: list of tuples, where each tuple is a pair of suitable dates
    :max_price: maximum price of a flight
    :max_hours_passed: maximum hours passed since flight finding
    :unwilling_destinations: list of IATA codes of not suitable destinations,
        needed if search made for whole country, but some of destinations are not suitable
    """
    LOG.debug("Filtering flights...")
    LOG.debug(f"\tgot {len(flights_data)} flights and {len(date_pairs)} date pairs")
    LOG.debug(f"\tmax price is {max_price}, max hours passed is {max_hours_passed}")
    LOG.debug(f"\tunwillings destinations are {unwilling_destinations}")
    unwilling_destinations = unwilling_destinations or []

    filtered_flights = []

    for flight in flights_data:
        found_at = flight['found_at']
        try:
            found_at_datetime = datetime.strptime(found_at, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            found_at_datetime = datetime.strptime(found_at, '%Y-%m-%dT%H:%M:%S.%f')

        time_now = datetime.now()
        time_difference = time_now - found_at_datetime
        time_difference_in_hours = time_difference / timedelta(hours=1)
        if time_difference_in_hours > max_hours_passed:
            continue

        if (flight['value'] <= max_price and
           flight['destination'] not in unwilling_destinations and
           (flight["depart_date"], flight["return_date"]) in date_pairs):
            filtered_flights.append(flight)

    LOG.debug(f"\t{len(filtered_flights)} left after filtering")
    return filtered_flights


def format_flights(flights):
    """Formats flights dict: adds link, weekday names, gets rid of redundant information.
    Converts fields from
        value, trip_class, show_to_affiliates
        return_date, origin, number_of_changes
        gate, found_at, duration, distance
        destination, depart_date, actual
    to fields
        origin, destination,
        departure_date, departure_weekday,
        arrival_date, arrival_weekday,
        price, link, found_at

    NOTE:
        price is rounded by nudreds, e.g. 4251 -> 4200, 4248 -> 4200
        found_at converted to timestamp
    """
    formatted_flights = []

    for flight in flights:
        try:
            origin = CITY_CODE_TO_NAME[flight['origin']][1]
        except KeyError:
            origin = flight['origin']

        try:
            destination = CITY_CODE_TO_NAME[flight['destination']][1]
        except KeyError:
            destination = flight['destination']

        departure_weekday = wf.utils.get_weekday(flight['depart_date'])
        arrival_weekday = wf.utils.get_weekday(flight['return_date'])

        # round price to least hundred
        rounded_price = flight['value'] - flight['value'] % 100

        link = wf.utils.create_aviasales_link(
            flight['origin'], flight['depart_date'],
            flight['destination'], flight['return_date'],
        )

        try:
            found_at_datetime = datetime.strptime(flight["found_at"], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            found_at_datetime = datetime.strptime(flight["found_at"], '%Y-%m-%dT%H:%M:%S.%f')

        flight_dict = {
            'origin': origin,
            'destination': destination,
            'departure_date': flight['depart_date'],
            'departure_weekday': departure_weekday,
            'arrival_date': flight['return_date'],
            'arrival_weekday': arrival_weekday,
            'price': rounded_price,
            'link': link,
            'found_at': found_at_datetime,
        }
        formatted_flights.append(flight_dict)

    return formatted_flights


