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
        logging.info("Login Haiper via Google authentication.")
        self.driver.get(URL)

        # Click on the button 'login with Google' when it appears
        login_with_google_xpath = "/html/body/main/article/section/div/div[1]/div[2]/button[2]"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, login_with_google_xpath))).click()

        # Account selection is compulsory in haiper
        logging.info("Selecting Google account.")
        self.wait.until(EC.url_contains("oauthchooseaccount"))  # Wait until account selection page opens
        select_account_div_xpath = (
            '//*[@id="yDmH0d"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/ul/li[1]/div'
        )
        self.wait.until(EC.element_to_be_clickable((By.XPATH, select_account_div_xpath))).click()

        # Wait until login success
        self.wait.until(EC.url_contains("haiper.ai/explore"))
        logging.info("Login success.")

    def create_video_with_prompt(self, prompt: str, seed: str | int, duration: str | int = 2):
        """Create video with the given prompt text, seed value, and optional duration setting.

        Parameters:
            prompt (str): The text prompt for the video.
            seed (str | int): The seed value for the video.
            duration (str | int, optional): The duration setting for the video. Defaults to 2 seconds.
        """
        logging.info("Creating video with the given prompt.")
        create_video_with_text_div_xpath = "/html/body/main/article/section/div/div/div[2]/div[1]/div/div/div/div[1]"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, create_video_with_text_div_xpath))).click()

        self.driver.find_element(By.TAG_NAME, "textarea").send_keys(prompt)  # Prompt
        self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Creation Setting"]').click()  # Clicking option button
        self.wait.until(EC.visibility_of_element_located((By.ID, ":rbd:"))).send_keys(seed)  # seed

        duration_2_sec_button_id = ":rbf:"  # default value in haiper
        duration_4_sec_button_id = ":rbh:"
        if str(duration) == "4":
            self.driver.find_element(value=duration_4_sec_button_id).click()
        else:
            self.driver.find_element(value=duration_2_sec_button_id).click()

        create_button_xpath = "/html/body/main/article/section/div/div/footer/div/form/div/div[3]/button[3]"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, create_button_xpath))).click()  # Clicking create button
        logging.info("Create button clicked. Generating video.")

    def create_video_with_image(self, image_path: str, seed: str | int, prompt: str = "", duration: str | int = 2):
        """A function to create a video with an image.

        Args:
            image_path (str): The path to the image file.
            seed (str | int): The seed for the video creation.
            prompt (str, optional): The prompt to be included. Defaults to ""(empty).
            duration (str | int, optional): The duration of the video. Defaults to 2.
        """
        logging.info("Creating video with the given image.")

        def wait_until_image_uploaded():
            """Wait until the image is uploaded by waiting for the presence of the specified CSS selector."""
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='thumbnail']")))

        animate_your_image_div_xpath = "/html/body/main/article/section/div/div/div[2]/div[1]/div/div/div/div[2]"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, animate_your_image_div_xpath))).click()

        # Image upload
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(image_path)
        if prompt:
            self.driver.find_element(By.TAG_NAME, "textarea").send_keys(prompt)  # Prompt

        self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Creation Setting"]').click()  # Clicking option button
        self.wait.until(EC.visibility_of_element_located((By.ID, ":r5r:"))).send_keys(seed)

        duration_2_sec_button_id = ":r5t:"  # default value in haiper
        duration_4_sec_button_id = ":r5v:__label"
        if str(duration) == "4":
            self.driver.find_element(value=duration_4_sec_button_id).click()
        else:
            self.driver.find_element(value=duration_2_sec_button_id).click()

        # Waiting until the image uploaded and the submit-button will clickable.
        wait_until_image_uploaded()

        create_button_xpath = "/html/body/main/article/section/div/div/footer/div/form/div/div[3]/button[3]"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, create_button_xpath))).click()  # Clicking create button
        logging.info("Create button clicked. Generating video.")
