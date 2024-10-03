"""
Module to generate and return different possible greetings
"""

from random import randint


_greetings = [
    "Good Morning, {name}! Have a great day.....!",
    "Hello {name}! Hope your day is fantastic!",
    "Good day, {name}",
    "Top of the morning {name}!",
    "Have a lovely day, {name} :)",
]


def generate_message(name: str) -> str:
    """
    Retrieves a list of possible greetings, chooses one and formats it, and returns a string to
    the user

    :param name: The name of the person being greeted
    :return: A formatted string containing the greeting
    """

    # choose a random greeting from the imported ones
    greeting = _greetings[randint(0, len(_greetings) - 1)]

    return greeting.format(name=name)
