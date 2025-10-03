"""Module containing the Character, Person, and Enemy classes."""

def death_screen():
    """Display the death screen message."""
    print("***")
    print("YOU HAVE DIED")
    print("***")

class Character:
    """Base class for all characters in the game."""

    def __init__(self, name, description):
        """
        Initialize a Character object.

        Args:
            name (str): Character's name.
            description (str): Character's description.
        """
        self.name = name
        self.description = description
        self.conversation = None

    def set_conversation(self, conversation):
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

    def __init__(self, *, name, description, conversations, quest_items):
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

    def give(self, item_name):
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

    def fight(self, combat_item):
        """
        Print a message when the player tries to fight a person.

        Args:
            combat_item (str): Item used to fight.
        Returns:
            bool: True always (for game logic).
        """
        print(f"Ouch! Don't fight me! Put that {combat_item} away!")
        return True


class Enemy(Character):
    """Class for enemy characters in the game."""

    def __init__(self, name, description, weakness, drop):
        """
        Initialize an Enemy object.

        Args:
            name (str): Enemy's name.
            description (str): Description of the enemy.
            weakness (str): Item name that defeats the enemy.
            drop (Item): Item dropped by the enemy when defeated.
        """
        super().__init__(name, description)
        self.weakness = weakness
        self.is_enemy = True
        self.drop = drop

    def get_weakness(self):
        """Return the enemy's weakness item name."""
        return self.weakness

    def fight(self, combat_item):
        """
        Fight the enemy using a combat item.

        Args:
            combat_item (str): Item used to fight.
        Returns:
            Item or bool: Item if defeated, False if player dies.
        """
        if combat_item.lower() == self.weakness:
            print(f"You fend {self.name} off with the {combat_item}")
            print(f"You have obtained {self.drop.get_name()}!")
            return self.drop
        print(f"{self.name} swallows you, little wimp.")
        death_screen()
        return False

    def give(self, give_item_name):
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

    def __init__(self, name, description, weakness, drop):
        """
        Initialize a Boss object.

        Args:
            name (str): Boss's name.
            description (str): Description of the boss.
            weakness (str): Item name that defeats the boss.
            drop (Item): Item dropped by the boss when defeated.
        """
        super().__init__(name, description, weakness, drop)
        self.is_boss = True
