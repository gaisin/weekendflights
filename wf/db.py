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

