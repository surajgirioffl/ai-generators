"""Module containing various tools required for the script.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 23rd May 2024
Last-modified: 23rd May 2024
Error-series: 1300
"""

import json
import logging
import os


def load_settings(path: str = "settings.json") -> dict:
    """Load settings from a JSON file.

    Args:
        path (str): The path to the JSON file. Defaults to "settings.json".

    Returns:
        dict: The settings loaded from the file.

    Raises:
        Same exception as encountered during loading.
    """
    try:
        with open(path) as file:
            return json.load(file)
    except Exception as e:
        logging.error("Error in loading settings file. Error Code: 1301")
        logging.exception(f"Exception: {e}")
        raise e.__class__(f"{e}")


def configure_logging(filename: str = "appdata/script.log") -> None:
    """Configure logging with a specified filename or default 'appdata/script.log'.

    Args:
        filename (str): The name of the file to log to. Defaults to 'appdata/script.log'.

    Returns:
        None
    """
    logging.basicConfig(filename=filename, level=logging.INFO, format="%(asctime)s - %(module)s(%(lineno)d) - %(levelname)s -> %(message)s")


def create_app_require_directories(dirs: list | tuple) -> None:
    """A function that creates the required directories for the application.

    Parameters:
        dirs (list | tuple): A list or tuple of directory names.

    Returns:
        None
    """
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
