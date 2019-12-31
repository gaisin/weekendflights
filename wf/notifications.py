# -*- coding: utf-8 -*-
"""Various notifications."""

import logging
import os
import requests
import smtplib

from email.message import EmailMessage

MAIL_SERVER = os.environ['MAIL_SERVER']
MAIL_LOGIN = os.environ['MAIL_LOGIN']
MAIL_PASS = os.environ['MAIL_PASS']
OWNER_EMAIL = os.environ['OWNER_EMAIL']

VK_TOKEN = os.environ['VK_TOKEN']
VK_OWNER_ID_GROUP = os.environ['VK_OWNER_ID_GROUP']

LOG = logging.getLogger(__name__)


def send_failure_email(traceback_info):
    """Sends email notification about failure with traceback.
    TODO: make gmail account and allow it to send messages
    """
    message = EmailMessage()
    message.set_content(traceback_info)
    message['Subject'] = 'WF: error on production'
    message['From'] = MAIL_LOGIN
    message['To'] = OWNER_EMAIL

    smtp_server = smtplib.SMTP_SSL(MAIL_SERVER, 465)
    smtp_server.login(MAIL_LOGIN, MAIL_PASS)
    smtp_server.send_message(message)
    smtp_server.quit()


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
