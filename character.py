"""Module containing the Character, Person, and Enemy classes."""

from utilities import death_screen
import health


class Character:
    """Base class for all characters in the game."""

    def __init__(self, name: str, messages: dict):
        """
        Initialize a Character object.

        Args:
            name (str): Character's name.
            messages (dict): Character's messages.
        """
        self.name = name
        self.messages = messages
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
        print(self.messages["description"])

    def talk(self):
        """Print the character's conversation or a default message."""
        print()
        if self.conversation is not None:
            print(f"{self.name}: {self.conversation}")
        else:
            print(f"{self.name} does not want to talk to you.")

    def get_name(self):
        """Return the character's name."""
        return self.name


class Person(Character):
    """Class for non-enemy people in the game."""

    def __init__(self, name: str, messages: dict, quest_items: list):
        """
        Initialize a Person object.

        Args:
            name (str): Person's name.
            messages (dict): Conversation states.
                (strings description, pre_gift, grateful, ungrateful, post_gift as keys)
            quest_items (list): The item the person wants, the item given in exchange.
        """
        super().__init__(name, messages)
        self.conversation = messages["pre_gift"]
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
            self.set_conversation(self.messages["grateful"])
            self.talk()
            self.affinity += 1
            self.set_conversation(self.messages["post_gift"])
            return self.reward_item
        self.set_conversation(self.messages["ungrateful"])
        self.talk()
        self.affinity -= 1
        self.set_conversation(self.messages["pre_gift"])
        return None

    def fight(self, combat_item: str):
        """
        Print a message when the player tries to fight a person.

        Args:
            combat_item (str): Name of item used to fight.
        Returns:
            bool: True always (for game logic).
        """
        print(f"\nOuch! Don't fight me! Put that {combat_item} away!")
        return True


class Enemy(Character):
    """Class for enemy characters in the game."""

    def __init__(self, name: str, messages: dict, weakness, drop):
        """
        Initialize an Enemy object.

        Args:
            name (str): Enemy's name.
            messages (dict): Enemy's messages.
                (strings description, pre_fight, attack_success, attack_failure as keys)
            weakness (str): Name of the item that defeats the enemy.
            drop (Item): Item dropped by the enemy when defeated.
        """
        super().__init__(name, messages)
        self.weakness = weakness
        self.is_enemy = True
        self.messages = messages
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
            print()
            print(self.messages["attack_success"])
            if self.drop:
                print(f"You have obtained {self.drop.get_name()}!")
            return self.drop
        print(f"\n{self.messages['attack_failure']}")
        health.health = health.update(-2)
        return False

    def give(self, give_item_name: str):
        """
        Attempt to give an item to an enemy (results in death).

        Args:
            give_item (str): Item to give.
        Returns:
            bool: False (player dies).
        """
        give_item_name = give_item_name.lower()
        print(
            f"{self.name} reacts aggressively and attacks you. "
            "Unprepared, you cannot fight back."
        )
        print(self.messages["attack_failure"])
        health.health = health.update(-2)
        return False


class Boss(Enemy):
    """Class for the boss enemy (dragon)."""

    def __init__(self, name: str, weakness: list[str], messages: dict, drop=None):
        """
        Initialize a Boss object.

        Args:
            name (str): Boss's name.
            description (str): Description of the boss.
            weaknesses (list of strings): Item names that defeat the boss.
        """
        super().__init__(name=name, messages=messages, weakness=weakness, drop=drop)
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
            print(self.messages["attack_success"])
            print()
            print("YOU WIN!")
            return True
        print(self.messages["attack_failure"])
        print()
        death_screen()
        return False
