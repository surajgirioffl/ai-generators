"""Module to handle all operations related to the WordHero.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 23rd May 2024
Last-modified: 23rd May 2024
Error-series: 1200
"""

from typing import Any
from selenium.webdriver import Chrome, Edge
from selenium.webdriver.support.wait import WebDriverWait


class WordHero:
    """Class to handle all operations related to the WordHero."""

    def __init__(self, driver: Chrome | Edge | Any | None):
        """Constructor of WordHero class.
        Initializes the class with the given driver object and sets up a WebDriverWait object.

        Args:
            driver (Chrome | Edge | Any): The driver object to be used for the class.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)
