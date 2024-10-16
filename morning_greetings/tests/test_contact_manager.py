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
            "preferred_time": "1000",
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
        self.assertRaises(
            ValueError, contact_manager.add_contact, "", "abc@example.com", "0800"
        )
        self.assertRaises(ValueError, contact_manager.add_contact, "George", "", "0800")
        self.assertRaises(
            ValueError, contact_manager.add_contact, "George", "abc@example.com", ""
        )
        self.assertRaises(
            ValueError, contact_manager.add_contact, "George", "invalid_email", "0800"
        )
        self.assertRaises(
            ValueError,
            contact_manager.add_contact,
            "George",
            "abc@example.com",
            "invalid_time",
        )

        # make sure duplicates cannot be added
        contact_manager.add_contact("New friend", "rf@example.com", "0700")

    def test_remove_contact(self):
        contact_manager.remove_contact("New friend")
        print(contact_manager.get_contacts())

        # make sure it errors if we try to remove an invalid contact
        self.assertRaises(ValueError, contact_manager.remove_contact, "Invalid name")

    def test_get_contacts(self):
        print(contact_manager.get_contacts())

    def test_boolean(self):
        self.assertTrue(bool(contact_manager))
        self.assertFalse(bool(ContactsManager(ImportMode.NONE)))

    def test_modify_contact(self):
        contact_manager.modify_contact(
            "Giorgio", "New Giorgio", "s351995+giorgio@oslomet.no", "0900"
        )
        print(contact_manager.get_contact("New Giorgio"))

    def test_get_contact(self):
        self.assertTrue(contact_manager.get_contact("Chris") is not None)
        self.assertTrue(contact_manager.get_contact("Invalid name") is None)


if __name__ == "__main__":
    unittest.main()
