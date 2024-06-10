"""GUI module to provide Graphical User Interface for the application.

GUI module to provide Graphical User Interface for the application.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 09th June 2024
Last-modified: 10th June 2024
Error-series: 2300
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

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
        generation_category_dropdown = toga.Selection(
            items=[category.replace("_", " ").title() for category in self.categories], style=dropdown_style
        )

        # 3. Sites dropdown widget
        sites_label = toga.Label(text="Select AI Generation Category", style=normal_label_style)
        # 3.1 Generation Category dropdown
        sites_dropdown = toga.Selection(items=[], style=dropdown_style)

        # 4. Prompt dropdown widget
        prompts_label = toga.Label(text="Select AI Generation Category", style=normal_label_style)
        # 4.1 Generation Category dropdown
        prompts_dropdown = toga.Selection(items=[], style=dropdown_style)

        # 5. Submit Button widget
        button_style = Pack(width=100, padding_top=30, padding_bottom=30, padding_left=30, padding_right=30)
        submit_button = toga.Button(text="Submit", style=button_style)
        ### Widgets_End ###

        # Creating a box to hold the widgets. We can create as many to create layout.
        style = Pack(direction=COLUMN, padding=10, width=600, alignment="center")
        self.box = toga.Box(style=style)

        # Adding widgets to the box
        self.box.add(box_heading)
        self.box.add(generation_category_label)
        self.box.add(generation_category_dropdown)
        self.box.add(sites_label, sites_dropdown, prompts_label, prompts_dropdown)
        self.box.add(submit_button)

        # Adding the box as the content of the main window
        self.main_window.content = self.box

        # Displaying the main window
        self.main_window.show()

    def set_attributes(self, categories: list, categories_sites_mapping: dict, sites_preferences: dict, prompts: list, driver=None):
        self.categories: list = categories
        self.categories_sites_mapping: dict = categories_sites_mapping
        self.sites_preferences: dict = sites_preferences
        self.prompts: list = prompts
        self.driver = driver


def main(
    categories: list,
    categories_sites_mapping: dict,
    sites_preferences: dict,
    prompts: list,
    driver=None,
    app_name: str = "AI Generator",
    app_id: str = "org.surajgirioffl.ai_generator",
    icon_path: str | None = None,
    home_page: str = "https://github.com/surajgirioffl/ai-generators",
    *args,
    **kwargs
) -> None:
    """
    A function that handles the main logic of the program.
    It presents categories, sites and prompts option to the user and when choice is made then generate content accordingly.
    It then dynamically imports and executes modules based on the selected category to generate AI content.

    Parameters:
        categories (list): A list of available categories.
        categories_sites_mapping (dict): A dictionary mapping categories to sites.
        sites_preferences (dict): A dictionary containing preferences for each site.
        prompts (list): A list of available prompts.
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
    app.set_attributes(categories, categories_sites_mapping, sites_preferences, prompts, driver)
    app.main_loop()


if __name__ == "__main__":
    main([], {}, {}, [])
