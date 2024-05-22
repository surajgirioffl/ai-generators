"""Module to handle all the operations related to LensGo.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 22nd May 2024
Last-modified: 22nd May 2024
Error-series: 1800
"""

import logging
import os
from time import sleep
from typing import Any, Literal
from datetime import datetime
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, Edge
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

URL = "https://lensgo.ai/"


class LensGo:
    """Class to handle all operations related to the LensGo."""

    def __init__(self, driver: Chrome | Edge | Any):
        """Constructor of LensGo class.
        Initializes the class with the given driver object and sets up a WebDriverWait object.

        Args:
            driver (Chrome | Edge | Any): The driver object to be used for the class.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)
