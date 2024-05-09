"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 7th May 2024
Last-modified: 9th May 2024
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"


import logging
import os
import re
from datetime import datetime


def configure_logging(filename: str = "appdata/script.log") -> None:
    """Configure logging with a specified filename or default 'appdata/script.log'.

    Args:
        filename (str): The name of the file to log to. Defaults to 'appdata/script.log'.

    Returns:
        None
    """
    logging.basicConfig(filename=filename, level=logging.INFO, format="%(asctime)s - %(module)s(%(lineno)d) - %(levelname)s -> %(message)s")
