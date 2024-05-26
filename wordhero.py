"""Module to handle all operations related to the WordHero.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 23rd May 2024
Last-modified: 26th May 2024
Error-series: 1200
"""

import logging
from typing import Any
from time import sleep
import inflect
from selenium.webdriver import Chrome, Edge
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        email_input_element = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        email_input_element.clear()  # Clearing before entering
        email_input_element.send_keys(email)  # Email input
        password_input_element = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        password_input_element.clear()  # Clearing before entering
        password_input_element.send_keys(password)  # Password input

        if stay_logged_in:
            stay_logged_in_checkbox = self.driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
            if not stay_logged_in_checkbox.get_property("checked"):
                stay_logged_in_checkbox.click()

        # Clicking on the log-in button
        self.driver.find_element(By.CSS_SELECTOR, "button").click()
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

    def fetch_all_blog_tools(self):
        """Fetch all blog tools on the current page and return them in a dictionary."""
        if "/home" not in self.driver.current_url:
            # If the current page is not home page.
            self.driver.get(self.URL + "home")

        # Wait until any element located
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.bubble-element.Text.cmaZqaO")))
        document_body = self.driver.find_element(By.TAG_NAME, "body")

        # Scrolling down. So, all hidden elements will appear.
        for _ in range(6):
            document_body.send_keys(Keys.PAGE_DOWN)
            sleep(0.5)

        document_body.send_keys(Keys.HOME)  # Going to Top of the page

        # Fetching all the blog tools
        tools = self.driver.find_elements(
            By.XPATH, "//div[contains(@class, 'bubble-element Text cmaZqaO') and contains(normalize-space(), 'Blog')]"
        )
        blog_tools = {}

        for tool in tools:
            if text := tool.get_property("innerText"):
                text = text.strip()
                print(text)
                blog_tools[text] = tool
        return blog_tools

    def generate_content_with_chat(self, prompt: str, new_chat: bool = True) -> dict:
        """A function to generate content with chat based on a prompt.

        Args:
            prompt (str): The prompt to generate content with.
            new_chat (bool, optional): Flag to indicate if a new chat should be started. Defaults to True.

        Returns:
            dict: A dictionary containing questions and their corresponding answers/responses.

        More:
            - Prompt must not contain any '\n' (new line) characters. Otherwise, the prompt will submitted without writing the complete prompt as passed.
            - \n will act as ENTER and it submits the prompt immediately without writing any character next to it.
        """

        def wait_until_response_generated() -> None:
            """A function that waits until a response is generated by checking the innerText of an element in a loop."""
            generation_info_div = self.driver.find_element(By.CLASS_NAME, "cmeat")
            while True:
                if generation_info_div.get_property("innerText").strip():
                    sleep(0.5)
                    # if innerText contain any value (AI is typing...). Means element is visible and response is generating.
                    continue
                else:
                    # innerText contain no value. (''). Means response has been generated.
                    return

        def wait_until_generation_info_div_is_visible() -> None:
            """A function waits until the generation information div is visible on the webpage. It continuously checks the innerText of the element and returns when it contains any value, indicating that the response is being generated."""
            generation_info_div = self.driver.find_element(By.CLASS_NAME, "cmeat")
            while True:
                if generation_info_div.get_property("innerText").strip():
                    # if innerText contain any value (AI is typing...). Means element is visible and response is generating.
                    return
                else:
                    # innerText contain no value. (''). Means response generation is not yet started.
                    sleep(0.2)
                    continue

        logging.info("Generating content with Chat...")
        logging.info("Checking if Chat page is open...")
        if "/chat" not in self.driver.current_url:
            # If the current page is not chat page.
            logging.info("Chat page is not open. Opening it...")
            self.driver.get(self.URL + "chat")

        logging.info("Chat page opened successfully...")

        if new_chat:
            # Clicking on new chat
            logging.info("Starting a new conversation...")
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'New Chat')]"))).click()
        else:
            logging.info("Skipping new chat. Continue with existing conversation of the chat page...")

        textarea = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "textarea")))
        logging.info("Writing prompt...")
        textarea.clear()
        textarea.send_keys(prompt)
        textarea.send_keys(Keys.ENTER)
        # self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cmeaUaQ"))).click()
        wait_until_generation_info_div_is_visible()  # Checking if generation info div appeared.
        logging.info("Prompt written successfully..")

        logging.info("Waiting for response...")
        # Wait until response is generated
        # Below div will visible until response is generated.
        # <div class="bubble-element Text cmeat bubble-r-vertical-center" style=""><div>AI is typing...</div></div>
        # wait = WebDriverWait(self.driver, 120)
        # wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "cmeat")))
        wait_until_response_generated()
        logging.info("Response generated successfully.")
        sleep(1)

        # Fetching response
        qa_div_xpath = "//div[contains(@id, 'current_cell_text_')]"  # Div containing questions and answers/responses
        qa_divs = self.driver.find_elements(By.XPATH, qa_div_xpath)

        # index 0 question - index 1 it's answer
        # index 2 question - index 3 it's answer
        # index 4 question - index 5 it's answer
        # And so on...

        prompt_response_dict = {}

        for index in range(0, len(qa_divs), 2):
            question = qa_divs[index].get_property("innerText")
            answer = qa_divs[index + 1].get_property("innerText")
            prompt_response_dict[question] = answer

        return prompt_response_dict
