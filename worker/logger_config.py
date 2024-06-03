import logging
import os
import distutils.util as util


def setup_logger(name):
    logger = logging.getLogger(name)
    DEBUG = bool(util.strtobool(os.getenv('DEBUG', default='False')))

    # Set the level of the logger to DEBUG
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    # Create a console handler and set its level to DEBUG
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create a formatter and set it to the console handler
    formatter = logging.Formatter('%(name)s - %(levelname)s : %(message)s')
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    return logger