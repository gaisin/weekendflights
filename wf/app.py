#!/usr/bin/python3

"""Entry point for the parser.
Describes basic logic of cheap weekend flights search.
"""

import threading
import time

import schedule

import wf.db
import wf.flights
import wf.notifications
import wf.utils
import wf.searches

LOG = wf.utils.set_logger()


def find_flights():
    """Runs cheap flights searching."""

    try:
        searches = wf.searches.get_all()

        for search in searches:
            if not search.get("is_active"):
                continue

            search_name = search["name"]
            destinations = search["destinations"]
            max_price = search["max_price"]
            trip_type = search["trip_type"]

            if trip_type == "weekends":
                next_x_months = search["next_x_months"]
                months = wf.utils.get_next_months(next_x_months)
                date_pairs = wf.utils.get_date_pairs(on_weekends=True, next_x_months=next_x_months)

            elif trip_type == "vacation":
                departure_date = search["departure_date"]
                arrival_date = search["arrival_date"]
                months = wf.utils.get_months_from_dates(departure_date, arrival_date)
                date_pairs = wf.utils.get_date_pairs(
                    departure_date=departure_date,
                    arrival_date=arrival_date,
                    trip_min_length=int(search["trip_min_length"]),
                    trip_max_length=int(search["trip_max_length"]),
                )

            latest_flights = wf.flights.get_latest(destinations, months)
            filtered_flights = wf.flights.filter_flights(
                latest_flights,
                date_pairs,
                max_price
            )
            formatted_flights = wf.flights.format_flights(filtered_flights)
            unique_flights = wf.flights.get_unique_flights(formatted_flights)

            wf.notifications.post_bulk_to_channel(unique_flights, search_name)

    except Exception as e:
        LOG.exception(f"While flights searching exception happened: {e}")


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def run_parser_loop():
    """Run infinite loop for checking events periodically.
    Documentation for "Schedule": http://schedule.readthedocs.io/.
    """

    schedule.every().hour.do(run_threaded, find_flights)

    LOG.info('Starting cheap flights search...')

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_parser_loop()
