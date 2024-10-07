"""
Module to generate and return different possible greetings
"""

from random import randint
from .logger import get_logger


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

    if not name:
        raise ValueError("A name must be provided to generate a greeting")

    if not isinstance(name, str):
        raise ValueError("`name` has an invalid data type")

    # choose a random greeting from the imported ones and format it
    greeting = _greetings[randint(0, len(_greetings) - 1)].format(name=name)

    get_logger().info("Generated new greeting: %s", greeting)

    return greeting
