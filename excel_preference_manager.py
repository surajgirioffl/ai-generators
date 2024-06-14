"""Module to handle all operations related to the Preferences provided via the Excel file.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 8th June 2024
Last-modified: 9th June 2024
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

    def fetch_categories_and_sites(self) -> tuple[list, dict]:
        """
        Fetches unique categories and sites belongs to each unique category from the options dataframe.

        Returns:
            list: A list of unique categories.
            dict: A dictionary mapping categories to a list of sites.

        Examples:
            categories: ['text_to_video', 'image_to_video', 'text_to_image', 'text_to_text']
            categories_sites_mapping: {'text_to_video': ['pixverse', 'haiper'], 'image_to_video': ['pixverse', 'haiper'], 'text_to_image': ['ideogram', 'pixlr'], 'text_to_text': ['wordhero']
        """
        categories_sites_mapping: dict = {}

        categories: list = self.options_df["category"].drop_duplicates().to_list()

        for category in categories:
            sites: list = self.options_df.loc[self.options_df["category"] == category, "site"].to_list()
            categories_sites_mapping[category] = sites

        return categories, categories_sites_mapping

    def fetch_prompts(self) -> list[str]:
        """
        Fetches the prompts from the prompts_df DataFrame and returns them as a list of strings.

        Returns:
            list[str]: A list of prompt strings.
        """
        return self.prompts_df["prompt"].to_list()

    def fetch_sites_preferences(self) -> dict[dict]:
        """
        Fetches the sites preferences along with site metadata from the options dataframe and organizes them into a list of dictionaries.

        Returns:
            dict[dict]: A list of dictionaries containing site preferences.

        Example:
            site_options: {category1: {site1: {site1_options}, site2: {site2_options}}, category2: {site1: {site1_options}, site2: {site2_options}}, ...}
            1st site option: {'site': 'pixverse', 'category': 'image_to_video', 'automation_status': True, 'options': {'image': '', 'prompt': '', 'camera_motion': '', 'motion_strength': '', 'seed': '', 'hd_quality': 1.0}}
        """
        number_of_rows = len(self.options_df)
        sites_options: dict[dict] = {}

        # Iterating through each row of the dataframe
        for index in range(number_of_rows):
            site_dict: dict = {}  # Contains site specific key-values
            options_dict: dict = {}  # Contains site options key-values

            # Fetching the row as a dictionary of key-value pairs where keys are columns
            row_col_dict = self.options_df.iloc[index].to_dict()

            for key, value in row_col_dict.items():
                if "option" in key:
                    if value:
                        options_dict[value] = ""
                        last_key = value
                elif "value" in key:
                    if value:
                        options_dict[last_key] = value
                else:
                    site_dict[key] = value

            site_dict["options"] = options_dict

            try:
                sites_options[row_col_dict["category"]][site_dict["site"]] = site_dict
            except KeyError:
                # If the category is not present in the dictionary
                sites_options[row_col_dict["category"]] = {site_dict["site"]: site_dict}
        return sites_options

    @staticmethod
    def fetch_excel_sheet_names(excel_file_path: str = "preferences.xlsx"):
        """
        A static method to fetch the names of all the sheets in an Excel file.

        Parameters:
            excel_file_path (str): Path to the Excel file. Defaults to "preferences.xlsx".

        Returns:
            list: A list of sheet names in the Excel file.
        """
        excel_file = pd.ExcelFile(excel_file_path)
        return excel_file.sheet_names  # list of all sheet names

    @staticmethod
    def fetch_all_prompts(sheet_name: str, excel_file_path: str = "preferences.xlsx", column_name: str = "prompt"):
        """
        A function to fetch all prompts from a sheet of an Excel file.

        Parameters:
            sheet_name (str): The name of the sheet in the Excel file.
            excel_file_path (str): The path to the Excel file (default is "preferences.xlsx").
            column_name (str): The name of the column containing prompts (default is "prompt").

        Returns:
            list: A list of prompts extracted from the specified column.
        """
        prompt_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        prompt_df = prompt_df.map(lambda value: "" if pd.isna(value) else value)
        return prompt_df[column_name].to_list()

    @staticmethod
    def fetch_all_images(sheet_name: str, excel_file_path: str = "preferences.xlsx", column_name: str = "image"):
        """
        A static method to fetch all image path (images) from a specified Excel sheet.

        Args:
            sheet_name (str): The name of the sheet in the Excel file.
            excel_file_path (str): The path to the Excel file. Default is "preferences.xlsx".
            column_name (str): The name of the column containing the image URLs. Default is "image".

        Returns:
            list: A list of image Paths from the specified column.
        """
        image_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        image_df = image_df.map(lambda value: "" if pd.isna(value) else value)
        return image_df[column_name].to_list()


if __name__ == "__main__":
    preferences = PreferenceManager()
    print(preferences.fetch_prompts())
    print()
    print(preferences.fetch_sites_preferences())
    print()
    print(preferences.fetch_categories_and_sites())
