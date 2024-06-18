"""GUI module to provide Graphical User Interface for the application.

GUI module to provide Graphical User Interface for the application.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 09th June 2024
Last-modified: 17th June 2024
Error-series: 2300
"""

import os
import logging
import importlib
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from excel_preference_manager import PreferenceManager

__author__ = "Suraj Kumar Giri"
__version__ = "0.0.0"
__application_name__ = "AI GENERATOR"
__description__ = "A browser automation project that uses various AI generation sites to generate videos, images, and text with various options and customizations."


class AIGenerator(toga.App):
    def startup(self) -> None:
        # Creating main window
        self.main_window = toga.MainWindow(title=self.formal_name, size=(600, 600))

        ### Widgets_Start ###
        # 1. Creating initial widgets
        heading_style = Pack(color="black", text_align="center", font_size=30, font_weight="bold", width=600)
        box_heading = toga.Label(text=__application_name__, style=heading_style)

        # 2. Generation Category widget
        normal_label_style = Pack(color="black", font_size=15, font_weight="bold", text_align="center", padding_top=30)
        generation_category_label = toga.Label(text="Select AI Generation Category", style=normal_label_style)
        # 2.1 Generation Category dropdown
        dropdown_style = Pack(font_size=15, font_weight="bold", text_align="center", padding_top=5, padding_left=50, padding_right=50)
        categories = [category.replace("_", " ").title() for category in self.categories]
        categories.insert(0, "")  # Inserting an empty prompt at the beginning
        self.generation_category_dropdown = toga.Selection(
            items=categories,
            style=dropdown_style,
            on_change=self.on_category_change,
        )

        # 3. Sites Checkbox widget
        sites_label = toga.Label(text="Select Sites", style=normal_label_style)
        # 3.1 Generation Category dropdown
        self.sites_checkbox_container = toga.ScrollContainer(
            horizontal=True,
            vertical=False,
            style=Pack(padding_left=50, padding_right=50, alignment="center", text_align="center", padding_bottom=-50),
        )
        self.sites_checkbox_container.content = toga.Label(
            "Select a category first",
            style=Pack(background_color="white", color="black", font_size=15, font_weight="bold", text_align="center", padding_top=10),
        )

        # 4. Prompt or image dropdown widget
        self.prompts_label = toga.Label(text="Select Excel Sheet", style=normal_label_style)
        # 4.1 Prompt/image sheet selection dropdown
        self.prompt_image_sheet_dropdown = toga.Selection(items=[""], style=dropdown_style)

        # 5. Submit Button widget
        button_style = Pack(
            width=100,
            padding_top=30,
            padding_bottom=30,
            padding_left=30,
            padding_right=30,
            font_size=15,
            font_weight="bold",
            color="green",
        )
        self.submit_button = toga.Button(text="Submit", style=button_style, on_press=self.on_submit)

        # Creating a box to hold the widgets. We can create as many to create layout.
        style = Pack(direction=COLUMN, padding=10, width=600, alignment="center")
        self.box = toga.Box(style=style)

        # Adding widgets to the box
        self.box.add(box_heading)
        self.box.add(generation_category_label)
        self.box.add(
            self.generation_category_dropdown,
            sites_label,
            self.sites_checkbox_container,
            self.prompts_label,
            self.prompt_image_sheet_dropdown,
        )
        self.box.add(self.submit_button)

        # Adding the box as the content of the main window
        self.main_window.content = self.box

        # Displaying the main window
        self.main_window.show()

    def on_category_change(self, widget):
        """
        A function that handles the event when the category selection changes.

        Parameters:
            widget: the widget object triggering the event

        Returns:
            None
        """
        selected_category = widget.value.lower().replace(" ", "_")

        # For sites
        sites: list | None = self.categories_sites_mapping.get(selected_category)
        if sites:
            self.sites_checkbox_container.content = None  # Clearing the previous content
            sites = [site.title() for site in sites]

            switch_style = Pack(font_size=15, font_weight="bold", padding=10)
            self.switches = []
            switches_container = toga.Box(style=Pack(direction=ROW))
            for site in sites:
                switch = toga.Switch(site, style=switch_style)
                switches_container.add(switch)
                self.switches.append(switch)

            # Adding the switches to the container
            self.sites_checkbox_container.content = switches_container
            if len(sites) < 5:
                # Scrollbar will not appear in this case. So, decreasing the padding bottom to reduce the space and make it look good.
                self.sites_checkbox_container.style.padding_bottom = -50
            else:
                # Scrollbar will appear in this case.
                self.sites_checkbox_container.style.padding_bottom = 0
        else:
            # No sites found for the selected category
            self.sites_checkbox_container.content = toga.Label(
                "No sites found for the selected category",
                style=Pack(background_color="white", color="black", font_size=15, font_weight="bold", text_align="center", padding_top=10),
            )
            self.sites_checkbox_container.style.padding_bottom = -50

        # For Prompts (or Images in case of image_to_video category)
        if selected_category:
            excel_sheets = PreferenceManager.fetch_excel_sheet_names()
            if selected_category == "image_to_video":
                self.prompts_label.text = "Select Excel Sheet For Images"
                self.prompt_image_sheet_dropdown.items = [sheet for sheet in excel_sheets if sheet.startswith("image")]
            else:
                self.prompts_label.text = "Select Excel Sheet For Prompts"
                self.prompt_image_sheet_dropdown.items = [sheet for sheet in excel_sheets if sheet.startswith("prompt")]
        else:
            self.prompts_label.text = "Select Excel Sheet"
            self.prompt_image_sheet_dropdown.items = [""]

    def on_submit(self, widget):
        """
        A method that handles the submit event for the submit button.

        Parameters:
            widget: The widget triggering the submit event.

        Returns:
            None
        """
        # Checking if any category is not selected.
        if not self.generation_category_dropdown.value:
            self.main_window.error_dialog("Error", "Please select a category")
            return

        # Checking for the selected sites.
        selected_sites = [switch.text.lower() for switch in self.switches if switch.value]
        if not selected_sites:
            self.main_window.error_dialog("Error", "Please select a site")
            return

        # Checking for selected sheets for image/prompt.
        if not self.prompt_image_sheet_dropdown.value:
            message = (
                "Please select an Excel sheet for images"
                if self.generation_category_dropdown.value == "image_to_video"
                else "Please select an Excel sheet for prompt"
            )
            self.main_window.error_dialog("Error", message)

        # Fetching selected values
        selected_category = self.generation_category_dropdown.value.lower().replace(" ", "_")
        selected_sites = selected_sites  # Just for readability
        selected_sheet = self.prompt_image_sheet_dropdown.value

        # Started performing operations based on selected values
        self.submit_button.enabled = False  # Disabling the submit button until content is generated

        # Performing AI generation
        self.perform_ai_generation_operation(selected_category, selected_sites, selected_sheet)

        self.submit_button.enabled = True  # Enabling the submit button after content is generated

    def perform_ai_generation_operation(self, selected_category: str, selected_sites: str | list, selected_sheet: str):
        """
        A function to perform an AI generation operation with the given parameters.

        Parameters:
            self (obj): The instance of the class.
            selected_category (str): The selected category for the AI generation operation.
            selected_site (str): The selected site for the AI generation operation.
            selected_prompt (str): The prompt selected for the AI generation operation.

        Returns:
            None
        """
        # Updating prompts/images for the selected site
        for selected_site in selected_sites:
            if "prompt" in self.sites_preferences[selected_category][selected_site]["options"].keys():
                # BTW Above condition is not required. If prompt key doesn't exist then 'prompt' key will created and accepted by **kwargs of the function which accept this site options as args.
                prompts: list = PreferenceManager.fetch_all_prompts(selected_sheet)
                self.sites_preferences[selected_category][selected_site]["options"]["prompt"] = prompts
            elif "image" in self.sites_preferences[selected_category][selected_site]["options"].keys():
                images: list = PreferenceManager.fetch_all_prompts(selected_sheet)
                self.sites_preferences[selected_category][selected_site]["options"]["image"] = images

        category_package_name_mapping: dict[str, str] = {
            "text_to_video": "ai_video_generators",
            "image_to_video": "ai_video_generators",
            "text_to_image": "ai_image_generators",
            "text_to_text": "ai_content_generators",
        }

        for selected_site in selected_sites:
            os.chdir(os.path.dirname(__file__))
            logging.info("======================Starting a new AI Generation (With GUI Interface)=======================")
            logging.info(f"Category: {selected_category} | Site: {selected_site} | Sheet: {selected_sheet}")

            module = f"{category_package_name_mapping[selected_category]}.{selected_site}_ai.main"
            module = importlib.import_module(module)
            try:
                status: bool = module.main(
                    site_preferences=self.sites_preferences[selected_category][selected_site], driver=self.driver, *self.args, **self.kwargs
                )
            except Exception as e:
                status = False
                logging.exception(f"Exception: {e}. Error Code: 2301")
                self.main_window.error_dialog("Exception", str(e))

            if status:
                logging.info("======================AI Generation Completed | STATUS -> SUCCESS =======================")
                self.main_window.info_dialog("Success", f"AI Generation Completed Successfully For {selected_site}")
            else:
                logging.warning("======================AI Generation Failed | STATUS -> FAILED =======================")
                self.main_window.error_dialog("Failed", f"AI Generation Failed For {selected_site}")

        # Switching the CWD to root dir.
        os.chdir(os.path.dirname(__file__))

    def set_attributes(self, categories: list, categories_sites_mapping: dict, sites_preferences: dict, driver=None, *args, **kwargs):
        self.categories: list = categories
        self.categories_sites_mapping: dict = categories_sites_mapping
        self.sites_preferences: dict = sites_preferences
        self.driver = driver
        self.args = args
        self.kwargs = kwargs


def main(
    categories: list,
    categories_sites_mapping: dict,
    sites_preferences: dict,
    driver=None,
    app_name: str = "AI Generator",
    app_id: str = "org.surajgirioffl.ai_generator",
    icon_path: str | None = None,
    home_page: str = "https://github.com/surajgirioffl/ai-generators",
    *args,
    **kwargs,
) -> None:
    """
    A function that handles the main logic of the program.
    It presents categories, sites and prompts option to the user and when choice is made then generate content accordingly.
    It then dynamically imports and executes modules based on the selected category to generate AI content.

    Parameters:
        categories (list): A list of available categories.
        categories_sites_mapping (dict): A dictionary mapping categories to sites.
        sites_preferences (dict): A dictionary containing preferences for each site.
        driver (optional): An optional web driver object.
        app_name (str): The name of the application (application title that will visible to the user)
        app_id (str): The ID of the application. E.g: com.example.myapp
        icon_path (str | None, optional): Path to the icon file. Defaults to None.
        home_page (str, optional): The home page of the application. Defaults to "https://github.com/surajgirioffl/ai-generators".
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Literal[False] | None: False if the user selects to exit the program, otherwise None.
    """
    icon = None
    if icon_path:
        icon = toga.Icon(icon_path)

    app = AIGenerator(app_name, app_id, author=__author__, version=__version__, description=__description__, icon=icon, home_page=home_page)
    app.set_attributes(categories, categories_sites_mapping, sites_preferences, driver, *args, **kwargs)
    app.main_loop()


if __name__ == "__main__":
    main([], {}, {}, [])
