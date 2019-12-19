# -*- coding: utf-8 -*-
"""Tests for utils module."""

import wf.utils

from freezegun import freeze_time


@freeze_time("2019-11-3 12:00:00")
def test_get_next_months():
    """Test get_next_months() function."""

    expected_result = {
        'November': '2019-11-01',
        'December': '2019-12-01',
        'January': '2020-01-01'
    }
    assert wf.utils.get_next_months(3) == expected_result


def test_get_months_from_dates():
    """Tests get_months_from_dates() funciton."""

    result = wf.utils.get_months_from_dates('2020-04-23', '2020-05-11')

    expected_result = {
        'April': '2020-04-01',
        'May': '2020-05-01',
    }

    assert expected_result == result
