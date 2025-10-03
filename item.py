"""Module containing Item class"""


class Item:
    """Class representing an item in the game."""

    def __init__(self, name, description):
        """
        Initialize an Item object.

        Args:
            name (str): The name of the item.
            description (str): The description of the item.
        """
        self.name = name
        self.description = description

    def get_name(self):
        """Return the item's name."""
        return self.name

    def set_name(self, name):
        """Set the item's name."""
        self.name = name

    def get_description(self):
        """Return the item's description."""
        return self.description

    def set_description(self, description):
        """Set the item's description."""
        self.description = description

    def describe(self):
        """Print a sentence declaring the item's name and description."""
        print(f"This is a {self.name}. {self.description}")

    def pickup(self):
        """Print a sentence declaring the item has been picked up."""
        print(f"You have picked up the {self.get_name()}. {self.description}")

    def obtain(self):
        """Print a sentence declaring the item has been obtained."""
        print(f"You have obtained the {self.get_name()}. {self.description}")
