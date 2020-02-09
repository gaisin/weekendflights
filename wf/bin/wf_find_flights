#!/usr/bin/python3

"""Main script, that works in CRON.
Describes basic logic of cheap weekend flights search.
"""

import wf.db
import wf.flights
import wf.notifications
import wf.utils
import wf.searches

LOG = wf.utils.set_logger()


def main():
    """Runs cheap flights searching."""

    searches = wf.searches.get_all()

    for search in searches:
        search_name = search["name"]
        destinations = search["destinations"]
        max_price = search["max_price"]
        trip_type = search["trip_type"]

        if trip_type == "weekends":
            next_x_months = search["next_x_months"]
            months = wf.utils.get_next_months(next_x_months)
            date_pairs = wf.utils.get_date_pairs(on_weekends=True, next_x_months=next_x_months)

        elif trip_type == "vacation":
            continue  # temporary, since get_date_pairs() not ready yet
            departure_date = search["departure_date"]
            arrival_date = search["arrival_date"]
            months = wf.utils.get_months_from_dates(departure_date, arrival_date)
            date_pairs = wf.utils.get_date_pairs(
                departure_date=departure_date,
                arrival_date=arrival_date,
                trip_min_length=search["trip_min_length"],
                trip_max_length=search["trip_max_length"],
            )

        latest_flights = wf.flights.get_latest(destinations, months)
        filtered_flights = wf.flights.filter_flights(
            latest_flights,
            date_pairs,
            max_price
        )
        formatted_flights = wf.flights.format_flights(filtered_flights)
        unique_flights = wf.flights.get_unique_flights(formatted_flights)

        wf.notifications.send_found_len_by_ifttt(len(unique_flights), search_name)
        wf.notifications.post_bulk_message_to_vk(unique_flights, search_name)


if __name__ == "__main__":
    main()
