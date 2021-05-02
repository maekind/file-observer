# encoding:utf-8

"""
logger.py - Wrapper for printing a formatted message.
"""

import logging

__author__ = 'Marco Espinosa'
__version__ = '1.0'
__email__ = 'hi@marcoespinosa.com'


class Level:
    """
    Level wrapper class for not importing logging into source code.
    """

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class Logger:
    """
    Python logger wrapper for printing formatted messages.
    Format =  '%Y-%m-%d %H:%M:%S - logger_name - logger_level - message'
    """

    def __init__(self, name, level=Level.INFO, output="stdout"):
        """
        Default constructor
        @param name:            name for identifying the logged messages.
        @optional param level:  logging level from Level class. (Default: Level.INFO)
        @optional param output: where to print the message. (Default: stdout)
        """

        # Create logger
        self.__name = name
        log_setup = logging.getLogger(name)

        # Formatting logger output
        formatter = logging.Formatter(
            "%(asctime)s [%(name)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Check for console or file output
        if output != "stdout":
            log_handler = logging.FileHandler(output, mode="a")
        else:
            log_handler = logging.StreamHandler()

        # Setting formatter
        log_handler.setFormatter(formatter)

        # Setting level
        log_setup.setLevel(level)

        # Creating handler to configured logger
        log_setup.addHandler(log_handler)

    def warning(self, message):
        """
        Warning function wrapper
        @param message: string message to log.
        """
        logging.getLogger(self.__name).warning(message)

    def info(self, message):
        """
        Info function wrapper
        @param message: string message to log.
        """
        logging.getLogger(self.__name).info(message)

    def error(self, message):
        """
        Error function wrapper
        @param message: string message to log.
        """
        logging.getLogger(self.__name).error(message)

    def debug(self, message):
        """
        Debug function wrapper
        @param message: string message to log.
        """
        logging.getLogger(self.__name).debug(message)

    def critical(self, message):
        """
        Critical function wrapper
        @param message: string message to log.
        """
        logging.getLogger(self.__name).critical(message)
