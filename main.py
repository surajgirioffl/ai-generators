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
from undetected_chromedriver import Chrome, ChromeOptions
from undetected_edgedriver import Edge, EdgeOptions


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


def get_webdriver_instance(browser: str = "chrome", headless=False) -> Chrome | Edge | None:
    """Function to get the webdriver instance for the given browser.

    Args:
        browser (str, optional): Desired browser (chrome or edge). Defaults to "chrome".
        headless (bool, optional): Set to True for headless mode. Defaults to False.

    Returns:
        Chrome | Edge | None: Webdriver instance if browser is supported, else None.
    """
    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        return Chrome(options=options)
    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        return Edge(options=options)
    else:
        print("Browser not supported. Please use Chrome or Edge. Error Code: 1104")
        logging.info("Browser not supported. Please use Chrome or Edge. Error Code: 1104")
        return None


def login_to_google_account(driver: Chrome | Edge, url: str = "https://accounts.google.com") -> bool:
    """Function to login to google account.

    Args:
        driver (Chrome | Edge): Webdriver instance.
        url (str, optional): URL to login. Defaults to "https://accounts.google.com".

    Returns:
        bool: Returns True if logged in successfully else False.
    """
    driver.get(url)
    user_input = input("Press enter if googled logged in successfully else any key: ")
    return True if not user_input else False


def main() -> None:
    """Driver function to integrate and execute the script.

    Returns:
        None
    """
    # ----------------- Setting basic configuration -----------------------
    create_app_require_directories()
    parse_config_file()
    configure_logging(CONFIG["Default_location_start"]["default_log_location_local"])
    logging.info("-----------------STARTING A NEW SESSION-----------------")

    # ------------------ Main workflow will start from here ---------------------
    driver = get_webdriver_instance()
    if not login_to_google_account(driver):
        print("Error: Google login failed. Error Code: 1105")
        logging.error("Google login failed. Error Code: 1105")
        driver.quit()
        return False

    option_enabled = False  # Specify if the options are enabled

    if CONFIG["options_start"]["use_images"] == "Y":
        option_enabled = True
        ...

    if CONFIG["options_start"]["use_prompts"] == "Y":
        option_enabled = True
        ...

    driver.quit()  # Closing the browser

    if not option_enabled:
        print("No options are enabled to generate video. Please enable at least one option. Error Code: 1103")
        logging.info("No options are enabled to generate video. Please enable at least one option. Error Code: 1103")
        return False
    return True


if __name__ == "__main__":
    main()
