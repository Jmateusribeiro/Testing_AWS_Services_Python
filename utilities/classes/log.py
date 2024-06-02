"""
A custom logger class that logs messages to both console and file with timed rotation.
"""
import logging
import re
from logging import handlers, Logger


class CustomLogger(Logger):
    """
    A custom logger class that logs messages to both console and file with timed rotation.

    This class extends the standard Logger class from the logging module and provides additional functionality
    for logging messages to both console and file. Log files are rotated daily, and old log files are automatically
    deleted after a specified number of days.

    Attributes:
        log_folder (str): The directory where log files will be stored.
        backupCount_days (int): The number of days to keep backup log files.

    Methods:
        __init__: Initializes the custom logger.
    """
    def __init__(self, log_folder: str, backupCount_days: int = 5):
        """
        Initialize the CustomLogger.

        Args:
            log_folder (str): The folder where log files will be stored.
            backupCount_days (int, optional): The number of days to keep log files. Defaults to 5.
        """
        super().__init__('CustomLogger')
        self.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

        # File handler (with timed rotation each day)
        # Think is better to have a log file per day
        file_handler = handlers.TimedRotatingFileHandler(
            log_folder + '\\AWS_Testing',
            when='midnight',
            backupCount=backupCount_days
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.suffix = '%Y_%m_%d.log'
        file_handler.extMatch = re.compile(r"^\d{4}_\d{2}_\d{2}.log$")
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)
