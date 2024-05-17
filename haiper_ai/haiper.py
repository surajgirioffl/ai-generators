"""Module to handle all the operations related to haiper.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 17th May 2024
Last-modified: 18th May 2024
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

    def login_with_google(self) -> bool:
        """Function to login to haiper using Google authentication.

        Args:
            driver (Chrome | Edge | Any): The driver to interact with the browser.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        logging.info("Login Haiper via Google authentication.")
        self.driver.get(URL)

        try:
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
        except Exception as e:
            print("Login failed. Error Code: 1401")
            logging.error("Login failed. Error Code: 1401")
            logging.exception(f"Exception: {e}")
            return False
        else:
            logging.info("Login success.")
            return True

    def download_video(self, link: str, path: str, filename: str = None):
        """Download a video from the given link and save it to the specified path with an optional filename.

        Args:
            link (str): The URL of the video to download.
            path (str): The directory path where the video will be saved.
            filename (str, optional): The name of the file to save the video as. If not provided, a default filename will be generated.
        """
        if not filename:
            filename = datetime.now().strftime("pixverse_%Y%m%d%H%M%S.mp4")
        response = requests.get(link)
        with open(os.path.join(path, filename), "wb") as file:
            file.write(response.content)

    def fetch_generated_video_link(self):
        """A function to fetch the generated video link after a series of actions to locate and retrieve it."""
        logging.info("Started fetching generated video link.")
        try:
            # When submit button is clicked then url changes to 'creation page url' in few seconds.
            self.wait.until(EC.url_contains("haiper.ai/creations"))
        except Exception as e:
            print("Failed to fetch generated video link. Error Code: 1405")
            logging.error("Failed to fetch generated video link. Error Code: 1405")
            logging.info("Probably submit button is not clicked.")
            logging.exception(f"Exception: {str(e)}")
        else:
            logging.info("URL changes to haiper.ai/creations")
            sleep(2)
            wait = WebDriverWait(self.driver, 800)

            logging.info("Finding all containers with video ID.")
            # Wait until the generating/queuing message removed from the DOM.
            partial_id = "creation-card-"
            # video_id_containers = self.driver.find_elements(By.XPATH, f'//*[contains(@id, "{partial_id}")]') # Working
            video_id_containers = self.driver.find_elements(By.CSS_SELECTOR, "div[id*=creation-card-]")

            try:
                video_generating_info_div = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[text()="Queuing for generation"]'))
                )
            except Exception:
                video_generating_info_div = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[text()="Your video is being generated"]'))
                )
            else:
                video_generating_info_div = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[text()="Your video is being generated"]'))
                )
            logging.info("Video generation info div is located.")

            container_video_id = None
            for container in video_id_containers:
                if video_generating_info_div in container.find_elements(By.TAG_NAME, "div"):
                    container_video_id = container.get_attribute("id")
                    break

            if container_video_id:
                video_id = container_video_id.strip(partial_id)
                logging.info("Video ID found.")
            else:
                logging.critical("Video ID not found. Means video generation info div is not included in any of video_id_containers.")

            # Wait until video generation is in process.
            wait.until_not(EC.presence_of_element_located((By.XPATH, '//div[text()="Your video is being generated"]')))

            self.driver.get(f"https://haiper.ai/creation/{video_id}")  # Opening the video page
            mp4_link = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "video"))).get_attribute("src")
            self.driver.get("https://haiper.ai/explore")  # Opening the explore page
            return mp4_link

    def create_video_with_prompt(self, prompt: str, seed: str | int, duration: str | int = 2):
        """Create video with the given prompt text, seed value, and optional duration setting.

        Parameters:
            prompt (str): The text prompt for the video.
            seed (str | int): The seed value for the video.
            duration (str | int, optional): The duration setting for the video. Defaults to 2 seconds.

        Returns:
            bool: True if video creation is successful, False otherwise.
        """
        logging.info("Creating video with the given prompt.")
        try:
            create_video_with_text_div_xpath = "/html/body/main/article/section/div/div/div[2]/div[1]/div/div/div/div[1]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, create_video_with_text_div_xpath))).click()

            self.driver.find_element(By.TAG_NAME, "textarea").send_keys(prompt)  # Prompt
            option_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Creation Setting"]')
            option_button.click()  # Clicking option button
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='seed']"))).send_keys(seed)  # seed

            duration_2_sec_button_selector = "button[value='2']"  # default value in haiper
            duration_4_sec_button_selector = "button[value='4']"
            if str(duration) == "4":
                self.driver.find_element(By.CSS_SELECTOR, duration_4_sec_button_selector).click()
            else:
                self.driver.find_element(By.CSS_SELECTOR, duration_2_sec_button_selector).click()

            logging.debug("Going to click on the create button.")
            # create_button = option_button.find_element(By.XPATH, "./following-sibling::button[1]")
            wait = WebDriverWait(option_button, 30)
            wait.until(EC.element_to_be_clickable((By.XPATH, "./following-sibling::button[1]"))).click()  # Clicking create button
        except Exception as e:
            print("Something went wrong while generating video with prompt. Error Code: 1402")
            logging.error("Something went wrong while generating video with prompt. Error Code: 1402")
            logging.exception(f"Exception: {e}")
            return False
        else:
            logging.info("Create button clicked. Generating video.")
            return True

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

        try:
            animate_your_image_div_xpath = "/html/body/main/article/section/div/div/div[2]/div[1]/div/div/div/div[2]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, animate_your_image_div_xpath))).click()

            # Image upload
            self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(image_path)
            if prompt:
                self.driver.find_element(By.TAG_NAME, "textarea").send_keys(prompt)  # Prompt

            option_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Creation Setting"]')
            option_button.click()  # Clicking option button
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='seed']"))).send_keys(seed)  # seed

            duration_2_sec_button_selector = "button[value='2']"  # default value in haiper
            duration_4_sec_button_selector = "button[value='4']"
            if str(duration) == "4":
                self.driver.find_element(By.CSS_SELECTOR, duration_4_sec_button_selector).click()
            else:
                self.driver.find_element(By.CSS_SELECTOR, duration_2_sec_button_selector).click()

            # Waiting until the image uploaded and the submit-button will clickable.
            wait_until_image_uploaded()

            logging.debug("Going to click on the create button.")
            # create_button = option_button.find_element(By.XPATH, "./following-sibling::button[1]")
            wait = WebDriverWait(option_button, 30)
            wait.until(EC.element_to_be_clickable((By.XPATH, "./following-sibling::button[1]"))).click()  # Clicking create button
        except Exception as e:
            print("Something went wrong while generating video with image. Error Code: 1403")
            logging.error("Something went wrong while generating video with image. Error Code: 1404")
            logging.exception(f"Exception: {e}")
            return False
        else:
            logging.info("Create button clicked. Generating video.")
            return True
