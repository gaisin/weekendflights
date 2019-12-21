""""Module for handling db connections."""

import os
import logging

import pymongo.collection

from pymongo import MongoClient

LOG = logging.getLogger(__name__)

DB_LOGIN = os.environ['DB_LOGIN']
DB_PASS = os.environ['DB_PASS']
DB_ADDRESS = os.environ['DB_ADDRESS']


class Database():
    """Wrapper over mongo database.

    Made for handling database connection using environmental variables.
    """
    def __init__(self, name):
        self.__name = name
        self.__database = self._get_client()[self.__name]

    def __getattr__(self, name):
        result = getattr(self.__database, name)
        if isinstance(result, pymongo.collection.Collection):
            return Collection(name, result)
        else:
            return result

    def __repr__(self):
        return f"Database({self.__name})"

    def _get_client(self):
        """Returns connected client to MongoDB server."""

        client = MongoClient(
            "mongodb+srv://{}:{}@{}/"
            "test?retryWrites=true&w=majority"
            .format(DB_LOGIN, DB_PASS, DB_ADDRESS)
        )

        return client


class Collection():
    """Wrapper over mongo collection.

    Now just proxies calls to mongo collection,
    but any logic can be build in the future.
    """

    def __init__(self, name, collection):
        self.__name = name
        self.__collection = collection

    def __getattr__(self, name):
        return getattr(self.__collection, name)

    def __repr__(self):
        return f"Collection({self.__name})"


def initiate_db():
    """Initiates database."""

    create_indexes()


def create_indexes():
    """Sets indexes and unique keys."""

    db = Database("wf")

    # flights collection index
    db.flights.create_index([
        ("destination", 1),
        ("price", 1),
        ("departure_date", 1),
        ("arrival_date", 1),
    ], unique=True)

    # searches collection index
    db.searches.create_index(
        [("name", 1)],
        unique=True
    )

    # flights collection TTL index to delete documents after 30 days
    month_in_seconds = 2630000
    db.flights.create_index([
        ("added_at", 1),
    ], expireAfterSeconds=month_in_seconds)
