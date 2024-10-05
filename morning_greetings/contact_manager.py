"""
This module is used to manage a list of contacts, from a list, CSV, JSON or text file
"""

import json
from enum import IntEnum
from pathlib import Path, PurePath
from typing import Optional, Iterable
from .logger import get_logger


class ImportMode(IntEnum):
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
    :param csv_fname: A CSV file to extract contacts from
    :param csv_sep: Specify a custom CSV separator if it isn't the default comma
    :param json_fname: A JSON/JSONL file to extract contacts from
    :param txt_fname: A text file to extract contacts from
    :param txt_sep: Specify a custom separator (default is a whitespace)
    """

    def __init__(
        self,
        import_mode: ImportMode = ImportMode.LIST,
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

        if not 0 < import_mode < 16:
            # regardless of the combination of import modes, we shouldn't get a number outside
            # the range [1, 15], which means we should raise if one is passed (N.B. in binary,
            # combining 1, 2, 4, 8 (0b0001, 0b0010, 0b0100, 0b1000 respectively) will give back
            # 15 (0b1111), hence the upper limit)
            raise ValueError("An invalid contact extraction mode was provided")

        if import_mode & ImportMode.LIST:
            if contact_list is None:
                raise ValueError(
                    "Extraction mode `LIST` was chosen, but none was provided"
                )
            self._contacts.extend(contact_list)
            self._logger.info("Added contacts to list: %s", contact_list)

        if import_mode & ImportMode.CSV:
            if csv_fname is None:
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
            if json_fname is None:
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

                    if is_jsonl:
                        # makes a list of each line (a.k.a. each json stored)
                        json_list = list(f_json)

                        for json_str in json_list:
                            json_dict = json.loads(json_str)
                            self._contacts.append(json_dict)
                            self._logger.info("Added contact to list: %s", json_dict)

                    else:
                        # if a json file is provided, we can load it directly
                        json_dict = json.load(f_json)
                        self._contacts.append(json_dict)
                        self._logger.info("Added contact to list: %s", json_dict)

        if import_mode & ImportMode.TXT:
            if txt_fname is None:
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

        contact = {"name": name, "email": email, "preferred_time": preferred_time}
        self._contacts.append(contact)
        self._logger.info("Added contact to list: %s", contact)

    def remove_contact(self, name: str) -> None:
        """
        Removes a contact from the contact list

        :param name: The contact to be removed
        """

        # filter out any contacts which match the provided name
        self._contacts = list(filter(lambda c: c["name"] != name, self._contacts))
        self._logger.info("Removed %s from contact list", name)

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
