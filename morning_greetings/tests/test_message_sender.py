"""
Tests the `message_sender` module
"""

import unittest
from ..message_sender import send_message


class TestContactManager(unittest.TestCase):
    def test_sender(self):
        send_message("test@email.org", "Hello")

        # make sure that an exception is raised if an empty email address or body is provided
        self.assertRaises(ValueError, send_message, "test@email.org", "")
        self.assertRaises(ValueError, send_message, "", "Hello")

        # ensure correct data type has to be passed
        self.assertRaises(ValueError, send_message, "test@email.org", 123)
        self.assertRaises(ValueError, send_message, True, "Hello")
