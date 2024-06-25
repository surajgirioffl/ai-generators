"""Module to handle all the operations related to pixverse.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 9th May 2024
Last-modified: 26th June 2024
Error-series: 1200
"""

import logging
import os
from time import sleep
from typing import Any
from datetime import datetime
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, Edge
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

URL = "https://app.pixverse.ai/login"


def login_with_google(driver: Chrome | Edge | Any) -> None:
    """Function to login using Google authentication.

    Args:
        driver (Chrome | Edge | Any): The driver to interact with the browser.

    Returns:
        None
    """
    logging.info("Login with Google...")
    driver.get(URL)
    wait = WebDriverWait(driver, 20)
    # Click on the button 'login with Google' when it appears
    login_with_google_selector = ".ant-btn-default.w-full.border-none"  # This selector will return two buttons. Select 1st one for Google.
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, login_with_google_selector))).click()
    logging.info("Login with Google Button clicked...")
    logging.info("waiting until url changes to /home route.")
    WebDriverWait(driver, 60).until(expected_conditions.url_contains("app.pixverse.ai/home"))
    logging.info("Login successful...")


def download_video(link: str, path: str, filename: str = None) -> str:
    """Download a video from the given link and save it to the specified path with an optional filename.

    Args:
        link (str): The URL of the video to download.
        path (str): The directory path where the video will be saved.
        filename (str, optional): The name of the file to save the video as. If not provided, a default filename will be generated.

    Returns:
        str: The absolute path of the saved file.
    """
    if not filename:
        filename = datetime.now().strftime("pixverse_%Y%m%d%H%M%S.mp4")
    response = requests.get(link)
    with open(os.path.join(path, filename), "wb") as file:
        file.write(response.content)
        created_filename = file.name
    return os.path.abspath(created_filename)


def fetch_generated_video_link(driver: Chrome | Edge | Any) -> str | bool:
    """Function to fetch the public link of the generated video.

    Args:
        driver (Chrome | Edge | Any): The web driver to use for interacting with the webpage.

    Returns:
        str | bool: The public link of the generated video or False if the video is not generated.
    """

    """
    Download last generated video
    - document.querySelectorAll(".text-white.text-base.text-center")
    - Above div is available only when video is generating (not before and not after generating)
    - document.getElementsByClassName("media-card") will return all generated video including the last one (but in random order.)
    - Don't use div.media-card to fetch all videos because for different screen sizes, classes/elements are changing.
    - Implement another logic which is:
        - Click on the video generating div, it will open the video before it's generated and fetch the link.
        - Come back to video generation page because this page will updated when video generated but not that one.
        - Use below for reference:
        - # https://app.pixverse.ai/create/video?detail=show&id=273428895983744
        - # document.querySelectorAll('svg[data-icon="arrow-left"]')[0].parentElement.click()
    
    - It will open as full screen (Means only that video and it's contents will visible on the screen).
    - Now use, video_element = document.getElementsByTagName("video")[0] - 0 because tag name returns node list. by the way, the page contains only one video element.
    - OR
    - Now use, video_element = document.querySelector("video")
    - fetch video_element.src, this src is public.
    - Use requests lib and download the video.
    """
    # First waiting and checking if the div specifying the video generation is present or not.
    wait = WebDriverWait(driver, 3)

    for _ in range(3):
        try:
            video_generation_info_div = wait.until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".text-white.text-base.text-center"))
            )
        except TimeoutException:
            # Div is not present means button is clicked.
            logging.info("Div specifying the video generation is not present. Clicking the submit button again...")
            submit_button_selector = 'button[type="submit"]'
            wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, submit_button_selector))).click()
        else:
            # if no exception
            # Div is present.
            video_generation_info_div.click()
            sleep(5)
            generated_video_link = driver.current_url

            # Now going back to the 'create-video' page
            # driver.find_element(By.CSS_SELECTOR, 'svg[data-icon="arrow-left"]').parent.click()
            arrow_left_svg = driver.find_element(By.CSS_SELECTOR, 'svg[data-icon="arrow-left"]')
            arrow_left_svg_parent = arrow_left_svg.find_element(By.XPATH, "./..")
            arrow_left_svg_parent.click()
            break

    # Now, wait until the message div will removed from the DOM because when video will be generated then this div will no longer attached to the DOM.
    wait_300 = WebDriverWait(driver, 600)  # Video generation takes time.
    try:
        wait_300.until_not(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".text-white.text-base.text-center")))
    except TimeoutException:
        print("Video generating taking too much time (10 min+). Error Code: 1202")
        logging.log("Video generating taking too much time (10 min+). Error Code: 1202")
        return False

    # at this point, the video has been generated and the div is removed from the DOM.
    driver.get(generated_video_link)

    WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.TAG_NAME, "video")))
    generated_video_public_link = driver.find_element(By.TAG_NAME, "video").get_attribute("src")
    driver.get(URL.strip("login"))  # Returning to the dashboard
    return generated_video_public_link


def create_video_from_prompt(driver: Chrome | Edge | Any, prompt: str, seed: int | str, *args, **kwargs):
    """Creates a video based on a given prompt using the provided driver.

    Args:
        driver (Chrome | Edge | Any): The web driver to use for interacting with the webpage.
        prompt (str): The prompt to base the video on.
        seed (int | str): The seed value to use for generating the video.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    logging.info("Creating video with the given prompt.")
    if not prompt:
        logging.error("Please provide a prompt. Error Code: 1203")
        logging.error("Prompt is required parameter. If it is missing, this error (1203) will be raised.")
        raise ValueError("Please provide a valid prompt. Error Code: 1203")

    if "app.pixverse.ai/create/video/text" not in driver.current_url:
        logging.info("Navigating to app.pixverse.ai/create/video/text")
        driver.get("https://app.pixverse.ai/create/video/text")

    wait = WebDriverWait(driver, 20)

    # Click on the 'create video' button when it appears
    text_to_video_button_selector = ".flex.flex-col.gap-1"
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, text_to_video_button_selector))).click()

    WebDriverWait(driver, 60).until(expected_conditions.visibility_of_element_located((By.ID, "Prompt")))
    driver.find_element(By.ID, "Prompt").send_keys(prompt)  # Prompt
    seed_button_selector = 'input[role="spinbutton"]'
    driver.find_element(By.CSS_SELECTOR, seed_button_selector).send_keys(seed)
    submit_button_selector = 'button[type="submit"]'
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, submit_button_selector)))
    driver.find_element(By.CSS_SELECTOR, submit_button_selector).click()


def create_video_from_images(
    driver: Chrome | Edge | Any,
    image: str,
    motion_strength: float | int | str,
    seed: int | str,
    prompt: str = "",
    hd_quality=False,
    *args,
    **kwargs,
):
    """Function to create video using image.

    Args:
        driver (Chrome | Edge | Any): the driver to use for the operation
        image (str): the path to the images to create the video from
        motion_strength (float | int | str): the strength of the motion for the video
        seed: int | str - the seed value for the video creation
        prompt (str): optional prompt for the video creation
        hd_quality (bool): whether to enable HD quality for the video
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Result:
        None
    """

    def wait_until_image_uploaded() -> bool:
        """
        A function that waits until a specific image is uploaded on the webpage and returns True if successful, False otherwise.
        No parameters are passed to this function and it returns a boolean value.
        """
        try:
            wait.until(
                expected_conditions.text_to_be_present_in_element_attribute((By.TAG_NAME, "img"), "src", "https://media.pixverse.ai/upload")
            )
        except TimeoutException:
            logging.error("Image not uploaded. Time out. Error Code: 1201")
            return False
        else:
            return True

    logging.info("Creating video with the given image.")

    if not image:
        logging.error("Please provide a Image. Error Code: 1204")
        logging.error("Image is a required parameter. If it is missing, this error (1204) will be raised.")
        raise ValueError("Please provide a valid image path. Error Code: 1204")

    if "app.pixverse.ai/create/video/image" not in driver.current_url:
        logging.info("Navigating to app.pixverse.ai/create/video/image")
        driver.get("https://app.pixverse.ai/create/video/image")

    wait = WebDriverWait(driver, 20)

    # Click on the 'create video' button when it appears
    image_2_video_button_selector = ".flex.flex-col.gap-1"
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, image_2_video_button_selector)))
    driver.find_elements(By.CSS_SELECTOR, image_2_video_button_selector)[1].click()

    # Image upload button
    # image_upload_button_selector = ".ant-btn.css-1ntsptu.ant-btn-text.ant-btn-sm"
    image_file_input_selector = 'input[type="file"]'
    wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, image_file_input_selector))).send_keys(image)
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
        if hd_quality:
            quality_button.click()  # HD enabled
    else:
        if not hd_quality:
            quality_button.click()  # HD disabled

    # Waiting for image to be uploaded
    if not wait_until_image_uploaded():
        return False

    submit_button_selector = 'button[type="submit"]'
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, submit_button_selector)))
    driver.find_element(By.CSS_SELECTOR, submit_button_selector).click()
