"""
Tests the `message_generator` module
"""

import unittest
from ..message_generator import generate_message


class TestContactManager(unittest.TestCase):
    def test_generator(self):
        # test that we get different messages each time
        for _ in range(10):
            print(generate_message("Giorgio"))
