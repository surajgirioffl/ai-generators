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
