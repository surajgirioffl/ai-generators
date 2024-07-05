"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 23rd May 2024
Last-modified: 5th July 2024
Error-series: 1100
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"

import os
import logging
from datetime import datetime

if __name__ == "__main__":
    import tools
    from wordhero import WordHero
else:
    # Relative import (for executing from the root project directory)
    from . import tools
    from .wordhero import WordHero
    from db_scripts import AIGeneratorDB

logging.info(f"Old CWD: {os.getcwd()}")
logging.info("Changing CWD.")
PROJECT_DIR = os.path.dirname(__file__)
os.chdir(PROJECT_DIR)  # Changing the current working directory to the project directory.
logging.info(f"New CWD: {os.getcwd()}")
SETTINGS: dict = tools.load_settings("config.json")

APP_REQUIRED_DIRS = ["appdata", "appdata/logs", "appdata/profile", SETTINGS["output_location"]]
tools.create_app_require_directories(APP_REQUIRED_DIRS)
tools.configure_logging(SETTINGS["logging_location"])


def generate_file_name(
    prompt: str = None,
    image_path=None,
    timestamp: datetime | str = None,
    index: int = None,
    timestamp_format: str = "%Y%m%d%H%M%S%f",
    extension: str = "txt",
) -> str:
    """Generates a file name based on the provided prompt, image path, timestamp, and index.

    Parameters:
        - prompt (str, optional): The prompt to be used in the file name. Defaults to None. (Compulsory if image_path is not provided).
        - image_path (any, optional): The path to the image. Defaults to None (Compulsory if prompt is not provided).
        - timestamp (datetime | str, optional): The timestamp to be included in the file name. Defaults to None. If not provided then datetime.now() will used.
        - index (int, optional): The index to be appended to the file name. Defaults to None.
        - timestamp_format (str, optional): The format of the timestamp. Defaults to "%Y%m%d%H%M%S%f".
        - extension (str, optional): The extension for the filename. Default to "txt".

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

    return f"{filename_prefix}_{str(timestamp)}_{index}.{extension}" if index else f"{filename_prefix}_{str(timestamp)}.{extension}"


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
        timestamp = datetime.now()
        filename = generate_file_name(prompt=headline, timestamp=timestamp, extension="txt")
        output_filepath = WordHero.save_content(generated_article, SETTINGS["output_location"], filename, headline)
        logging.info(f"Article {index} of the batch saved successfully...")

        # Saving the required entities into the database
        db.insert_output(
            file_path=output_filepath,
            category=site_preferences["category"],
            site_id=db.get_site_id(site_preferences["site"]),
            prompt_id=db.insert_prompt(headline),
            timestamp=timestamp,
        )
        logging.info("Output details successfully inserted into the database...")

    # Quitting the driver instance if local_webdriver
    if local_webdriver:
        driver.quit()
    return True
