import logging

from utils.logging import setup_logger


def test_logger_setup():
    logger = setup_logger("test_logger")
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO
