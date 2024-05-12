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


def create_video_from_prompt(driver: Chrome | Edge | Any, prompt: str, seed: int | str):
    """Creates a video based on a given prompt using the provided driver.

    Args:
        driver (Chrome | Edge | Any): The web driver to use for interacting with the webpage.
        prompt (str): The prompt to base the video on.
        seed (int | str): The seed value to use for generating the video.

    Returns:
        None
    """
    logging.info("Creating video from prompt...")
    wait = WebDriverWait(driver, 20)

    # Click on the 'create video' button when it appears
    create_video_button_selector = ".ant-btn.css-sjdo89.ant-btn-default.px-8.border-none.rounded-full"
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, create_video_button_selector))).click()

    text_button_selector = ".p-2.rounded-md.cursor-pointer.flex.items-center.gap-2"
    driver.find_element(By.CSS_SELECTOR, text_button_selector).click()
    driver.find_element(By.ID, "Prompt").send_keys(prompt)  # Prompt
    seed_button_selector = 'input[role="spinbutton"]'
    driver.find_element(By.CSS_SELECTOR, seed_button_selector).send_keys(seed)
    submit_button_selector = 'button[type="submit"]'
    driver.find_element(By.CSS_SELECTOR, submit_button_selector).click()
