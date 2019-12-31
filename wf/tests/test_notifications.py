# -*- coding: utf-8 -*-
"""Tests for notifications module."""

import mock
import wf.notifications


def mock_found_tickets_list():
    """Returns mocked list of found flights."""

    flight1 = {
        'destination': 'Ufa',
        'value': '3246',
        'departure_date': '28.12.2019',
        'departure_weekday': 'Sun',
        'arrival_date': '06.01.2020',
        'arrival_weekday': 'Mon',
        'price': 4200,
        'link': 'https://link.com',
        'found_at': '2019-12-28',
    }

    flight2 = {
        'destination': 'Ufa',
        'value': '2854',
        'departure_date': '27.12.2019',
        'departure_weekday': 'Fri',
        'arrival_date': '06.01.2020',
        'arrival_weekday': 'Mon',
        'price': 4200,
        'link': 'https://link.com',
        'found_at': '2019-12-28',
    }

    return [flight1, flight2]


@mock.patch('requests.post', side_effect=mock.Mock())
def test_send_found_len_by_ifttt(mocked_requests_post):
    """Tests send_found_len_by_ifttt function."""

    search_name = "Test search"
    mocked_flights = mock_found_tickets_list()
    wf.notifications.send_found_len_by_ifttt(len(mocked_flights), search_name)
    assert mocked_requests_post.call_count == 1

    expected_result = f'Found {len(mocked_flights)} new flights for "{search_name}" search'
    assert mocked_requests_post.call_args.kwargs["json"]["value1"] == expected_result
