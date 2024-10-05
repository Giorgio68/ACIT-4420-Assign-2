"""
Tests the `contact_manager` module
"""

import unittest
from pathlib import Path
from ..contact_manager import ContactsManager, ImportMode


class TestContactManager(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        contact_folder = Path(".") / "contacts"

        self.contact_manager = ContactsManager(
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

        super().__init__(*args, **kwargs)

    def test_print_contacts(self):
        print(repr(self.contact_manager))
        print(self.contact_manager.get_contacts())

    def test_new_contact(self):
        self.contact_manager.add_contact("New friend", "fr@example.com", "0600")
        print(self.contact_manager.get_contacts())

    def test_remove_contact(self):
        self.contact_manager.remove_contact("New friend")
        print(self.contact_manager.get_contacts())

    def test_get_contacts(self):
        print(self.contact_manager.get_contacts())


if __name__ == "__main__":
    unittest.main()
