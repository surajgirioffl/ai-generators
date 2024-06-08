"""Driver module to integrate and execute the script.

Driver module to integrate and execute the script.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 23rd May 2024
Last-modified: 27th May 2024
Error-series: 1100
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"

import os
import tools
from .wordhero import WordHero


APP_REQUIRED_DIRS = ["appdata", "appdata/logs", "appdata/profile"]
SETTINGS: dict = tools.load_settings()


tools.create_app_require_directories(APP_REQUIRED_DIRS)
tools.configure_logging(SETTINGS["logging_location"])

driver = tools.get_webdriver_instance(profile_dir_path=f"{os.getcwd()}/appdata/profile")
driver.maximize_window()

wordhero = WordHero(driver)
wordhero.login_to_wordhero(SETTINGS["wordhero_credentials"]["email"], SETTINGS["wordhero_credentials"]["password"])
# wordhero.fetch_all_blog_tools()

wordhero.generate_article("what doesn't work in nutrition related to weight loss", "funny", 2000)
driver.quit()
exit()

flag = True
while True:
    prompt = input("Write prompt: ").strip()
    if flag:
        response = wordhero.generate_content_with_chat(prompt)
        flag = False
    else:
        response = wordhero.generate_content_with_chat(prompt, new_chat=False)

    print(response)
    print()
    print(f"Last response: {response[prompt]}")
    print()
