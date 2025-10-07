"""Main module for the adventure game."""

from cave import Cave
from character import Person, Enemy, Boss
from item import Item

instructions = [
    """
Please read this tutorial in detail!

This is a text-based adventure game set in a cave system. 
The caves are all connected, and you can move between them.
In some caves, there are people, enemies and/or items. 

A dragon has been terrorising the cave system, stealing treasures and harming the inhabitants.
You are a brave adventurer exploring these caves. 
Your righteous sense of justice drives you to slay the dragon. 
Help the people and you shall be rewarded.
""",
    """
Here are a few of the commands you can use. 

Type move to move to a connected cave.
Type inventory to see your inventory.
    You may then choose to view an item's description. (Which may contain a hint!)
    Obviously, you can only give/fight with items from your inventory. 
Type ? to show the tutorial.
Type quit to quit the game. 
""",
    """
In a cave with a person:
    Type talk to talk with them.
        They may be in need of something!
    Type give to give something to them.
In a cave with an enemy:
    Type talk to talk with them.
    Type fight to fight them using an item. 
        Make sure this item is something that will work against them though!
        If it does, you'll be able to defeat them and claim some nice loot, otherwise its GAME OVER.
        Be careful about giving an item to an enemy!
In a cave with an item: 
    Type pickup to pick the item up and add it to your inventory.
""",
    """
After completing an action (e.g. talking to someone, picking up an item), press enter to continue. 
This is to avoid having excessive "Press enter to continue" statements.

Please be careful about typos, as the game is quite space-sensitive and unintelligent.
""",
]


def tutorial():
    """Show the tutorial instructions."""
    for section in instructions:
        print("\n---")
        print(section)
        input("Press enter to continue")
    print("\n---\n\nI hope you have fun playing this!")


# Caves
cavern = Cave("cavern")
grotto = Cave("grotto")
dungeon = Cave("dungeon")
lair = Cave("lair")
swamp = Cave("swamp")

cavern.set_description("A damp and dirty cave.")
grotto.set_description(
    "A small cave with a large pond.\n"
    "The sounds of waves can be heard echoing from the distance."
)
dungeon.set_description("A large cave with a hearty forge.")
lair.set_description(
    "An ominous cave shining with treasures.\n"
    "The air is thick with smoke and the ground trembles."
)
swamp.set_description(
    "A murky cave filled with swampy water and fluorescent fungi.\n"
    "The air is filled with the stench of decay."
)

#          cavern(start)
# swamp    grotto         dungeon
#          lair
cavern.link_cave(grotto, "south")
grotto.link_cave(cavern, "north")
dungeon.link_cave(grotto, "west")
grotto.link_cave(dungeon, "east")
lair.link_cave(grotto, "north")
grotto.link_cave(lair, "south")
swamp.link_cave(grotto, "east")
grotto.link_cave(swamp, "west")


# Items
torch = Item("torch", "Effective against water type enemies.")
slime_remains = Item("slime remains", "Disgusting, gooey stuff. Sticky to touch.")
water_bomb = Item("water bomb", "An excellent combat item against fire type enemies.")
belinda = Item("Belinda", "A sturdy hammer, a blacksmith's best friend.")
dragon_slayer = Item(
    "dragon slaying sword",
    "An excellent sword crafted by the master blacksmith, Senshi.",
)
frog_hide = Item(
    "frog hide",
    "A tough hide. Solid substitute for armour, "
    "with the added benefit of immunity from insect bites.",
)

# People
harry_conversation_dict = {
    "pre_gift": (
        "Hello. I am writing a PhD on the hostile blue slimes that can be found in grottos.\n"
        "The dragon's been making my work difficult, stealing samples and causing trouble.\n"
        "You look like a solid adventurer.\n"
        "You bring me some slime remains, I'll get you something to help against the dragon.\n"
        "Otherwise, leave me alone."
    ),
    "grateful": (
        "Ah, these are excellent slime remains—just what I needed for my research.\n"
        "Here, take this water bomb. It's proven handy for keeping the dragon at bay.\n"
        "Use it wisely on your quest."
    ),
    "ungrateful": "What is this? I'm only interested in slimes. What a bother.",
    "post_gift": (
        "Good to see you again.\n"
        "I trust the water bomb will help you against the dragon."
    ),
}

harry = Person(
    name="Harry",
    description="A young researcher.",
    conversations=harry_conversation_dict,
    quest_items=[slime_remains, water_bomb],
)

senshi_conversation_dict = {
    "pre_gift": (
        "Hey there! Your sword is looking a little damaged...\n"
        "I'm a blacksmith, want a new one?\n"
        "That damned frog stole my dear Belinda though...\n"
        "That dragon's drawn all sorts of monsters here.\n"
        "I'm gonna need my trusty hammer back to make you a good sword."
    ),
    "gratitude": (
        "Thank you. I'll make you a top-notch sword. Just wait.\n"
        "(to the hammer): Oh, Belinda, my sweet beauty. I'm so glad you have returned to me."
    ),
    "ungrateful": "... I'm not sure what I'd do with this. You keep it.",
    "post_gift": (
        "This sword has served you well, yes?\n"
        "Come back if you want any more equipment!\n"
        "I'll always be happy to serve the adventurer who brought back my dear hammer."
    ),
}
senshi = Person(
    name="Senshi",
    description="An experienced dwarf blacksmith.",
    conversations=senshi_conversation_dict,
    quest_items=[belinda, dragon_slayer],
)

# Enemies
sledge = Enemy(
    "Sledge",
    "A wet blue slime emitting a low growl as it slides around.",
    "torch",
    slime_remains,
)
sledge.set_conversation("Hangry...Hanggrry...")

kermit = Enemy(
    "Kermit",
    "A green frog the size of a Great Dane with bulging eyes and a wide mouth.",
    "torch",
    frog_hide,
)

# Boss dragon
ifir = Boss(
    "Ifir",
    "A massive red dragon with scales as hard as steel and burning ruby eyes.",
    ["dragon slaying sword", "water bomb"],
)

# Put things in caves
grotto.set_character(sledge)
cavern.set_item(torch)
cavern.set_character(harry)
dungeon.set_character(senshi)
lair.set_character(ifir)
swamp.set_character(kermit)
swamp.set_item(belinda)


# Inventory
inventory = []


def inventory_names():
    """Return a dictionary of lowercase item name to item description for each item in the inventory."""
    return {item.get_name().lower(): item.get_description() for item in inventory}


def show_inventory():
    """Show a humanized list of inventory items, then ask to show descriptions of any item."""
    names_list = [item.get_name() for item in inventory]
    match len(inventory):
        case 0:
            print("You have nothing in your inventory.")
        case 1:
            print(f"You have a {names_list[0]} in your inventory.")
        case _:
            print(
                f"You have {', '.join(names_list[:-1])} and {names_list[-1]} in your inventory."
            )
    show_descriptions = input("Do you want to see the description of any items? y/n\n")
    if show_descriptions == "y":
        item_name = input("\nWhich item? Type none to exit.\n").strip().lower()
        while item_name != "none":
            if item_name in inventory_names():
                print(inventory_names()[item_name])
            else:
                print("This item is not in your inventory.")
            item_name = input("\nWhich item? Type none to exit.\n").strip().lower()
    else:
        print("Alright.")

# Health
health = 3

# Status
current_cave = cavern
# IMPORTANT: DEVELOPMENT MODE
# inventory.append(torch)
# inventory.append(water_bomb)
# inventory.append(dragon_slayer)

# IMPORTANT: uncomment the lines below when not in development
# tutorial()
# input()

while True:
    print("---")
    print()
    print("You are in:")
    current_cave.get_details()
    inhabitant = current_cave.get_character()
    item = current_cave.get_item()

    COMMAND = ""
    while COMMAND == "":
        COMMAND = input("What do you want to do?\n").strip().lower()

    print()
    match COMMAND:
        case "quit" | "exit" | "end" | "leave":
            break
        case "move" | "go":
            if len(current_cave.linked_caves) > 1:
                direction = input("What direction do you want to go in?\n").strip().lower()
                current_cave = current_cave.move(direction)
            else:
                current_cave = current_cave.move(list(current_cave.linked_caves.keys())[0])
        case "talk" | "speak":
            if inhabitant:
                inhabitant.talk()
            else:
                print("There is no-one to talk to.")
        case "fight" | "battle" | "attack":
            if not inventory:
                print("You have nothing in your inventory to fight with.")
            elif not inhabitant:
                print("There is no-one to fight in this cave.")
            elif isinstance(inhabitant, Boss):
                combat_items = (
                    input(
                        "You have chosen to face Ifir, the dragon!\n"
                        "You will need 2 items to defeat this formiddable foe.\n"
                        "What shall you choose, brave adventurer?\n"
                        "(Separate items with a comma and a space, e.g. item1, item2)\n"
                    )
                    .strip()
                    .lower()
                ).split(", ")
                if len(combat_items) != 2:
                    print("You must choose exactly 2 items.")
                else:
                    CONTINUE_FIGHT = True
                    for item in combat_items:
                        if item not in inventory_names():
                            print(f"{item} is not in your inventory.")
                            CONTINUE_FIGHT = False
                    if CONTINUE_FIGHT:
                        inhabitant.fight(combat_items)
                        break
            else:
                combat_item = (
                    input(
                        "What item would you like to fight with? "
                        "You cannot fight barehanded.\n"
                    )
                    .strip()
                    .lower()
                )

                if combat_item not in inventory_names():
                    print("That item is not in your inventory.")
                else:
                    loot = inhabitant.fight(combat_item)
                    if loot:
                        current_cave.remove_character()
                        inventory.append(loot)
                    else:
                        break
        case "pickup" | "pick up" | "get":
            if item:
                if inhabitant and isinstance(inhabitant, Enemy):
                    print(
                        f"You reach for the {item.get_name()}, "
                        f"only for {inhabitant.get_name()} to attack you!"
                    )
                    health -= 1
                else:
                    inventory.append(item)
                    item.pickup()
                    current_cave.remove_item()
            else:
                print("There is nothing to pick up.")
        case "give" | "handover":
            if not inventory:
                print("You have nothing to give.")
            elif not inhabitant:
                print("There is no one here to give anything to.")
            else:
                give_item_name = (
                    input(f"What would you like to give {inhabitant.get_name()}?\n")
                    .strip()
                    .lower()
                )
                print()
                if give_item_name not in inventory_names():
                    print("That item is not in your inventory.")
                else:
                    give_result = inhabitant.give(give_item_name)
                    print()
                    if give_result:
                        inventory.append(give_result)
                        give_result.obtain()
                    elif give_result is False:
                        break
                    elif give_result is None:
                        pass
                    else:
                        print(f"{give_result=}")
                        print("Improper give result.")

        case "inventory" | "inv" | "show inventory" | "show inv" | "bag":
            show_inventory()
            continue  # avoid "Press enter to continue" after showing inventory
        case "?" | "help" | "tutorial":
            tutorial()
        case _:
            print("You cannot do that.")

    if health <= 0:
        print()
        print("After a series of misadventures, you have succumbed to your injuries.")
        print()
        print("***")
        print("YOU HAVE DIED")
        print("***")
        break
    input()
