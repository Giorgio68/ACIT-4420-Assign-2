"""
This module is used to manage a list of contacts, from a list, CSV, JSON or text file
"""

import re
import json
from enum import IntEnum
from pathlib import Path, PurePath
from typing import Optional, Iterable
from .logger import get_logger


class ImportMode(IntEnum):
    """
    Used to specify which mode should be used to add contacts
    """

    NONE = 0
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
    :param csv_fname: A CSV file to extract contacts from
    :param csv_sep: Specify a custom CSV separator if it isn't the default comma
    :param json_fname: A JSON/JSONL file to extract contacts from
    :param txt_fname: A text file to extract contacts from
    :param txt_sep: Specify a custom separator (default is a whitespace)
    """

    def __init__(
        self,
        import_mode: ImportMode = ImportMode.NONE,
        *,
        contact_list: Optional[list] = None,
        csv_fname: Optional[str | list[str] | Path | list[Path]] = None,
        csv_sep: Optional[str] = None,
        json_fname: Optional[str | list[str] | Path | list[Path]] = None,
        txt_fname: Optional[str | list[str] | Path | list[Path]] = None,
        txt_sep: Optional[str] = None,
    ) -> None:
        """
        Constructor method
        """
        self._contacts = []
        self._logger = get_logger()

        if not -1 < import_mode < 16:
            # regardless of the combination of import modes, we shouldn't get a number outside
            # the range [1, 15], which means we should raise if one is passed (N.B. in binary,
            # combining 1, 2, 4, 8 (0b0001, 0b0010, 0b0100, 0b1000 respectively) will give back
            # 15 (0b1111), hence the upper limit)
            raise ValueError("An invalid contact import mode was provided")

        if import_mode == ImportMode.NONE:
            self._logger.info("Created empty contact list")
            return

        if import_mode & ImportMode.LIST:
            if not contact_list:
                raise ValueError(
                    "Extraction mode `LIST` was chosen, but none was provided"
                )
            self._contacts.extend(contact_list)
            self._logger.info("Added contacts to list: %s", contact_list)

        if import_mode & ImportMode.CSV:
            if not csv_fname:
                raise ValueError(
                    "Extraction mode `CSV` was chosen, but no file name was provided"
                )

            # if we didn't pass a list of files, create a list to iterate over
            if not isinstance(csv_fname, Iterable):
                csv_fname = [csv_fname]

            if csv_sep is None:
                csv_sep = ","

            for file in csv_fname:
                with open(file, "r", encoding="utf-8") as f_csv:
                    for line in f_csv:
                        name, email, preferred_time = line.split(csv_sep)
                        self.add_contact(name, email, preferred_time)

        if import_mode & ImportMode.JSON:
            if not json_fname:
                raise ValueError(
                    "Extraction mode `JSON` was chosen, but no file name was provided"
                )

            # if we didn't pass a list of files, create a list to iterate over
            if not isinstance(json_fname, Iterable):
                json_fname = [json_fname]

            for file in json_fname:
                with open(file, "r", encoding="utf-8") as f_json:
                    # if passing a jsonl file, we need to handle it differently from a normal
                    # json, so check the extension
                    if isinstance(file, PurePath):
                        is_jsonl = file.suffix.lower() == ".jsonl"
                    elif isinstance(file, str):
                        is_jsonl = file.endswith(".jsonl")
                    else:
                        is_jsonl = False

                    if is_jsonl:
                        # makes a list of each line (a.k.a. each json stored)
                        json_list = list(f_json)

                        for json_str in json_list:
                            json_dict = json.loads(json_str)
                            self.add_contact(
                                json_dict["name"],
                                json_dict["email"],
                                json_dict["preferred_time"],
                            )

                    else:
                        # if a json file is provided, we can load it directly
                        json_dict = json.load(f_json)
                        self.add_contact(
                            json_dict["name"],
                            json_dict["email"],
                            json_dict["preferred_time"],
                        )

        if import_mode & ImportMode.TXT:
            if not txt_fname:
                raise ValueError(
                    "Extraction mode `TXT` was chosen, but no file name was provided"
                )

            # if we didn't pass a list of files, create a list to iterate over
            if not isinstance(txt_fname, Iterable):
                txt_fname = [txt_fname]

            for file in txt_fname:
                with open(file, "r", encoding="utf-8") as f_txt:
                    for line in f_txt:
                        if txt_sep is None:
                            name, email, preferred_time = line.split()
                        else:
                            name, email, preferred_time = line.split(txt_sep)

                        self.add_contact(name, email, preferred_time)

    def add_contact(self, name: str, email: str, preferred_time: str = "0800") -> None:
        """
        This method allows a user to add a new contact to the contact list

        :param name: The contact's name
        :param email: The contact's email
        :param preferred_time: The time to send a greeting to the contact
        """

        if not name:
            raise ValueError("No name was provided")

        if self._contact_exists(name):
            self._logger.warning("Contact %s exists already", name)
            return

        if not email:
            raise ValueError("No email was provided")

        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise ValueError("An invalid email address was provided")

        if not preferred_time:
            raise ValueError("No preferred_time was provided")

        if not re.match(r"\d{4}", preferred_time):
            raise ValueError("An invalid preferred time was provided")

        contact = {"name": name, "email": email, "preferred_time": preferred_time}
        self._contacts.append(contact)
        self._logger.info("Added contact to list: %s", contact)

    def get_contact(self, name: str) -> dict[str] | None:
        """
        Retrieves a specified contact. Note that the contact returned is a reference, not a copy

        :param name: The contact to retrieve
        :return: The `dict` object storing the contact itself, or `None` if no contact is found
        """
        for contact in self._contacts:
            if contact["name"] == name:
                return contact

        self._logger.warning("Contact %s does not exist", name)
        return None

    def modify_contact(
        self,
        name: str,
        new_name: Optional[str] = None,
        email: Optional[str] = None,
        preferred_time: Optional[str] = None,
    ) -> None:
        """
        Allows a user to modify a contact's fields, as desired

        :param name: The contact to modify
        :param new_name: A new name for the contact
        :param email: The new email address
        :param preferred_time: The new preferred time for sending
        """
        if not name:
            raise ValueError("No name was provided")

        contact = self.get_contact(name)
        if contact is None:
            raise ValueError("An invalid contact name was provided")

        if new_name:
            contact["name"] = new_name

        if email:
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                raise ValueError("An invalid email address was provided")

            contact["email"] = email

        if preferred_time:
            if not re.match(r"\d{4}", preferred_time):
                raise ValueError("An invalid preferred time was provided")

            contact["preferred_time"] = preferred_time

        self._logger.info("Changed contact %s to: %s", name, contact)

    def remove_contact(self, name: str) -> None:
        """
        Removes a contact from the contact list.

        :param name: The contact to be removed
        """

        if not self._contact_exists(name):
            raise ValueError("A non-existant contact name was given")

        # filter out any contacts which match the provided name
        self._contacts = list(filter(lambda c: c["name"] != name, self._contacts))
        self._logger.info("Removed %s from contact list", name)

    def _contact_exists(self, name: str) -> bool:
        """
        Checks whether a contact already exists or not

        :param name: The name to check
        :return: A boolean indicating if a contacts is stored or not
        """
        return bool(list(filter(lambda c: c["name"] == name, self._contacts)))

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

    def __bool__(self) -> bool:
        return bool(self._contacts)
