"""Module to handle all operations related to the Pixlr.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 27th May 2024
Last-modified: 1st June 2024
Error-series: 1200
"""

import logging
from typing import Any
from datetime import datetime
import base64
import os
import time
from selenium.webdriver import Chrome, Edge
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


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

    def generate_image(
        self,
        prompt: str,
        aspect: str = None,
        style: str = None,
        color: str = None,
        lighting: str = None,
        composition: str = None,
        negative_prompt: str = None,
    ) -> None:
        logging.info("Generating image...")
        if "pixlr.com/image-generator" not in self.driver.current_url:
            logging.info("URL of image generator page not found. Redirecting...")
            self.driver.get(self.URL)

        # Clicking on the prompt-options container. So, all elements appear on the screen.
        self.wait.until(EC.visibility_of_element_located((By.ID, "generator-main-modal"))).click()

        # Writing prompt
        self.wait.until(EC.visibility_of_element_located((By.ID, "generator-positive"))).send_keys(prompt)
        logging.info("Prompt written successfully...")

        # Negative prompt if provided
        if negative_prompt:
            # Clicking on negative prompt toggle checkbox
            # self.driver.find_element(By.ID, "negative-prompt-toggle").click() # Not working
            self.driver.execute_script('document.querySelector("#negative-prompt-toggle").click()')
            # Writing negative prompt
            self.wait.until(EC.visibility_of_element_located((By.ID, "generator-negative"))).send_keys(negative_prompt)
            logging.info("Negative prompt written successfully...")

        logging.info("It's time to select options if provided else default will use...")
        # selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable (Means we can't interact with that element. Cause may be element is hidden, required hover to visible...)
        # Above exception is raised when I have tried to click on the options that visible after mouse hover.
        # So, I am going to use ActionChain to simulate the mouse hover, so element became interactable and then click.

        options: dict[str, dict[str, str]] = {
            "aspect": {
                "Square": "aspect-square",
                "Wide": "aspect-wide",
                "Tall": "aspect-tall",
            },
            "style": {
                "None": "style-none",
                "Enhance": "style-enhance",
                "Anime": "style-anime",
                "Photographic": "style-photographic",
                "Digital Art": "style-digital-art",
                "Comic Book": "style-comic-book",
                "Fantasy Art": "style-fantasy-art",
                "Analog Film": "style-analog-film",
                "Neon Punk": "style-neon-punk",
                "Isometric": "style-isometric",
                "Low Poly": "style-low-poly",
                "Origami": "style-origami",
                "Line Art": "style-line-art",
                "Craft Clay": "style-craft-clay",
                "Cinematic": "style-cinematic",
                "3D Model": "style-3d-model",
                "Pixel Art": "style-pixel-art",
            },
            "color": {
                "None": "color-none",
                "Warm Tone": "color-warm-tone",
                "Cool Tone": "color-cool-tone",
                "Muted Colors": "color-muted-colors",
                "Vibrant Colors": "color-vibrant-colors",
                "Pastel Colors": "color-pastel-colors",
                "Black And White": "color-black-and-white",
            },
            "lighting": {
                "None": "lighting-none",
                "Studio": "lighting-studio",
                "Backlight": "lighting-backlight",
                "Sunlight": "lighting-sunlight",
                "Dramatic": "lighting-dramatic",
                "Low Light": "lighting-low-light",
                "Volumetric": "lighting-volumetric",
                "Rim Lighting": "lighting-rim-lighting",
                "Dimly Lit": "lighting-dimly-lit",
                "Golden Hour": "lighting-golden-hour",
                "Crepuscular Rays": "lighting-crepuscular-rays",
            },
            "composition": {
                "None": "composition-none",
                "Blurry Background": "composition-blurry-background",
                "Close Up": "composition-close-up",
                "Wide Angle": "composition-wide-angle",
                "Narrow Depth Of Field": "composition-narrow-depth-of-field",
                "Shot From Below": "composition-shot-from-below",
                "Shot From Above": "composition-shot-from-above",
                "Macrophotography": "composition-macrophotography",
            },
        }
        actions = ActionChains(self.driver)
        self.actions: ActionChains = actions

        aspect_option_button_label = self.driver.find_element(By.ID, "aspect-type-label")
        style_option_button_label = self.driver.find_element(By.ID, "style-type-label")
        color_option_button_label = self.driver.find_element(By.ID, "color-type-label")
        lighting_option_button_label = self.driver.find_element(By.ID, "lighting-type-label")
        composition_option_button_label = self.driver.find_element(By.ID, "composition-type-label")

        if aspect:
            self.actions.move_to_element(aspect_option_button_label).click_and_hold().perform()
            self.driver.find_element(By.ID, options["aspect"][aspect.title()]).click()

        if style:
            self.actions.move_to_element(style_option_button_label).click_and_hold().perform()
            self.driver.find_element(By.ID, options["style"][style.title()]).click()

        if color:
            self.actions.move_to_element(color_option_button_label).click_and_hold().perform()
            self.driver.find_element(By.ID, options["color"][color.title()]).click()

        if lighting:
            self.actions.move_to_element(lighting_option_button_label).click_and_hold().perform()
            self.driver.find_element(By.ID, options["lighting"][lighting.title()]).click()

        if composition:
            self.actions.move_to_element(composition_option_button_label).click_and_hold().perform()
            self.driver.find_element(By.ID, options["composition"][composition.title()]).click()

        generate_button_selector = ".button.med.positive.but"
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, generate_button_selector))).click()
        logging.info("Generate button clicked successfully....")

    def fetch_images_link(self) -> list:
        logging.info("Fetching images link...")
        wait = WebDriverWait(self.driver, 300)

        # Image container appears immediately after 'Generate' button is clicked. If it doesn't appear means 'Generator' button is not clicked or failed to clicked.
        logging.info("Waiting for the image container to appear. When 'Generate button' is clicked, it appears immediately.")
        t1 = time.time()
        image_container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pane")))
        t2 = time.time()
        logging.debug(f"Image container appeared in {t2-t1} seconds")

        # Images are displayed when generation completed. It may take from 15 sec to 300 sec.
        logging.info("Waiting for image to appear...")
        t1 = time.time()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img.result")))
        t2 = time.time()
        logging.debug(f"Images appeared in {t2-t1} seconds")

        images = image_container.find_elements(By.CSS_SELECTOR, "img.result")
        logging.info("Images links fetched successfully...")
        return [image.get_attribute("src") for image in images]
