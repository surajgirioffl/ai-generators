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


def create_video_from_images(
    driver: Chrome | Edge | Any,
    image_path: str,
    motion_strength: float | int | str,
    seed: int | str,
    prompt: str = "",
    hd=False,
):
    """Function to create video using image.

    Args:
        driver (Chrome | Edge | Any): the driver to use for the operation
        image_path (str): the path to the images to create the video from
        motion_strength (float | int | str): the strength of the motion for the video
        seed: int | str - the seed value for the video creation
        prompt (str): optional prompt for the video creation
        hd (bool): whether to enable HD quality for the video

    Result:
        None
    """
    logging.info("Creating video from images...")
    wait = WebDriverWait(driver, 20)

    # Click on the 'create video' button when it appears
    create_video_button_selector = ".ant-btn.css-sjdo89.ant-btn-default.px-8.border-none.rounded-full"
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, create_video_button_selector))).click()

    create_video_from_image_button_selector = ".p-2.rounded-md.cursor-pointer.flex.items-center.gap-2"
    driver.find_elements(By.CSS_SELECTOR, create_video_from_image_button_selector)[1].click()

    # Image upload button
    # image_upload_button_selector = ".ant-btn.css-1ntsptu.ant-btn-text.ant-btn-sm"
    image_file_input_selector = 'input[type="file"]'
    wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, image_file_input_selector))).send_keys(image_path)
    driver.find_element(By.ID, "Prompt").send_keys(prompt)  # Prompt if any
    motion_strength_input_xpath = (
        '//*[@id="root"]/div/div/div[2]/div/main/div[1]/div/div[1]/form/div/div[5]/div[2]/div/div/div/div/div[1]/div/div[2]/input'
    )
    driver.find_element(By.XPATH, motion_strength_input_xpath).send_keys(motion_strength)
    seed_button_selector = (
        '//*[@id="root"]/div/div/div[2]/div/main/div[1]/div/div[1]/form/div/div[6]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/input'
    )
    driver.find_element(By.XPATH, seed_button_selector).send_keys(seed)
    quality_button = driver.find_element(By.ID, "Quality")
    if quality_button.get_property("aria-checked") == "false":
        if hd:
            quality_button.click()  # HD enabled
    else:
        if not hd:
            quality_button.click()  # HD disabled

    submit_button_selector = 'button[type="submit"]'
    driver.find_element(By.CSS_SELECTOR, submit_button_selector).click()
