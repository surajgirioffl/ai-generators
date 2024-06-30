"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 29th May 2024
Last-modified: 30th June 2024
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
    from db_scripts import AIGeneratorDB
    from .pixlr import Pixlr


logging.info(f"Old CWD: {os.getcwd()}")
logging.info("Changing CWD.")
PROJECT_DIR = os.path.dirname(__file__)
os.chdir(PROJECT_DIR)
logging.info(f"New CWD: {os.getcwd()}")

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
    logging.info("Starting Pixlr AI...")
    local_webdriver = False
    if not driver:
        driver = tools.get_webdriver_instance()
        driver.maximize_window()
        local_webdriver = True

    pixlr = Pixlr(driver)

    if site_preferences.get("login_required"):
        pixlr.login(SETTINGS["pixlr_credentials"]["email"], SETTINGS["pixlr_credentials"]["password"])

    prompts: list | str = site_preferences["options"]["prompt"]
    prompts: list = prompts if isinstance(prompts, list) else [prompts]
    logging.info(f"Total number of prompts in this batch is {len(prompts)}")

    db = AIGeneratorDB()

    for index, prompt in enumerate(prompts):
        site_preferences["options"]["prompt"] = prompt
        logging.info(f"Initiating image generation for the prompt index {index}...")
        pixlr.generate_image(**site_preferences["options"])
        downloaded_images_path = pixlr.download_images(pixlr.fetch_images_link(), "output")
        logging.info(f"Done for the prompt index {index} (Message by Pixlr)")

        # Saving the required entities into the database
        db.insert_output(
            file_path=downloaded_images_path,
            category=site_preferences["category"],
            site_id=db.get_site_id(site_preferences["site"]),
            prompt_id=db.insert_prompt(prompt),
        )
        logging.info("Output details successfully inserted into the database...")

    if local_webdriver:
        driver.quit()
    return True


if __name__ == "__main__":
    main()
