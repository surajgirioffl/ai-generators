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

    def login_with_google(self) -> bool:
        """Function to login to LensGo using Google authentication.

        Args:
            driver (Chrome | Edge | Any): The driver to interact with the browser.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        logging.info("Login LensGo via Google authentication.")
        self.driver.get(URL)

        try:
            # Login with google appears by clicking log-in button or any other button performing any operation
            # Clicking on Log-in button. So, Login with Google pop-up div will appear.
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".no-login"))).click()

            # We can login via Google or using email & password.
            # Log-in using Google.
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".google-btn"))).click()

            # Account selection is compulsory in Lensgo
            logging.info("Selecting Google account.")
            self.wait.until(EC.url_contains("oauthchooseaccount"))  # Wait until account selection page opens
            select_account_div_xpath = (
                '//*[@id="yDmH0d"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/ul/li[1]/div'
            )
            self.wait.until(EC.element_to_be_clickable((By.XPATH, select_account_div_xpath))).click()

            # Wait until login success
            self.wait.until(EC.url_contains("lensgo"))
        except Exception as e:
            print("Login failed. Error Code: 1801")
            logging.error("Login failed. Error Code: 1801")
            logging.exception(f"Exception: {e}")
            return False
        else:
            logging.info("Login success.")
            return True
