"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 20th May 2024
Last-modified: 06th July 2024
Error-series: 1500
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"


import logging
import os
from time import sleep
from datetime import datetime
import re
from undetected_chromedriver import Chrome, ChromeOptions
from undetected_edgedriver import Edge, EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

if __name__ == "__main__":
    from ideogram import Ideogram
else:
    from db_scripts import AIGeneratorDB
    from .ideogram import Ideogram

logging.info(f"Old CWD: {os.getcwd()}")
logging.info("Changing CWD.")
PROJECT_DIR = os.path.dirname(__file__)
os.chdir(PROJECT_DIR)  # Changing the current working directory to the project directory.
logging.info(f"New CWD: {os.getcwd()}")


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
        - extension (str, optional): The extension for the filename. Default to "None". If not provided then only filename will return.

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


def main(site_preferences: dict, driver=None, *args, **kwargs) -> None:
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
    local_webdriver = False
    if not driver:
        driver = get_webdriver_instance()
        driver.maximize_window()
        local_webdriver = True

    if site_preferences.get("login_required"):
        if CONFIG["google_login_options_start"]["manual_login"] == "Y":
            is_login_success = login_to_google_account(driver)
        else:
            email = CONFIG["google_login_options_start"]["email"]
            password = CONFIG["google_login_options_start"]["password"]
            is_login_success = login_to_google_with_email_and_password(driver, email, password)

        if not is_login_success:
            print("Error: Google login failed. Error Code: 1505")
            logging.error("Google login failed. Error Code: 1505")
            if local_webdriver:
                driver.quit()
            return False

    # Creating instance of the Ideogram class
    ideogram = Ideogram(driver)
    if site_preferences.get("login_required"):
        ideogram.login_with_google()

    prompts: list | str = site_preferences["options"]["prompt"]
    prompts: list = prompts if isinstance(prompts, list) else [prompts]
    logging.info(f"Total number of prompts in this batch is {len(prompts)}")

    db = AIGeneratorDB()

    for index, prompt in enumerate(prompts):
        site_preferences["options"]["prompt"] = prompt
        logging.info(f"Initiating image generation for the prompt {index}...")

        ideogram.create_image_with_prompt(**site_preferences["options"])
        image_links = ideogram.fetch_images_link(site_preferences["options"]["prompt"])
        logging.info("Image links fetched successfully....")
        timestamp = datetime.now()
        filename = generate_file_name(prompt=prompt, timestamp=timestamp)
        filenames = [f"{filename}_{index}.jpg" for index in range(1, 11)]
        downloaded_images_path = ideogram.download_images(
            image_links, CONFIG["Default_location_start"]["default_output_location_local"], filenames
        )
        logging.info(f"Operation Completed @Ideogram for the prompt {index}")

        # Saving the required entities into the database
        db.insert_output(
            file_path=downloaded_images_path,
            category=site_preferences["category"],
            site_id=db.get_site_id(site_preferences["site"]),
            prompt_id=db.insert_prompt(prompt),
            timestamp=timestamp,
        )
        logging.info("Output details successfully inserted into the database...")

    if local_webdriver:
        driver.quit()  # Closing the browser
    return True


if __name__ == "__main__":
    main()
