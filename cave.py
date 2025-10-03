"""Module containing Cave class."""

class Cave:
    """Class representing a cave in the adventure game."""

    def __init__(self, name):
        """
        Initialize a Cave object.

        Args:
            name (str): The name of the cave.
        """
        self.name = name
        self.description = None
        self.linked_caves = {}
        self.character = None
        self.item = None

    def get_name(self):
        """
        Get the cave's name.

        Returns:
            str: The name of the cave.
        """
        return self.name

    def set_name(self, name):
        """
        Set the cave's name.

        Args:
            name (str): The new name of the cave.
        """
        self.name = name

    def get_description(self):
        """
        Get the cave's description.

        Returns:
            str: The cave's description.
        """
        return self.description

    def set_description(self, description):
        """
        Set the cave's description.

        Args:
            description (str): The description of the cave.
        """
        self.description = description

    def get_character(self):
        """
        Get the character in the cave.

        Returns:
            object: The character object, or None if no character is present.
        """
        return self.character

    def set_character(self, character):
        """
        Place a character in the cave.

        Args:
            character (object): The character object to place in the cave.
        """
        self.character = character

    def remove_character(self):
        """
        Remove the character from the cave.
        """
        self.character = None

    def get_item(self):
        """
        Get the item in the cave.

        Returns:
            object: The item object, or None if no item is present.
        """
        return self.item

    def set_item(self, item):
        """
        Place an item in the cave.

        Args:
            item (object): The item object to place in the cave.
        """
        self.item = item

    def remove_item(self):
        """
        Remove the item from the cave.
        """
        self.item = None

    def link_cave(self, cave, direction):
        """
        Link another cave to this cave in a given direction.

        Args:
            cave (Cave): The cave object to link.
            direction (str): The direction (e.g., 'north', 'south') of the linked cave.
        """
        self.linked_caves[direction] = cave

    def get_details(self):
        """
        Print details of the cave, including description, linked caves,
        and any character or item present.
        """
        print(f"The {self.name}")
        print(self.description)
        for direction, cave in self.linked_caves.items():
            print(f"The {cave.get_name()} is {direction}.")
        print()
        if self.character:
            self.character.describe()
            print()
        if self.item:
            self.item.describe()
            print()

    def move(self, direction):
        """
        Move to the cave in the specified direction if possible.

        Args:
            direction (str): The direction to move.

        Returns:
            Cave: The cave object in the specified direction,
                  or the current cave if movement is not possible.
        """
        if direction in self.linked_caves:
            print(f"You have moved to the {self.linked_caves[direction].get_name()}")
            return self.linked_caves[direction]
        print("You can't go that way.")
        print(f"You are still in the {self.get_name()}.")
        return self
