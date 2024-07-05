"""Module containing various tools required for the script.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 23rd May 2024
Last-modified: 06th July 2024
Error-series: 1300
"""

from datetime import datetime
import json
import logging
import os
from selenium.webdriver import Chrome, Edge, ChromeOptions, EdgeOptions


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


def get_webdriver_instance(browser: str = "chrome", headless=False, profile_dir_path: str | None = None) -> Chrome | Edge | None:
    """Function to get the webdriver instance for the given browser.

    Args:
        browser (str, optional): Desired browser (chrome or edge). Defaults to "chrome".
        headless (bool, optional): Set to True for headless mode. Defaults to False.
        profile_dir_path (str, optional): Path to the profile directory. Defaults to None.

    Returns:
        Chrome | Edge | None: Webdriver instance if browser is supported, else None.
    """
    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        if profile_dir_path:
            options.add_argument(f"--user-data-dir={profile_dir_path}")
        return Chrome(options=options)
    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        if profile_dir_path:
            options.add_argument(f"--user-data-dir={profile_dir_path}")
        return Edge(options=options)
    else:
        logging.error("Browser not supported. Please use Chrome or Edge. Error Code: 1302")
        return None


def generate_file_name(
    prompt: str = None,
    image_path=None,
    timestamp: datetime | str = None,
    index: int = None,
    timestamp_format: str = "%Y%m%d%H%M%S%f",
    extension: str = None,
) -> str:
    """Generates a file name based on the provided prompt, image path, timestamp, and index.

    Parameters:
        - prompt (str, optional): The prompt to be used in the file name. Defaults to None. (Compulsory if image_path is not provided).
        - image_path (any, optional): The path to the image. Defaults to None (Compulsory if prompt is not provided).
        - timestamp (datetime | str, optional): The timestamp to be included in the file name. Defaults to None. If not provided then datetime.now() will used.
        - index (int, optional): The index to be appended to the file name. Defaults to None.
        - timestamp_format (str, optional): The format of the timestamp. Defaults to "%Y%m%d%H%M%S%f".
        - extension (str, optional): The extension for the filename. Default to "None". If not provided then filename without extension will return.

    More:
        - If prompt and image_path both are provided then prompt will used because it has more priority.

    Returns:
        str: The generated file name based on the inputs.
    """
    if prompt is None and image_path is None:
        raise ValueError("Either prompt or image_path must be provided.")
    max_file_size = 256  # In windows
    max_prompt_size = max_file_size - 30  # 30 for adding timestamp, index, underscores etc

    if image_path:
        image_path = os.path.splitext(os.path.basename(image_path))[0]

    filename_prefix = prompt if prompt else image_path  # Prompt has top priority if both is provided.

    if timestamp:
        if isinstance(timestamp, datetime):
            timestamp = timestamp.strftime(timestamp_format)
    else:
        timestamp = datetime.now().strftime(timestamp_format)

    if len(filename_prefix) > max_prompt_size:
        filename_prefix = filename_prefix[:max_prompt_size]
    if extension:
        return f"{filename_prefix}_{str(timestamp)}_{index}.{extension}" if index else f"{filename_prefix}_{str(timestamp)}.{extension}"
    else:
        return f"{filename_prefix}_{str(timestamp)}_{index}" if index else f"{filename_prefix}_{str(timestamp)}"
