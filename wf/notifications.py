# -*- coding: utf-8 -*-
"""Various notifications."""

import logging
import os
import requests

VK_TOKEN = os.environ['VK_TOKEN']
VK_OWNER_ID_GROUP = os.environ['VK_OWNER_ID_GROUP']

LOG = logging.getLogger(__name__)


def post_bulk_message_to_vk(flights, search_name):
    """Posts one message about all given flights."""

    if not flights:
        return

    LOG.info(f'Posting one message to VK about {len(flights)} flights of {search_name} search...')

    flight_messages = []

    for flight in flights:
        destination = flight['destination']
        price = flight['price']
        departure_date = flight['departure_date']
        departure_weekday = flight['departure_weekday']
        arrival_date = flight['arrival_date']
        arrival_weekday = flight['arrival_weekday']
        link = flight['link']
        found_at = flight['found_at'].strftime('%-H:%M, %d %b %Y')

        flight_message = f'Moscow - {destination} '\
                         f'for {price} rubles, '\
                         f'{departure_date} ({departure_weekday}) — '\
                         f'{arrival_date} ({arrival_weekday}): {link}.\n'\
                         f'found on {found_at}'

        flight_messages.append(flight_message)

    message_to_post = f'Flights found for "{search_name}" search:\n\n' +\
                      f'\n\n'.join(flight_messages)

    requests.post(
        'https://api.vk.com/method/wall.post',
        data={
            'access_token': VK_TOKEN,
            'owner_id': VK_OWNER_ID_GROUP,
            'from_group': 1,
            'message': message_to_post,
            'signed': 0,
            'v': "5.52",
        })
