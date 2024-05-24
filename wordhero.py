"""Module to handle all operations related to the WordHero.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 23rd May 2024
Last-modified: 25th May 2024
Error-series: 1200
"""

import logging
from typing import Any
from selenium.webdriver import Chrome, Edge
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class WordHero:
    """Class to handle all operations related to the WordHero."""

    URL = "https://app.wordhero.co/"

    def __init__(self, driver: Chrome | Edge | Any | None):
        """Constructor of WordHero class.
        Initializes the class with the given driver object and sets up a WebDriverWait object.

        Args:
            driver (Chrome | Edge | Any): The driver object to be used for the class.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)

    def login_to_wordhero(self, email: str, password: str, stay_logged_in: bool = True) -> bool:
        """Logs into WordHero using the provided email and password.

        Parameters:
            email (str): The email address used for login.
            password (str): The password for the account.
            stay_logged_in (bool, optional): Whether to stay logged in (default is True).

        Returns:
            bool: True if login is successful, False otherwise.
        """
        logging.info("Login to the WordHero...")
        self.driver.get(WordHero.URL + "login")  # We can also use self.URL.
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys(email)  # Email input
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys(password)  # Password input

        if stay_logged_in:
            stay_logged_in_checkbox = self.driver.find_element((By.CSS_SELECTOR, 'input[type="checkbox"]'))
            if not stay_logged_in_checkbox.get_property("checked"):
                stay_logged_in_checkbox.click()

        # Clicking on the log-in button
        self.driver.find_element((By.CSS_SELECTOR, "button")).click()
        logging.info("Clicked on log-in button...")

        # Checking if login successful or not
        try:
            self.wait.until(EC.url_contains("app.wordhero.co/home"))
        except TimeoutException as e:
            logging.exception(f"Error in login: {e}. Error Code: 1201")
            logging.exception("Home page URL not found after login attempt.")
            return False
        else:
            logging.info("Login successful.")
            return True


if __name__ == "__main__":
    pass
