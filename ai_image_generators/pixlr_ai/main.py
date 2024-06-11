"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 29th May 2024
Last-modified: 11th June 2024
Error-series: 1400
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"

import os
from time import sleep
import tools
import logging

if __name__ == "__main__":
    from pixlr import Pixlr
else:
    from .pixlr import Pixlr


PROJECT_DIR = os.path.dirname(__file__)
os.chdir(PROJECT_DIR)

APP_REQUIRED_DIRS = ["appdata", "appdata/logs", "appdata/profile", "output"]
SETTINGS: dict = tools.load_settings("config.json")

tools.create_app_require_directories(APP_REQUIRED_DIRS)
tools.configure_logging(SETTINGS["logging_location"])


def main(site_preferences: dict, driver=None, *args, **kwargs):
    """Driver function to integrate and execute the script.

    Args:
        site_preferences (dict): A dictionary containing preferences for the site.
        driver (WebDriver, optional): An instance of a WebDriver, defaults to None. If not passed then local web driver will be created.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    local_webdriver = False
    if not driver:
        driver = tools.get_webdriver_instance(profile_dir_path=f"{PROJECT_DIR}/appdata/profile")
        driver.maximize_window()
        local_webdriver = True

    pixlr = Pixlr(driver)

    if site_preferences.get("login_required"):
        pixlr.login(SETTINGS["pixlr_credentials"]["email"], SETTINGS["pixlr_credentials"]["password"])

    pixlr.generate_image(**site_preferences["options"])
    pixlr.download_images(pixlr.fetch_images_link(), "output")
    logging.info("Done.... (Message by Pixlr)")

    if local_webdriver:
        driver.quit()
    return True


if __name__ == "__main__":
    main()
