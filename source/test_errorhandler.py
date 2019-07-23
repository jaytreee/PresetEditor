import logging
import pytest
from errorhandler import ErrorLogHandler


def test_errorhandler(qapp):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    hand = ErrorLogHandler(None)
    logger.addHandler(hand)

    logging.info('Test Message')
    logging.warning('Test Warning')
    logging.error('Error')