"""Module to perform database operations associated with the application.

You can import this module to perform database operations for any site.
Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 17th June 2024
Last-modified: 17th June 2024
"""

from models import Sites, Prompts, Images, Output, get_new_session


class AIGeneratorDB:
    def __init__(self) -> None:
        """Initialize the object with a new session.
        No parameters.
        Returns None.
        """
        self.session = get_new_session()

    def __del__(self) -> None:
        self.session.close()

    def get_site_id(self, site: str) -> int:
        """Get the site ID for a given site name.

        Args:
            site (str): The name of the site.

        Returns:
            int: The site ID.
        """
        return self.session.query(Sites.id).where(Sites.site == site).one()[0]

    def insert_prompt(self, prompt: str) -> int:
        """Insert a prompt into the database.

        Args:
            prompt (str): The prompt to be inserted into the database.

        Returns:
            int: The ID of the inserted prompt.
        """
        row = Prompts(prompt=prompt)
        self.session.add(row)
        self.session.commit()
        return row.id

    def insert_image(self, image: str) -> int:
        """Insert an image (image_path) into the database.

        Args:
            image (str): The image path to be inserted into the database.

        Returns:
            int: The ID of the inserted image (image_path).
        """
        row = Images(image=image)
        self.session.add(row)
        self.session.commit()
        return row.id

    def insert_output(self, file_path: str | list, category: str, site_id: str, prompt_id: str = None, image_id: str = None):
        """Insert the output into the database.

        Parameters:
            file_path (str | list): The path to the output file or list of path to output files (if more than one output files).
            category (str): The category of the site.
            site_id (str): The ID of the site.
            prompt_id (str, optional): The ID of the prompt (default is None).
            image_id (str, optional): The ID of the image (default is None).
        """
        if isinstance(file_path, str):
            self.session.add(Output(file_path=file_path, category=category, site_id=site_id, prompt_id=prompt_id, image_id=image_id))
        else:
            for path in file_path:
                self.session.add(Output(file_path=path, category=category, site_id=site_id, prompt_id=prompt_id, image_id=image_id))
        self.session.commit()
