"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 20th May 2024
Last-modified: 22nd May 2024
Error-series: 1500
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"


import logging
import os
from time import sleep
import re
from undetected_chromedriver import Chrome, ChromeOptions
from undetected_edgedriver import Edge, EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from ideogram import Ideogram

PROJECT_DIR = os.path.dirname(__file__)
os.chdir(PROJECT_DIR)  # Changing the current working directory to the project directory.


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
        print(f"Error: File '{file_path}' not found. Error Code: 1501")
        logging.error(f"Error: File '{file_path}' not found. Error Code: 1501")
        logging.error(f"Exception: {e}")
        return False
    except Exception as e:
        print("Error: Something went wrong while parsing config file. Error Code: 1502")
        logging.error("Error: Something went wrong while parsing config file. Error Code: 1502")
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
        print("Browser not supported. Please use Chrome or Edge. Error Code: 1504")
        logging.info("Browser not supported. Please use Chrome or Edge. Error Code: 1504")
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


def login_to_google_with_email_and_password(
    driver: Chrome | Edge, email: str, password: str, url: str = "https://accounts.google.com"
) -> bool:
    """A function to login to Google with an email and password using a web driver.

    Args:
        driver (Chrome | Edge): The web driver to use for logging in.
        email (str): The email address to use for login.
        password (str): The password to use for login.
        url (str, optional): The URL to navigate to for login. Default is "https://accounts.google.com".

    Returns:
        bool: True if login is successful, False otherwise.
    """
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    try:
        email_input = wait.until(EC.visibility_of_element_located((By.ID, "identifierId")))
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)

        password_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='Passwd']")))
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        # Checking if login successful
        try:
            wait.until(EC.url_contains("https://myaccount.google.com"))
        except TimeoutException as e:
            raise Exception(f"Login Failed. TimeoutException: {e}")

    except Exception as e:
        print(f"Exception: {e}")
        print("Google login failed by email and password. Error Code: 1506")
        logging.error(f"Exception: {e}")
        logging.error("Google login failed by email and password. Error Code: 1506")
        logging.info("Please login manually...")
        return False
    else:
        return True


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
    driver.maximize_window()
    if CONFIG["google_login_options_start"]["manual_login"] == "Y":
        is_login_success = login_to_google_account(driver)
    else:
        email = CONFIG["google_login_options_start"]["email"]
        password = CONFIG["google_login_options_start"]["password"]
        is_login_success = login_to_google_with_email_and_password(driver, email, password)

    if not is_login_success:
        print("Error: Google login failed. Error Code: 1505")
        logging.error("Google login failed. Error Code: 1505")
        driver.quit()
        return False

    option_enabled = False  # Specify if the options are enabled

    # Creating instance of the Ideogram class
    ideogram = Ideogram(driver)
    ideogram.login_with_google()

    if CONFIG["options_start"]["use_prompts"] == "Y":
        logging.info("Initiating image generation from prompt...")
        option_enabled = True
        prompt_file_location = CONFIG["Default_location_start"]["default_prompt_file_location"]
        try:
            with open(prompt_file_location) as file:
                prompt = file.read()
        except FileNotFoundError as e:
            print("Error: Prompt file not found. Error Code: 1507")
            logging.error("Prompt file not found. Error Code: 1507")
            logging.error(f"Exception: {e}")
        else:
            ideogram.create_image_with_prompt(prompt)
            ideogram.download_images(ideogram.fetch_images_link(prompt), CONFIG["Default_location_start"]["default_output_location_local"])

    sleep(5000)

    print("Operation Completed. Closing the webdriver.")
    logging.info("Operation Completed. Closing the webdriver.")
    driver.quit()  # Closing the browser

    if not option_enabled:
        print("No options are enabled to generate video. Please enable at least one option. Error Code: 1503")
        logging.info("No options are enabled to generate video. Please enable at least one option. Error Code: 1503")
        return False
    return True


if __name__ == "__main__":
    main()
