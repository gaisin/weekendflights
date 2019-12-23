import logging

import wf.db

LOG = logging.getLogger(__name__)


def get_collection():
    """Returns searches collection."""

    db = wf.db.Database("wf")
    return db.searches
