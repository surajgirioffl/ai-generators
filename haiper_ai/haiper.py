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

    def login_with_google(self) -> None:
        """Function to login to haiper using Google authentication.

        Args:
            driver (Chrome | Edge | Any): The driver to interact with the browser.

        Returns:
            None
        """
        self.driver.get(URL)

        # Click on the button 'login with Google' when it appears
        login_with_google_xpath = "/html/body/main/article/section/div/div[1]/div[2]/button[2]"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, login_with_google_xpath))).click()

        # Wait until login success
        self.wait.until(EC.url_contains("haiper.ai/explore"))
