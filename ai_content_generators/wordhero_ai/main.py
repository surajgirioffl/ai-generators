"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 23rd May 2024
Last-modified: 10th June 2024
Error-series: 1100
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"

import os
import logging

if __name__ == "__main__":
    import tools
    from wordhero import WordHero
else:
    # Relative import (for executing from the root project directory)
    from . import tools
    from .wordhero import WordHero


PROJECT_DIR = os.path.dirname(__file__)
os.chdir(PROJECT_DIR)  # Changing the current working directory to the project directory.
SETTINGS: dict = tools.load_settings("config.json")

APP_REQUIRED_DIRS = ["appdata", "appdata/logs", "appdata/profile", SETTINGS["output_location"]]
tools.create_app_require_directories(APP_REQUIRED_DIRS)
tools.configure_logging(SETTINGS["logging_location"])


def main(site_preferences: dict, driver=None, *args, **kwargs):
    local_webdriver = False
    if not driver:
        driver = tools.get_webdriver_instance(profile_dir_path=f"{os.getcwd()}/appdata/profile")
        driver.maximize_window()
        local_webdriver = True

    wordhero = WordHero(driver)
    if site_preferences.get("login_required"):
        wordhero.login_to_wordhero(SETTINGS["wordhero_credentials"]["email"], SETTINGS["wordhero_credentials"]["password"])

    logging.info("Going to generate article...")
    generated_article, prompt_response_mapping = wordhero.generate_article(**site_preferences["options"])
    logging.info("Article generated successfully...")
    WordHero.save_content(generated_article, SETTINGS["output_location"])
    logging.info("Article saved successfully...")

    # Quitting the driver instance if local_webdriver
    if local_webdriver:
        driver.quit()
