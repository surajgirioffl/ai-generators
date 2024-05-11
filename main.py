"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 7th May 2024
Last-modified: 11th May 2024
Error-series: 1100
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"


import logging
import os
import re


def configure_logging(filename: str = "appdata/script.log") -> None:
    """Configure logging with a specified filename or default 'appdata/script.log'.

    Args:
        filename (str): The name of the file to log to. Defaults to 'appdata/script.log'.

    Returns:
        None
    """
    logging.basicConfig(filename=filename, level=logging.INFO, format="%(asctime)s - %(module)s(%(lineno)d) - %(levelname)s -> %(message)s")


def create_app_require_directories(dirs: list | tuple = ["appdata", "images", "output"]) -> None:
    """A function that creates the required directories for the application.

    Parameters:
        dirs (list | tuple): A list or tuple of directory names. Default value is ["appdata", "images", "output"].

    Returns:
        None
    """
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)


def parse_config_file(file_path: str = "config.txt", set_as_global: bool = True) -> dict | bool:
    """Parse the config file and return the configuration as a dictionary.

    Args:
        file_path (str): The path to the config file. Defaults to "config.txt".
        set_as_global (bool): Whether to set the config dictionary as global variable. Defaults to True.

    Returns:
        dict | bool: The configuration as a dictionary, or False if there's an error.
    """
    config_dict = {}
    current_section = None

    try:
        with open(file_path) as file:
            for line in file:
                if not line:
                    # Skip empty lines
                    continue

                section_match = re.match(r"^###(.+)###$", line)
                if section_match:
                    current_section = section_match.group(1).strip()
                    # Skipping 'end' section because it doesn't have any key-value.
                    if "start" in current_section:
                        config_dict[current_section] = {}
                elif current_section:
                    key_value_match = re.match(r"^([^=]+)=(.*)$", line)
                    if key_value_match:
                        key = key_value_match.group(1).strip()
                        value = key_value_match.group(2).strip()
                        config_dict[current_section][key] = value
    except FileNotFoundError as e:
        print(f"Error: File '{file_path}' not found. Error Code: 1101")
        logging.error(f"Error: File '{file_path}' not found. Error Code: 1101")
        logging.error(f"Exception: {e}")
        return False
    except Exception as e:
        print("Error: Something went wrong while parsing config file. Error Code: 1102")
        logging.error("Error: Something went wrong while parsing config file. Error Code: 1102")
        logging.error(f"Exception: {e}")
        return False
    else:
        if set_as_global:
            global CONFIG
            CONFIG = config_dict
        return config_dict
