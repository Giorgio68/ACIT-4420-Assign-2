"""
This module is used to manage all contacts to which morning greetings should be sent
"""

import json
from pathlib import Path, PurePath
from enum import Enum
from typing import Optional, Iterable


class ImportMode(Enum):
    """
    Used to specify which mode should be used to add contacts
    """

    LIST = 1
    CSV = 2
    JSON = 4
    TXT = 8


class ContactsManager:
    """
    Class used to store and manage a list of contacts. Contacts can either be added by providing a
    list, or a filename, and the insertion mode. For files, the correct insertion must be chosen.
    Multiple insertion modes can be selected by OR'ing the different import modes

    :param insertion_mode: Whether to extract the contacts from a list, csv, json, etc.
    :param contact_list: A list of contacts, if provided
    :param file_name: The file to extract contacts from, if provided
    """

    def __init__(
        self,
        insertion_mode: ImportMode = ImportMode.LIST,
        *,
        contact_list: Optional[list] = None,
        csv_fname: Optional[str | list[str] | Path | list[Path]] = None,
        json_fname: Optional[str | list[str] | Path | list[Path]] = None,
        txt_fname: Optional[str | list[str] | Path | list[Path]] = None,
    ) -> None:
        """
        Constructor method
        """
        self._contacts = []

        if insertion_mode & ImportMode.LIST.value:
            if contact_list is None:
                raise ValueError(
                    "Extraction mode `LIST` was chosen, but none was provided"
                )
            self._contacts.extend(contact_list)

        if insertion_mode & ImportMode.CSV.value:
            if csv_fname is None:
                raise ValueError(
                    "Extraction mode `CSV` was chosen, but no file name was provided"
                )

            if not isinstance(csv_fname, Iterable):
                csv_fname = [csv_fname]

            for file in csv_fname:
                with open(file, "r", encoding="utf-8") as f_csv:
                    for line in f_csv:
                        name, email, preferred_time = line.split(",")
                        self.add_contact(name, email, preferred_time)

        if insertion_mode & ImportMode.JSON.value:
            if json_fname is None:
                raise ValueError(
                    "Extraction mode `JSON` was chosen, but no file name was provided"
                )

            if not isinstance(json_fname, Iterable):
                json_fname = [json_fname]

            for file in json_fname:
                with open(file, "r", encoding="utf-8") as f_json:
                    if isinstance(file, PurePath):
                        is_jsonl = file.suffix.lower() == ".jsonl"
                    elif isinstance(file, str):
                        is_jsonl = file.endswith(".jsonl")

                    if is_jsonl:
                        json_list = list(f_json)

                        for json_str in json_list:
                            json_dict = json.loads(json_str)
                            self._contacts.append(json_dict)

                    else:
                        json_dict = json.load(f_json)
                        self._contacts.append(json_dict)

        if insertion_mode & ImportMode.TXT.value:
            if txt_fname is None:
                raise ValueError(
                    "Extraction mode `TXT` was chosen, but no file name was provided"
                )

            if not isinstance(txt_fname, Iterable):
                txt_fname = [txt_fname]

            for file in txt_fname:
                with open(file, "r", encoding="utf-8") as f_txt:
                    for line in f_txt:
                        name, email, preferred_time = line.split()
                        self.add_contact(name, email, preferred_time)

    def add_contact(
        self, name: str, email: str, preferred_time: str = "08:00 AM"
    ) -> None:
        """
        This method allows a user to add a new contact to the contact list

        :param name: The contact's name
        :param email: The contact's email
        :param preferred_time: The time to send a greeting to the contact
        """

        contact = {"name": name, "email": email, "preferred_time": preferred_time}
        self._contacts.append(contact)

    def remove_contact(self, name: str) -> None:
        """
        Removes a contact from the contact list

        :param name: The contact to be removed
        """

        self._contacts = [c for c in self._contacts if c["name"] != name]

    def get_contacts(self) -> list[dict]:
        """
        Returns the contact list

        :return: The contacts
        """
        return self._contacts

    def list_contacts(self) -> None:
        """
        Prints a formatted list of all contacts and their details
        """
        for contact in self._contacts:
            print(
                f"Name: {contact['name']}, Email: {contact['email']}, Preferred Time: {contact['preferred_time']}"
            )

    def __repr__(self) -> str:
        repr_str = ""

        for contact in self._contacts:
            repr_str += f"Name: {contact['name']}, Email: {contact['email']}, Preferred Time: {contact['preferred_time']}\n"

        return repr_str

    def __str__(self) -> str:
        repr_str = ""

        for contact in self._contacts:
            repr_str += f"Name: {contact['name']}, Email: {contact['email']}, Preferred Time: {contact['preferred_time']}\n"

        return repr_str
