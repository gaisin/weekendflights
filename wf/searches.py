"""Various functions to work with searches.
    Each search — set of conditions for flights searching and filtering.
    In the main loop I iterate over each search and search flights.
    If search is successful (means found tickets that meet search conditions),
    notification will be sent with the label from search document,
    and can be sent for specific IFTTT key (means to a specific person).

    searches examples:
        weekend flights to Ufa for next 12 months
        flights to Portugal from April 12th to May 6th, 7-14 nights

    search model explanation with examples: {
        name: e.g. "Portugal in may"
        destinations: ["OPO", "LIS"]
        max_price: 14000
        trip_type: "weekends" | "vacation" | "looking_around"
            "weekends" means, that only flights will be searched for weekends
                if trip_type == "weekends", next_x_months field is required
                this search will be main search for publishing to a public channel
                use cacse: flights to Ufa on weekends for the next 12 months
            "vacation" means, that any days between given dates will be suitable
                flights will be filtered strictly between given dates
                this field used for the get_date_pairs() function
                if trip_type == "vacation", next fields are requied:
                    departure_date, arrival_date, trip_min_length, trip_max_length
                use case: flights to Portugal from April 12th to May 6th, 7-14 nights
            "looking_around" means, that this search is just to see what kind of flights are found
                TODO: work this idea better, now just leaving it here
                looking tickets for the whole month
                use case: flights to Portugal in April
        next_x_months = 12
            number of months, when tickets will be searched
            required only of dates_type == next_x_months
        departure_date: "2020-04-27"
            if dates_type == flexible, only month will be taken and arrival_date will be ignored
        arrival_date: "2020-05-05"
            this field required only if dates_type == fixed
        trip_min_length: 6
            minimal number of days in a trip
            required only if trip_type == vacation (required for get_date_pairs() function)
        trip_max_length: 14
            minimal number of days in a trip
            required only if trip_type == vacation (required for get_date_pairs() function)
    }
"""

import logging

import wf.db

LOG = logging.getLogger(__name__)


def get_collection():
    """Returns searches collection."""

    db = wf.db.Database("wf")
    return db.searches


def add(name, destinations, max_price, trip_type, next_x_months=None, departure_date=None,
        arrival_date=None, trip_min_length=None, trip_max_length=None):
    """Adds a search into a database."""

    LOG.info(f'Adding a "{name}" search to the database...')

    if trip_type == "weekends" and next_x_months is None:
        raise Exception("If trip_type == 'weekends', "
                        "'next_x_months' attribute should be specified.")

    elif trip_type == "vacation":
        if departure_date is None or arrival_date is None:
            raise Exception("If trip_type == vacation, "
                            "departure and arrival dates should be specified.")
        if trip_min_length is None or trip_max_length is None:
            raise Exception("If trip_type == vacation, "
                            "trip_min_length and trip_max_length "
                            "should be specified.")

    search = {
        "name": name,
        "destinations": destinations,
        "max_price": max_price,
        "trip_type": trip_type,
    }

    if trip_type == "weekends":
        search["next_x_months"] = next_x_months

    if trip_type == "vacation":
        search["departure_date"] = departure_date
        search["arrival_date"] = arrival_date
        search["trip_min_length"] = trip_min_length
        search["trip_max_length"] = trip_max_length

    searches_collection = get_collection()
    searches_collection.insert_one(search)


def remove(name):
    """Removes a search from a database."""

    LOG.info(f'Removing a "{name}" search from the database...')

    searches_collection = get_collection()
    searches_collection.delete_one({"name": name})

