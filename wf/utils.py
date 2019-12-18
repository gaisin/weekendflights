# -*- coding: utf-8 -*-
"""Various tools for the project."""

import logging
import logging.handlers

LOG = logging.getLogger(__name__)

def set_logger():
    """Sets logging configuration."""

    # create logger and set logging level
    logger = logging.getLogger("wf")
    logger.setLevel(logging.DEBUG)

    # create rotating file handler
    max_log_size_in_megabytes = 2
    fh = logging.handlers.RotatingFileHandler(
        'logs/wf.log',
        maxBytes=max_log_size_in_megabytes*1024*1024,
        backupCount=5
    )
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
