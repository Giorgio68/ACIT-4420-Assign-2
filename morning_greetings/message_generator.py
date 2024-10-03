"""
Module to generate and return different possible greetings
"""

import json
from random import randint
from pathlib import Path


def generate_message(name: str) -> str:
    """
    Retrieves a list of possible greetings, chooses one and formats it, and returns a string to
    the user

    :param name: The name of the person being greeted
    :return: A formatted string containing the greeting
    """

    config_path = Path(".") / "config"

    with open(config_path / "greeting_list.json", "r", encoding="utf-8") as f:
        greetings = json.load(f)["greetings"]

    # choose a random greeting from the imported ones
    greeting = greetings[randint(0, len(greetings)-1)]

    return greeting.format(name=name)
