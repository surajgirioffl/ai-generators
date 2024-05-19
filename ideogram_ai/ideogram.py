"""Module to handle all the operations related to ideogram.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 20th May 2024
Last-modified: 20th May 2024
Error-series: 1600
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

URL = "https://ideogram.ai/"


class Ideogram:
    """Class to handle all operations related to the Ideogram."""

    def __init__(self, driver: Chrome | Edge | Any):
        """Constructor of Ideogram class.
        Initializes the class with the given driver object and sets up a WebDriverWait object.

        Args:
            driver (Chrome | Edge | Any): The driver object to be used for the class.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)

    def login_with_google(self) -> bool:
        """Function to login to ideogram using Google authentication.

        Args:
            driver (Chrome | Edge | Any): The driver to interact with the browser.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        logging.info("Login Ideogram via Google authentication.")
        self.driver.get(URL)

        try:
            # Click on the button 'login with Google' when it appears
            login_with_google_xpath = '//*[@id="root"]/div[1]/div/div[3]/button[1]'
            self.wait.until(EC.element_to_be_clickable((By.XPATH, login_with_google_xpath))).click()

            # Wait until login success
            self.wait.until(EC.url_contains("ideogram.ai/t/top/1"))
        except Exception as e:
            print("Login failed. Error Code: 1601")
            logging.error("Login failed. Error Code: 1601")
            logging.exception(f"Exception: {e}")
            return False
        else:
            logging.info("Login success.")
            return True
