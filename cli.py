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
