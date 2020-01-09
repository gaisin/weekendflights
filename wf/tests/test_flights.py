"""Tests for flights module."""

import mock
import os
import datetime

from freezegun import freeze_time

import wf.flights


def mock_search_conditions():
    """Returns mocked destination codes and months
    for testing flights search.
    """
    destination_codes = ['OPO']
    months = {
        'november': '2019-11-01',
        'december': '2019-12-01',
    }
    return destination_codes, months


def mock_requests_get(*args, **kwargs):
    """Mocks requests.get() function."""

    class MockResponse:
        def __init__(self, *args, **kwargs):
            self.json_data = {'data': {'key': 'value'}}

        def json(self):
            return self.json_data

    return MockResponse()


@mock.patch('requests.get', side_effect=mock_requests_get)
def test_get_latest(mocked_requests_get):
    """Tests get_latest() function.

    Mocks requests.post function and
    1) counts how many time it was called;
    2) checks args of the last call of the mocked function 'requests.post'.

    This answer explained a lot: https://stackoverflow.com/a/28507806.
    """
    mocked_destination_codes, mocked_months = mock_search_conditions()
    wf.flights.get_latest(mocked_destination_codes, mocked_months)
    assert mocked_requests_get.call_count == len(mocked_destination_codes) * len(mocked_months)

    TRAVELPAYOUTS_TOKEN = os.environ['TRAVELPAYOUTS_TOKEN']
    travelpayouts_api_url = 'http://api.travelpayouts.com/v2/prices/latest'
    # expected arguments from the calls of requests.get function
    expected_args = [mock.call(
        travelpayouts_api_url,
        params={
            'token': TRAVELPAYOUTS_TOKEN,
            'origin': 'MOW',
            'destination': destination_code,
            'beginning_of_period': mocked_months[month],
            'period_type': 'month',
            'limit': 1000,
            'show_to_affiliates': False,
        }) for destination_code in mocked_destination_codes for month in mocked_months]
    assert mocked_requests_get.call_args_list == expected_args


def mocked_get_latest():
    """Mocks get_lastest() function."""

    return [
        # +
        {
            'value': 11356,
            'return_date': '2019-11-26',
            'origin': 'MOW',
            'found_at': '2019-11-03T09:37:26',
            'destination': 'OPO',
            'depart_date': '2019-11-12'},
        # -
        {
            'value': 11850,
            'return_date': '2019-11-27',
            'origin': 'MOW',
            'found_at': '2019-11-03T12:45:10',
            'destination': 'ZUR',
            'depart_date': '2019-11-13'},
        # +
        {
            'value': 12230,
            'return_date': '2019-12-11',
            'origin': 'MOW',
            'found_at': '2019-11-03T06:08:27',
            'destination': 'OPO',
            'depart_date': '2019-11-27'},
        {
            'value': 13400,
            'return_date': '2019-12-07',
            'origin': 'MOW',
            'found_at': '2019-11-03T17:15:59',
            'destination': 'OPO',
            'depart_date': '2019-11-23'},
        {
            'value': 13763,
            'return_date': '2019-12-10',
            'origin': 'MOW',
            'found_at': '2019-11-04T15:52:51',
            'destination': 'OPO',
            'depart_date': '2019-11-26'},
        {
            'value': 15477,
            'return_date': '2019-11-28',
            'origin': 'MOW',
            'found_at': '2019-11-05T16:52:04',
            'destination': 'OPO',
            'depart_date': '2019-11-13'},
        # +
        {
            'value': 16156,
            'return_date': '2019-11-30',
            'origin': 'MOW',
            'found_at': '2019-11-03T12:28:45.684687',
            'destination': 'OPO',
            'depart_date': '2019-11-16'},
        {
            'value': 17661,
            'return_date': '2019-11-28',
            'origin': 'MOW',
            'found_at': '2019-11-04T13:15:24.873683',
            'destination': 'OPO',
            'depart_date': '2019-11-09'},
        {
            'value': 17764,
            'return_date': '2019-11-25',
            'origin': 'MOW',
            'found_at': '2019-11-03T07:26:07.066354',
            'destination': 'OPO',
            'depart_date': '2019-11-11'},
        # -
        {
            'value': 17794,
            'return_date': '2019-11-30',
            'origin': 'MOW',
            'found_at': '2019-10-31T09:44:45.218404',
            'destination': 'OPO',
            'depart_date': '2019-11-15'},
        {
            'value': 19411,
            'return_date': '2019-11-21',
            'origin': 'MOW',
            'found_at': '2019-11-05T20:13:04.048175',
            'destination': 'OPO',
            'depart_date': '2019-11-07'},
        {
            'value': 20340,
            'return_date': '2019-11-29',
            'origin': 'MOW',
            'found_at': '2019-10-30T18:53:21.152061',
            'destination': 'OPO',
            'depart_date': '2019-11-15'}
    ]


@freeze_time("2019-11-3 12:51:30")
def test_filter_flights():
    """Tests filter_flights() function."""

    flights = mocked_get_latest()

    date_pairs = [
        ('2019-11-12', '2019-11-26'),
        ('2019-11-27', '2019-12-11'),
        ('2019-11-16', '2019-11-30'),
        ('2019-11-13', '2019-11-27'),
        ('2019-11-15', '2019-11-30'),
    ]

    expected_result = [
        {
            'value': 11356,
            'return_date': '2019-11-26',
            'origin': 'MOW',
            'found_at': '2019-11-03T09:37:26',
            'destination': 'OPO',
            'depart_date': '2019-11-12'
        },
        {
            'value': 12230,
            'return_date': '2019-12-11',
            'origin': 'MOW',
            'found_at': '2019-11-03T06:08:27',
            'destination': 'OPO',
            'depart_date': '2019-11-27'
        },
        {
            'value': 16156,
            'return_date': '2019-11-30',
            'origin': 'MOW',
            'found_at': '2019-11-03T12:28:45.684687',
            'destination': 'OPO',
            'depart_date': '2019-11-16'
        },
    ]

    filtered_flights = wf.flights.filter_flights(
        flights,
        date_pairs,
        17000,
        max_hours_passed=10,
        unwilling_destinations=['ZUR'],
    )

    assert filtered_flights == expected_result


def mock_flights():
    return [
        {
            'value': 11356,
            'return_date': '2019-11-26',
            'origin': 'MOW',
            'found_at': '2019-11-03T09:37:26',
            'destination': 'OPO',
            'depart_date': '2019-11-12'
        },
        {
            'value': 16156,
            'return_date': '2019-11-30',
            'origin': 'MOW',
            'found_at': '2019-11-03T12:28:45.684687',
            'destination': 'OPO',
            'depart_date': '2019-11-16'
        },
    ]


def test_format_flights():
    """Tests format_flights() function."""

    flights = mock_flights()
    formatted_flights = wf.flights.format_flights(flights)

    expected_result = [
        {
            'price': 11300, 'arrival_date': '2019-11-26', 'origin': 'Moscow',
            'destination': 'Porto', 'departure_date': '2019-11-12',
            'departure_weekday': 'Tuesday', 'arrival_weekday': 'Tuesday',
            'link': 'https://www.aviasales.ru/search/MOW1211OPO26111?marker=207849',
            'found_at': datetime.datetime(2019, 11, 3, 9, 37, 26),
        },
        {
            'price': 16100, 'arrival_date': '2019-11-30', 'origin': 'Moscow',
            'destination': 'Porto', 'departure_date': '2019-11-16',
            'departure_weekday': 'Saturday', 'arrival_weekday': 'Saturday',
            'link': 'https://www.aviasales.ru/search/MOW1611OPO30111?marker=207849',
            'found_at': datetime.datetime(2019, 11, 3, 12, 28, 45, 684687),
        },
    ]

    assert expected_result == formatted_flights
