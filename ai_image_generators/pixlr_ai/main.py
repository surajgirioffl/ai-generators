"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 29th May 2024
Last-modified: 06th July 2024
Error-series: 1400
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"

import os
from time import sleep
import tools
import logging
from datetime import datetime

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
    extension: str = None,
) -> str:
    """Generates a file name based on the provided prompt, image path, timestamp, and index.

    Parameters:
        - prompt (str, optional): The prompt to be used in the file name. Defaults to None. (Compulsory if image_path is not provided).
        - image_path (any, optional): The path to the image. Defaults to None (Compulsory if prompt is not provided).
        - timestamp (datetime | str, optional): The timestamp to be included in the file name. Defaults to None. If not provided then datetime.now() will used.
        - index (int, optional): The index to be appended to the file name. Defaults to None.
        - timestamp_format (str, optional): The format of the timestamp. Defaults to "%Y%m%d%H%M%S%f".
        - extension (str, optional): The extension for the filename. Default to "None". If not provided then filename without extension will return.

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
        images_links = pixlr.fetch_images_link()
        logging.info("Image links fetched successfully....")
        timestamp = datetime.now()
        filename = generate_file_name(prompt=prompt, timestamp=timestamp)
        downloaded_images_path = pixlr.download_images(images_links, SETTINGS["output_location"], filename)
        logging.info(f"Done for the prompt index {index} (Message by Pixlr)")

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
        driver.quit()
    return True


if __name__ == "__main__":
    main()
