"""Module to handle all the operations related to ideogram.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 20th May 2024
Last-modified: 17th June 2024
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
from selenium.webdriver.common.action_chains import ActionChains

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
            self.wait.until(
                EC.url_contains("ideogram.ai/t/")
            )  # Link may be "https://ideogram.ai/t/top/1" or  https://ideogram.ai/t/explore
        except Exception as e:
            print("Login failed. Error Code: 1601")
            logging.error("Login failed. Error Code: 1601")
            logging.exception(f"Exception: {e}")
            return False
        else:
            logging.info("Login success.")
            return True

    def download_images(self, links: list[str], path: str, filenames: list[str] = None) -> list[str]:
        """Download images from a list of links to the specified path with optional custom filenames.

        Parameters:
            links (list[str]): A list of URLs pointing to the images to be downloaded.
            path (str): The local directory path where the images will be saved.
            filenames (list[str], optional): A list of custom filenames corresponding to the downloaded images. Defaults to None.

        Returns:
            list[str]: A list of absolute paths to the downloaded images.
        """
        logging.info("Downloading started...")
        headers = {
            "authority": "ideogram.ai",
            "method": "GET",
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
            "Cache-Control": "max-age=0",
            "Dnt": "1",
            "Priority": "u=0, i",
            "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-Gpc": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }
        for index, link in enumerate(links):
            if not filenames:
                filename = datetime.now().strftime(f"ideogram_%Y%m%d%H%M%S_{index}.jpg")
            else:
                filename = filenames[index]

            headers["path"] = link.lstrip("https://ideogram.ai")  # This is one of the header

            created_filenames: list = []

            while True:
                with requests.Session() as session:
                    session.headers.update(headers)
                    response = session.get(link)
                    if response.headers.get("Content-Type") == "image/jpeg":
                        with open(os.path.join(path, filename), "wb") as file:
                            file.write(response.content)
                            created_filenames.append(file.name)
                            break
                    else:
                        # In case of error, retry. Means that the response content is not an image.
                        logging.error("Response content is not an image. Retrying...")
        logging.info("Download completed.")
        return created_filenames

    def fetch_images_link(self, prompt: str) -> list:
        """A function to fetch generated image links.

        Parameters:
            prompt (str): The prompt string that has been used to generate the images.

        Returns:
            list: A list of image links fetched based on the prompt.
        """
        logging.info("Fetching images links...")
        wait = WebDriverWait(self.driver, 300)
        # Wait until the paragraph contents changes to "Generation completed"
        logging.info("waiting for generation to complete...")
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1.css-vsgu40"), "Generation completed"
            )
        )
        logging.info("Generation completed.")
        links = []
        prompt = prompt.strip().strip(".").replace(" ", "_")
        if len(prompt) > 40:
            prompt = prompt[:40]
        request_response_div = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"div[data-download-name*='{prompt}']")))
        data_request_id = request_response_div.get_attribute("data-request-id")
        logging.info(f"Request ID: {data_request_id}")
        image_page_link = f"https://ideogram.ai/g/{data_request_id}/0"  # 0 or 1 or 2 or 3 or 4 (because 4 images are generated)
        logging.info("Image page link fetched successfully.")

        self.driver.get(image_page_link)
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'img[src*="/api"]')))
        images = self.driver.find_elements(By.CSS_SELECTOR, 'img[src*="/api"]')
        # print(f"images: {images}")
        for image in images:
            link = image.get_attribute("src")
            print(link)
            if link.endswith(".png"):
                # There are 4 images to be fetched but 5 images are returned by the above selector because one image is current page image and it only contains src with .png.
                # So, we skip this page specific image. BTW in rest 4, this image is also including with .jpg src.
                continue
            links.append(link)
        # print(links)
        logging.info("Fetched all images links successfully.")
        return list(set(links))

    def create_image_with_prompt(self, prompt: str, *args, **kwargs):
        """Function that creates an image with the provided prompt.

        Args:
            prompt (str): The prompt text to be used for generating the image.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None

        Raises:
            ValueError: If prompt is not provided.
        """
        logging.info("Creating image with prompt...")

        if not prompt:
            logging.error("Please provide a prompt. Error Code: 1602")
            logging.error("prompt is required parameters. If it is missing, this error will be raised.")
            raise ValueError("Please provide a valid prompt. Error Code: 1602")

        if "ideogram.ai/t/" not in self.driver.current_url:
            logging.info("Navigating to ideogram.ai/t/top/1")
            self.driver.get("https://ideogram.ai/t/top/1")

        screen_width = self.driver.execute_script("return window.innerWidth")
        if screen_width >= 900:
            logging.info("Screen width is greater that 900px (or equal to)")
            logging.info("Trying to fetch the textarea element.")
            # In this case, there are two textarea elements with same selector. By fetching using querySelector, index may be different for desired textarea in different session.
            # In all possibility, two textarea are returning.
            prompt_textarea_selector = "textarea[placeholder='What do you want to create?']"
            self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, prompt_textarea_selector)))
            textarea_elements = self.driver.find_elements(By.CSS_SELECTOR, prompt_textarea_selector)

            # Using same logic as we used in the button (given below). Using clientWidth to determine if element is visible or not.
            for textarea_element in textarea_elements:
                if int(textarea_element.get_property("clientWidth")) > 0:
                    textarea_element.send_keys(prompt)
                    break
            logging.info("Prompt written successfully..")

            # There are two generate buttons. And By fetching using querySelector, index may be different for desired textarea in different session.
            # No other properties like width, style.visibility, display etc working because both elements have same property but one is not visible but visibility is not set using display or style.visibility.
            # Solution is clientWidth, clientHeight, clientTop, clientLeft. element.<any_of_this_property> return value greater than 0 if element visible on the screen and have some size.
            # The clientWidth property returns the viewable width of an element in pixels, including padding, but not the border, scrollbar or margin. (Similar in case of other properties from the above line)
            generate_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Generate"]')
            logging.info(f"Number of Generate buttons: {len(generate_buttons)}")
            if len(generate_buttons) > 1:
                logging.info(f"Button-1 size: {generate_buttons[0].size}")
                logging.info(f"Button-2 size: {generate_buttons[1].size}")  # size: {'height': 23, 'width': 75}
            else:
                logging.info(f"Button-1 size: {generate_buttons[1].size}")
            # logging.info(generate_buttons[1].get_dom_attribute("clientWidth"))  # None (For DOM attributes only)
            # logging.info(generate_buttons[1].get_property("clientWidth"))  # 75
            for generate_button in generate_buttons:
                if int(generate_button.get_property("clientWidth")) > 0:
                    generate_button.click()
                    break
            logging.info("Generate button clicked successfully..")
        else:
            logging.info("Screen width is less than 900px")
            logging.info("Trying to fetch the textarea element.")
            # Below svg(+ icon) is visible only when screen width is less than 900 px. And after clicking on this only text area is visible.
            self.driver.find_element(By.CSS_SELECTOR, 'svg[data-testid="AddIcon"]').click()
            # In this case there is only one textarea
            prompt_textarea_selector = "textarea[placeholder='What do you want to create?']"
            self.driver.find_element(By.CSS_SELECTOR, prompt_textarea_selector).send_keys(prompt)
            logging.info("Prompt written successfully..")

            # Clicking on the generate button. There is only one generate button in this case.
            self.driver.find_element(By.XPATH, '//button[text()="Generate"]').click()
            logging.info("Generate button clicked successfully..")
