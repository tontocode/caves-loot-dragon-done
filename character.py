"""Module containing the Character, Person, and Enemy classes."""

def death_screen():
    """Display the death screen message."""
    print("***")
    print("YOU HAVE DIED")
    print("***")


class Character:
    """Base class for all characters in the game."""

    def __init__(self, name: str, description: str):
        """
        Initialize a Character object.

        Args:
            name (str): Character's name.
            description (str): Character's description.
        """
        self.name = name
        self.description = description
        self.conversation = None

    def set_conversation(self, conversation: str):
        """
        Set the character's conversation string.

        Args:
            conversation (str): Conversation text.
        """
        self.conversation = conversation

    def describe(self):
        """Print the character's presence and description."""
        print(f"{self.name} is here.")
        print(self.description)

    def talk(self):
        """Print the character's conversation or a default message."""
        if self.conversation is not None:
            print(f"{self.name}: {self.conversation}")
        else:
            print(f"{self.name} does not want to talk to you.")

    def get_name(self):
        """Return the character's name."""
        return self.name


class Person(Character):
    """Class for non-enemy people in the game."""

    def __init__(
        self, *, name: str, description: str, conversations: dict, quest_items: list
    ):
        """
        Initialize a Person object.

        Args:
            name (str): Person's name.
            description (str): Description of the person.
            conversations (dict): Conversation states.
                (strings pre_gift, grateful, ungrateful, post_gift as keys)
            quest_items (list): The item the person wants, the item given in exchange.
        """
        super().__init__(name, description)
        self.conversation_dict = conversations
        self.conversation = conversations["pre_gift"]
        self.gift_item = quest_items[0]
        self.reward_item = quest_items[1]
        self.affinity = 0

    def give(self, item_name: str):
        """
        Give an item to the person and update conversation/affinity.

        Args:
            item_name (str): Name of the item to give.
        Returns:
            reward item or None
        """
        if item_name == self.gift_item.get_name():
            self.set_conversation(self.conversation_dict["grateful"])
            self.talk()
            self.affinity += 1
            self.set_conversation(self.conversation_dict["post_gift"])
            return self.reward_item
        self.set_conversation(self.conversation_dict["ungrateful"])
        self.talk()
        self.affinity -= 1
        self.set_conversation(self.conversation_dict["pre_gift"])
        return None

    def fight(self, combat_item: str):
        """
        Print a message when the player tries to fight a person.

        Args:
            combat_item (str): Name of item used to fight.
        Returns:
            bool: True always (for game logic).
        """
        print(f"Ouch! Don't fight me! Put that {combat_item} away!")
        return True


class Enemy(Character):
    """Class for enemy characters in the game."""

    def __init__(self, name: str, description: str, weakness, drop):
        """
        Initialize an Enemy object.

        Args:
            name (str): Enemy's name.
            description (str): Description of the enemy.
            weakness (str): Name of the item that defeats the enemy.
            drop (Item): Item dropped by the enemy when defeated.
        """
        super().__init__(name, description)
        self.weakness = weakness
        self.is_enemy = True
        self.drop = drop

    def get_weakness(self):
        """Return the enemy's weakness item name."""
        return self.weakness

    def fight(self, combat_item: str):
        """
        Fight the enemy using a combat item.

        Args:
            combat_item (str): Name of item used to fight.
        Returns:
            Item or bool: Item if defeated, False if player dies.
        """
        if combat_item.lower() == self.weakness:
            print(f"You fend {self.name} off with the {combat_item}.")
            if self.drop:
                print(f"You have obtained {self.drop.get_name()}!")
            return self.drop
        print(f"{self.name} swallows you, little wimp.")
        death_screen()
        return False

    def give(self, give_item_name: str):
        """
        Attempt to give an item to an enemy (results in death).

        Args:
            give_item (str): Item to give.
        Returns:
            bool: False (player dies).
        """
        print(
            f"{self.name} reacts aggressively and attacks you. Unprepared, you cannot fight back."
            f"Your {give_item_name} is destroyed."
        )
        print(f"{self.name} swallows you, little wimp.")
        death_screen()
        return False


class Boss(Enemy):
    """Class for the boss enemy (dragon)."""

    def __init__(self, name, description, weakness: list[str], drop=None):
        """
        Initialize a Boss object.

        Args:
            name (str): Boss's name.
            description (str): Description of the boss.
            weaknesses (list of strings): Item names that defeat the boss.
        """
        super().__init__(name, description, weakness, drop)
        self.weakness.sort()
        self.is_boss = True

    def fight(self, combat_item: list[str]):
        """
        Fight the boss using a combat item.

        Args:
            combat_items (list): Names of items used to fight.
        Returns:
            bool: True if defeated, False if player dies.
        """
        combat_item.sort()
        print()
        if combat_item == self.weakness:
            print(
                "After a long and arduous battle,\n"
                "wherein you narrowly escaped death multiple times,\n"
                "you have finally defeated the dragon!\n"
                "You have liberated the caves from its tyranny!\n\n"
                "The cavespeople are eternally grateful!\n"
                "They throw you an extravagant feast, featuring a suspiciously slimey dish\n"
                "and a cake that could well have been baked in a forge,\n"
                "among a spread of mouth-watering dishes!"
            )
            print()
            print("YOU WIN!")
            return True
        print(
            f"After a long and arduous battle,\n"
            f"you have been defeated by {self.name}.\n"
            "You feel a cold sensation as you realize that this is the end.\n"
            "Your vision fades to black as you succumb to your wounds.\n"
            "You have failed to liberate the caves from its tyranny.\n"
            "The cavespeople mourn your loss.\n"
            "They hold a somber ceremony in your honor,\n"
            "and erect a statue in the town square to commemorate your bravery."
        )
        print()
        death_screen()
        return False
