"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 7th May 2024
Last-modified: 06th July 2024
Error-series: 1100
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "1.0.0"


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
import tools

if __name__ == "__main__":
    import pixverse
else:
    from db_scripts import AIGeneratorDB
    from . import pixverse

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
        print("Google login failed by email and password. Error Code: 1106")
        logging.error(f"Exception: {e}")
        logging.error("Google login failed by email and password. Error Code: 1106")
        logging.info("Please login manually...")
        return False
    else:
        return True


def main(site_preferences: dict, driver=None, *args, **kwargs) -> None:
    """Driver function to integrate and execute the script.

    Returns:
        None
    """
    # ----------------- Setting basic configuration -----------------------
    create_app_require_directories()
    parse_config_file()
    configure_logging(CONFIG["Default_location_start"]["default_log_location_local"])
    logging.info("-----------------STARTING A NEW SESSION (Pixverse)-----------------")

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
            print("Error: Google login failed. Error Code: 1105")
            logging.error("Google login failed. Error Code: 1105")
            if local_webdriver:
                driver.quit()
            return False

    if site_preferences.get("login_required"):
        pixverse.login_with_google(driver)

    def is_image_option_available(site_preferences: dict) -> bool:
        """
        Check if the image option is available in the site preferences.

        Args:
            sites_preferences (dict): A dictionary containing site preferences.

        Returns:
            bool: True if the image option is available, False otherwise.

        More Info:
            - Logic is: If the image option is present in the site preferences means user want to generate video using image. So, we will trigger the image based generation flow otherwise we will trigger the prompt based generation flow.
        """
        if "image" in site_preferences["options"].keys():
            return True
        return False

    if is_image_option_available(site_preferences):
        logging.info("Initiating video generation from images (Pixverse AI)...")

        images: list | str = site_preferences["options"]["image"]
        images: list = images if isinstance(images, list) else [images]
        logging.info(f"Total number of images path in this batch is {len(images)}")

        db = AIGeneratorDB()

        for index, image in enumerate(images):
            site_preferences["options"]["image"] = image
            logging.info(f"Initiating video generation for the image index {index}...")
            pixverse.create_video_from_images(driver, **site_preferences["options"])
            link = pixverse.fetch_generated_video_link(driver)
            logging.info("Video linked fetched successfully...")
            timestamp = datetime.now()
            filename = tools.generate_file_name(image_path=image, timestamp=timestamp, extension="mp4")
            downloaded_video_path = pixverse.download_video(
                link, CONFIG["Default_location_start"]["default_output_location_local"], filename
            )
            logging.info(f"Operation Completed for the image index {index}")

            # Saving the required entities into the database
            db.insert_output(
                file_path=downloaded_video_path,
                category=site_preferences["category"],
                site_id=db.get_site_id(site_preferences["site"]),
                image_id=db.insert_image(image),
                timestamp=timestamp,
            )
            logging.info("Output details successfully inserted into the database...")

    else:
        logging.info("Initiating video generation from prompt...")

        prompts: list | str = site_preferences["options"]["prompt"]
        prompts: list = prompts if isinstance(prompts, list) else [prompts]
        logging.info(f"Total number of prompts in this batch is {len(prompts)}")

        db = AIGeneratorDB()

        for index, prompt in enumerate(prompts):
            site_preferences["options"]["prompt"] = prompt
            logging.info(f"Initiating image generation for the prompt index {index}...")
            pixverse.create_video_from_prompt(driver, **site_preferences["options"])
            link = pixverse.fetch_generated_video_link(driver)
            logging.info("Video linked fetched successfully...")
            timestamp = datetime.now()
            filename = tools.generate_file_name(prompt=prompt, timestamp=timestamp, extension="mp4")
            downloaded_video_path = pixverse.download_video(
                link, CONFIG["Default_location_start"]["default_output_location_local"], filename
            )
            logging.info(f"Operation Completed for the prompt index {index}")

            # Saving the required entities into the database
            db.insert_output(
                file_path=downloaded_video_path,
                category=site_preferences["category"],
                site_id=db.get_site_id(site_preferences["site"]),
                prompt_id=db.insert_prompt(prompt),
                timestamp=timestamp,
            )
            logging.info("Output details successfully inserted into the database...")

    print("Operation Completed (Pixverse)")
    logging.info("Operation Completed (Pixverse)")

    if local_webdriver:
        driver.quit()  # Closing the browser if local webdriver
    return True


if __name__ == "__main__":
    main()
