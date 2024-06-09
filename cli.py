"""CLI module to provide Command Line Interface for the application.

CLI module to provide Command Line Interface for the application.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 09th June 2024
Last-modified: 09th June 2024
Error-series: 2200
"""

import importlib
import sys
from typing import Literal
from os import system


def clear_screen():
    """
    A function to clear the screen based on the operating system.
    """
    if sys.platform == "win32":
        system("cls")
    else:
        system("clear")


def category_selector_menu(categories: list[str]) -> str | Literal[False]:
    """
    A function that displays a category selection menu based on the provided list of categories.
    Allows the user to select a category by inputting the corresponding index or perform other actions like clearing the screen or exiting the application.
    Returns the selected category as a string or False if the user chooses to exit.

    Parameters:
        categories (list[str]): A list of strings representing the available categories.

    Returns:
        str | Literal[False]: Returns the selected category on success or False if the user chooses to exit.
    """
    index_category_mapping = {}

    clear_screen()
    while True:
        print("===================CATEGORY SELECTION MENU (Main Menu)===================")
        for index, category in enumerate(categories):
            print(f"=> Press {index} to select category '{category.replace('_', ' ').title()}'")
            index_category_mapping[f"{index}"] = category
        print("=> Write '@' or 'clear' to clear the display")
        print("=> Write '#' or 'exit' to exit the application")

        choice = input("Write your choice: ")

        if choice in index_category_mapping.keys():
            return index_category_mapping[choice]
        elif choice in ["@", "clear"]:
            clear_screen()
            continue
        elif choice in ["#", "exit"]:
            return False
        else:
            print("Invalid choice. Write again...\n")
            continue


def site_selector_menu(sites: list[str], selected_category: str) -> str | Literal[False]:
    """
    A function that displays a site selection menu based on the provided list of sites.

    Parameters:
        sites (list[str]): A list of strings representing different site names.
        selected_category (str): A string representing the selected category (Shown in the title of the menu).

    Returns:
        str | Literal[False]: Returns the selected site on success or False to indicate exiting the menu.
    """
    index_site_mapping = {}

    print("\n")
    while True:
        print(f"===================SITE SELECTION MENU (CATEGORY: {selected_category.replace('_', ' ').title()})===================")
        for index, site in enumerate(sites):
            print(f"=> Press {index} to select site '{site.replace('_', ' ').title()}'")
            index_site_mapping[f"{index}"] = site

        print("=> Write '@' or 'clear' to clear the display")
        print("=> Write '#' or 'exit' to go back to main menu (Category selection menu)")

        choice = input("Write your choice: ")

        if choice in index_site_mapping.keys():
            return index_site_mapping[choice]
        elif choice in ["@", "clear"]:
            clear_screen()
            continue
        elif choice in ["#", "exit"]:
            return False
        else:
            print("Invalid choice. Write again...\n")
            continue


def prompt_selector_menu(prompts: list[str], selected_site: str) -> str | Literal[False]:
    """
    A function to display a prompt selection menu based on a list of prompts.

    Parameters:
        prompts (list[str]): a list of strings representing different prompts to choose from
        selected_site (str): a string representing the selected site

    Returns:
        str | Literal[False]: Returns the selected prompt on success else False.
    """
    index_prompt_mapping = {}

    print("\n")
    while True:
        print(f"===================PROMPT SELECTION MENU (Site: {selected_site.replace('_', ' ').title()})===================")
        print("=> Press 'enter' to skip the prompt (prompt not required)")
        print("=> Press 'w' to write your own prompt")
        print("=> Write '@' or 'clear' to clear the display")
        print("=> Write '#' or 'exit' to go back to Site Selection Menu")
        for index, prompt in enumerate(prompts):
            print(f"=> Press {index} for '{prompt.replace('_', ' ').title()}'")
            index_prompt_mapping[f"{index}"] = prompt

        choice = input("Write your choice: ")

        if choice in index_prompt_mapping.keys():
            return index_prompt_mapping[choice]
        elif choice in ["@", "clear"]:
            clear_screen()
            continue
        elif choice in ["#", "exit"]:
            return False
        elif choice == "w":
            return input("Write your prompt: ")
        elif choice == "":
            return ""
        else:
            print("Invalid choice. Write again...\n")
            continue
