"""Module to manage player health."""

from termcolor import cprint

from utilities import death_screen

health = 5


def get():
    """Return the current health value."""
    return health


def update(amount: int):
    """
    Update health by a specified amount.
    Positive values increase health, negative values decrease health.
    If health drops to 0 or below, the death sequence is triggered.

    Args:
        amount (int): The amount to update health by. Default is 1.
    """
    if -1 * health >= amount:
        print(
            "\nAfter a series of misadventures, you have succumbed to your injuries.\n"
        )
        death_screen()
        return False
    cprint(
        f"\nYou have {'gained' if amount > 0 else 'lost'} {abs(amount)} health.",
        "red" if amount < 0 else "green",
    )
    print("♡" * (health + amount))
    return health + amount
