"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 23rd May 2024
Last-modified: 17th June 2024
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
    from db_scripts import AIGeneratorDB


PROJECT_DIR = os.path.dirname(__file__)
os.chdir(PROJECT_DIR)  # Changing the current working directory to the project directory.
SETTINGS: dict = tools.load_settings("config.json")

APP_REQUIRED_DIRS = ["appdata", "appdata/logs", "appdata/profile", SETTINGS["output_location"]]
tools.create_app_require_directories(APP_REQUIRED_DIRS)
tools.configure_logging(SETTINGS["logging_location"])


def main(site_preferences: dict, driver=None, *args, **kwargs):
    """
    A function that generates an article using WordHero based on site preferences.

    Parameters:
        site_preferences (dict): A dictionary containing preferences for the site.
        driver (WebDriver, optional): An instance of a WebDriver, defaults to None. If not passed then local web driver will be created.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        bool: True if the article is generated successfully, False otherwise.

    More Info:
        - site_preferences will like: {"login_required": True, "options": {"title": "Title of the article", "description": "Description of the article", "keywords": "Keywords of the article"}}
    """
    local_webdriver = False
    if not driver:
        # driver = tools.get_webdriver_instance(profile_dir_path=f"{os.getcwd()}/appdata/profile")
        driver = tools.get_webdriver_instance()
        driver.maximize_window()
        local_webdriver = True

    wordhero = WordHero(driver)
    if site_preferences.get("login_required"):
        wordhero.login_to_wordhero(SETTINGS["wordhero_credentials"]["email"], SETTINGS["wordhero_credentials"]["password"])

    prompts: list | str = site_preferences["options"]["prompt"]  # In case of wordhero, prompts are headline only
    prompts: list = prompts if isinstance(prompts, list) else [prompts]
    logging.info(f"Total number of headlines in this batch is {len(prompts)}")

    db = AIGeneratorDB()

    for index, headline in enumerate(prompts):
        site_preferences["options"]["headline"] = headline
        logging.info(f"Going to generate article {index} of the batch...")
        generated_article, prompt_response_mapping = wordhero.generate_article(**site_preferences["options"])
        logging.info("Article generated successfully...")
        output_filepath = WordHero.save_content(generated_article, SETTINGS["output_location"])
        logging.info(f"Article {index} of the batch saved successfully...")

        # Saving the required entities into the database
        db.insert_output(
            file_path=output_filepath,
            category=site_preferences["category"],
            site_id=db.get_site_id(site_preferences["site"]),
            prompt_id=db.insert_prompt(headline),
        )
        logging.info("Output details successfully inserted into the database...")

    # Quitting the driver instance if local_webdriver
    if local_webdriver:
        driver.quit()
    return True
