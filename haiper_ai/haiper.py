"""Module to handle all the operations related to haiper.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 17th May 2024
Last-modified: 17th May 2024
Error-series: 1400
"""

import logging
import os
from time import sleep
from typing import Any
from datetime import datetime
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, Edge
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

URL = "https://haiper.ai/auth/signin"


class Haiper:
    """Class to handle all operations related to the Haiper."""

    def __init__(self, driver: Chrome | Edge | Any):
        """Constructor of Haiper class.
        Initializes the class with the given driver object and sets up a WebDriverWait object.

        Args:
            driver (Chrome | Edge | Any): The driver object to be used for the class.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)
