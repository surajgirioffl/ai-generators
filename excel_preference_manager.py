"""Module to handle all operations related to the Preferences provided via the Excel file.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 8th June 2024
Last-modified: 8th June 2024
Error-series: 2100
"""

import pandas as pd


class PreferenceManager:
    """Class to handle all operations related to the Preferences provided via the Excel file."""

    def __init__(
        self, excel_file_path: str = "preferences.xlsx", options_sheet_name: str = "options", prompts_sheet_name: str = "prompts"
    ) -> None:
        """
        Initialize the preferences manager with the given Excel file path and sheet names.

        Parameters:
            excel_file_path (str): The file path to the Excel file containing preferences data. Default is "preferences.xlsx".
            options_sheet_name (str): The sheet name in the Excel file containing options data.
            prompts_sheet_name (str): The sheet name in the Excel file containing prompts data.

        Returns:
            None
        """
        try:
            options_df = pd.read_excel(excel_file_path, sheet_name=options_sheet_name)
            prompts_df = pd.read_excel(excel_file_path, sheet_name=prompts_sheet_name)
        except Exception as e:
            raise e.__class__(f"Error in extracting preferences. Error code: 2101. Exception: {e}")
        else:
            # NaN will of float type if we convert it to python object
            # Replacing NaN with '' (empty string)
            self.options_df: pd.DataFrame = options_df.map(lambda value: "" if pd.isna(value) else value)
            self.prompts_df: pd.DataFrame = prompts_df.map(lambda value: "" if pd.isna(value) else value)
