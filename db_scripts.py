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
        self.session.add(Prompts(prompt=prompt))
        self.session.commit()
        return self.session.query(Prompts.id).where(Prompts.prompt == prompt).all()[0][0]

    def insert_image(self, image: str) -> int:
        """Insert an image (image_path) into the database.

        Args:
            image (str): The image path to be inserted into the database.

        Returns:
            int: The ID of the inserted image (image_path).
        """
        self.session.add(Images(image=image))
        self.session.commit()
        return self.session.query(Images.id).where(Images.image == image).all()[0][0]

    def insert_output(self, file_path: str, category: str, site_id: str, prompt_id: str = None, image_id: str = None):
        """Insert the output into the database.

        Parameters:
            file_path (str): The path to the output file.
            category (str): The category of the site.
            site_id (str): The ID of the site.
            prompt_id (str, optional): The ID of the prompt (default is None).
            image_id (str, optional): The ID of the image (default is None).
        """
        self.session.add(Output(file_path=file_path, category=category, site_id=site_id, prompt_id=prompt_id, image_id=image_id))
        self.session.commit()


if __name__ == "__main__":
    db = AIGeneratorDB()
    print(db.insert_prompt("suraj"))
