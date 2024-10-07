"""
Tests the `contact_manager` module
"""

import unittest
from pathlib import Path
from ..contact_manager import ContactsManager, ImportMode


contact_folder = Path(".") / "contacts"

contact_manager = ContactsManager(
    ImportMode.LIST | ImportMode.CSV | ImportMode.JSON | ImportMode.TXT,
    contact_list=[
        {
            "name": "Giorgio",
            "email": "s351995@oslomet.no",
            "preferred_time": "10:00AM",
        }
    ],
    csv_fname=contact_folder / "contacts.csv",
    json_fname=[
        contact_folder / "contact.json",
        contact_folder / "contacts.jsonl",
    ],
    txt_fname=contact_folder / "contacts.txt",
)

class TestContactManager(unittest.TestCase):
    def test_print_contacts(self):
        print(repr(contact_manager))
        print(contact_manager.get_contacts())

    def test_new_contact(self):
        contact_manager.add_contact("New friend", "fr@example.com", "0600")
        print(contact_manager.get_contacts())

        # make sure it errors when not passing valid parameters
        self.assertRaises(ValueError, contact_manager.add_contact, "", "abc@example.com", "0800")
        self.assertRaises(ValueError, contact_manager.add_contact, "George", "", "0800")
        self.assertRaises(ValueError, contact_manager.add_contact, "George", "abc@example.com", "")

    def test_remove_contact(self):
        contact_manager.remove_contact("New friend")
        print(contact_manager.get_contacts())

        # make sure it errors if we try to remove an invalid contact
        self.assertRaises(ValueError, contact_manager.remove_contact, "Invalid name")

    def test_get_contacts(self):
        print(contact_manager.get_contacts())


if __name__ == "__main__":
    unittest.main()
