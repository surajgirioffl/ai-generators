"""Module to handle all operations related to the Pixlr.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 27th May 2024
Last-modified: 29th May 2024
Error-series: 1200
"""

import logging
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

    def login(self, email: str, password: str) -> None:
        """
        Logs into Pixlr using the provided email and password.

        Parameters:
            email (str): The email to use for logging in.
            password (str): The password to use for logging in.

        Returns:
            None
        """
        logging.info("Logging to Pixlr using email and password...")
        self.driver.get(Pixlr.URL)

        # Click on login button
        self.wait.until(EC.visibility_of_element_located((By.ID, "head-login"))).click()

        # Use email password to login instead of login with Google/Facebook/Apple
        # Clicking on the button having text 'Or use email' (Means login using email)
        self.driver.find_element(value="choose-email").click()

        # Writing email and password
        self.wait.until(EC.visibility_of_element_located((By.ID, "entry-email"))).send_keys(email)
        self.driver.find_element(value="entry-password").send_keys(password)

        # Clicking on the submit button
        self.wait.until(EC.element_to_be_clickable((By.ID, "entry-submit"))).click()

        logging.info("Email-password submitted successfully. Waiting for login to complete...")

        # Use logic to wait until the login successful (Like login/signup button disappear after success)
        self.wait.until(EC.invisibility_of_element_located((By.ID, "head-login")))
        logging.info("Logging successful...")
