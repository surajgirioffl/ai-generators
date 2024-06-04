"""Module to handle all operations related to the Adobe Firefly.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 27th May 2024
Last-modified: 27th May 2024
Error-series: 1100
"""

import requests


class Firefly:
    def __init__(self) -> None:
        self.URL = "https://firefly-api.adobe.io/v2/images/generate"
        ...

    def generate_image(self, prompt: str) -> str:
        requests.get(self.URL)
        ...
