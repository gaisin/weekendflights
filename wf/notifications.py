# -*- coding: utf-8 -*-
"""Various notifications."""

import logging
import os
import requests
import smtplib

import telegram

from email.message import EmailMessage

IFTTT_KEY = os.environ['IFTTT_KEY']
WF_BOT_TOKEN = os.environ['WF_BOT_TOKEN']

MAIL_SERVER = os.environ['MAIL_SERVER']
MAIL_LOGIN = os.environ['MAIL_LOGIN']
MAIL_PASS = os.environ['MAIL_PASS']
OWNER_EMAIL = os.environ['OWNER_EMAIL']

VK_TOKEN = os.environ['VK_TOKEN']
VK_OWNER_ID_GROUP = os.environ['VK_OWNER_ID_GROUP']

LOG = logging.getLogger(__name__)


def send_found_len_by_ifttt(found_flights_number, search_name):
    """Sends notification about number of found tickets for specific search."""

    if not found_flights_number:
        return

    LOG.info(f'Sending push notification that {found_flights_number} '
             f'flights found for "{search_name}" search...')

    notification = f'Found {found_flights_number} new flights for "{search_name}" search'

    ifttt_event_url = f'https://maker.ifttt.com/trigger/ticket_found/with/key/{IFTTT_KEY}'
    data_to_send = {'value1': notification}

    # Sending post request to IFTTT webhook url
    requests.post(ifttt_event_url, json=data_to_send)


def post_bulk_to_channel(flights, search_name):
    """Posts one message to telegram channel about all given flights."""

    if not flights:
        return

    bot = telegram.Bot(token=WF_BOT_TOKEN)
    bulk_message = create_bulk_message(flights, search_name)
    bot.send_message(chat_id='@weekendflights', text=bulk_message, disable_web_page_preview=True)


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


def create_bulk_message(flights, search_name):
    """Creates one message about all given fligths."""

    if not flights:
        return

    LOG.debug(f'Creating bulk message about {len(flights)} flights of {search_name} search...')

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

    bulk_message = f'Flights found for "{search_name}" search:\n\n' +\
                   '\n\n'.join(flight_messages)

    return bulk_message


def post_bulk_to_vk(flights, search_name):
    """Posts one message to vk about all given flights."""

    if not flights:
        return

    LOG.info(f'Posting bulk message to VK about {len(flights)} flights of {search_name} search...')

    bulk_message = create_bulk_message(flights, search_name)

    requests.post(
        'https://api.vk.com/method/wall.post',
        data={
            'access_token': VK_TOKEN,
            'owner_id': VK_OWNER_ID_GROUP,
            'from_group': 1,
            'message': bulk_message,
            'signed': 0,
            'v': "5.52",
        })
