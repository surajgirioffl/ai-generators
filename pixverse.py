"""Module to handle all the operations related to pixverse.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 9th May 2024
Last-modified: 9th May 2024
Error-series: 1200
"""

import logging
from time import sleep
from typing import Any
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, Edge
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


URL = "https://app.pixverse.ai/login"


def login_with_google(driver: Chrome | Edge | Any) -> None:
    """Function to login using Google authentication.

    Args:
        driver (Chrome | Edge | Any): The driver to interact with the browser.

    Returns:
        None
    """
    driver.get(URL)
    wait = WebDriverWait(driver, 20)
    # Click on the button 'login with Google' when it appears
    login_with_google_selector = ".ant-btn.css-17a3nt7.ant-btn-default.w-full.border-none"
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, login_with_google_selector))).click()
