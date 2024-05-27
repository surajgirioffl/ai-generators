"""Module to handle all operations related to the Pixlr.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 27th May 2024
Last-modified: 27th May 2024
Error-series: 1500
"""

from typing import Any
from selenium.webdriver import Chrome, Edge
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Pixlr:
    """Class to handle all operations related to the Pixlr"""

    URL = "https://pixlr.com/image-generator/"

    def __init__(self, driver: Chrome | Edge | Any | None) -> None:
        """Constructor of WordHero class.
        Initializes the class with the given driver object and sets up a WebDriverWait object.

        Args:
            driver (Chrome | Edge | Any): The driver object to be used for the class.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)
