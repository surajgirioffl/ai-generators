"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 29th May 2024
Last-modified: 29th May 2024
Error-series: 1400
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"

import os
from time import sleep
import tools
from .pixlr import Pixlr


PROJECT_DIR = os.path.dirname(__file__)
os.chdir(PROJECT_DIR)

APP_REQUIRED_DIRS = ["appdata", "appdata/logs", "appdata/profile", "output"]
SETTINGS: dict = tools.load_settings("config.json")

tools.create_app_require_directories(APP_REQUIRED_DIRS)
tools.configure_logging(SETTINGS["logging_location"])


def main():
    driver = tools.get_webdriver_instance(profile_dir_path=f"{PROJECT_DIR}/appdata/profile")
    driver.maximize_window()
    pixlr = Pixlr(driver)

    if SETTINGS["login_required"]:
        pixlr.login(SETTINGS["pixlr_credentials"]["email"], SETTINGS["pixlr_credentials"]["password"])

    with open("prompt.txt") as file:
        prompt = file.read()

    pixlr.generate_image(prompt)
    pixlr.download_images(pixlr.fetch_images_link(), "output")
    print("Done........................................")
    sleep(300)
    driver.quit()


if __name__ == "__main__":
    main()
