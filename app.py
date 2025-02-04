"""Driver module to integrate and execute the script (Master script - Master Module)

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 09th June 2024
Last-modified: 28th June 2024
Error-series: 3100
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"

import logging
import sys
import os
import cli
import gui
from excel_preference_manager import PreferenceManager
import tools
from db_scripts import AIGeneratorDB

APP_REQUIRED_DIRS = ["appdata", "appdata/logs", "appdata/profile"]

tools.create_app_require_directories(APP_REQUIRED_DIRS)
tools.configure_logging("appdata/logs/app.log")


def main() -> None:
    """
    A function that serves as the entry point of the program.
    It initializes the preference manager, fetches categories and sites,
    and determines whether to start the CLI or GUI version based on the arguments provided.

    Does not take any parameters and does not return anything.

    More Info:
        - If provided args are "CLI" or "cli", it starts the CLI version of the application.
        - If provided args are "GUI" or "gui", it starts the GUI version of the application.
        - If no args are provided, it starts the default CLI version of the application.
    """
    preference_manager = PreferenceManager()
    categories, categories_sites_mapping = preference_manager.fetch_categories_and_sites()
    sites_preferences: dict = preference_manager.fetch_sites_preferences()

    sites = []
    for value in categories_sites_mapping.values():
        sites += value
    AIGeneratorDB().insert_sites_if_not_exist(list(set(sites)))

    # driver = tools.get_webdriver_instance(profile_dir_path=f"{os.getcwd()}/appdata/profile")
    # driver.maximize_window()
    driver = None

    if len(sys.argv) > 1:
        if sys.argv[1] in ["CLI", "cli"]:
            logging.info("CLI version specified. Starting CLI version...")
            cli.main(categories, categories_sites_mapping, sites_preferences, driver)
        elif sys.argv[1] in ["GUI", "gui"]:
            logging.info("GUI version specified. Starting GUI version...")
            gui.main(categories, categories_sites_mapping, sites_preferences, driver)
        else:
            logging.error("Invalid args. Starting default CLI version...")
            cli.main(categories, categories_sites_mapping, sites_preferences, driver)
    else:
        logging.info("No args specified. Starting default GUI version...")
        gui.main(categories, categories_sites_mapping, sites_preferences, driver)


if __name__ == "__main__":
    main()
