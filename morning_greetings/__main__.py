"""
Allows direct execution of the package by calling `python -m morning_greetings`
"""

from time import sleep
import argparse
from .__init__ import (
    ContactsManager,
    ImportMode,
    generate_message,
    send_message,
    get_logger,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a contact list to send morning greetings to"
    )
    parser.add_argument("--csv", action="append")
    parser.add_argument("--json", action="append")
    parser.add_argument("--txt", action="append")

    args = parser.parse_args()
    logger = get_logger()

    import_mode = 0
    csv_fname = None
    json_fname = None
    txt_fname = None

    if args.csv:
        import_mode |= ImportMode.CSV
        csv_fname = args.csv
        logger.debug("Provided CSV files for import: %s", csv_fname)

    if args.json:
        import_mode |= ImportMode.JSON
        json_fname = args.json
        logger.debug("Provided JSON files for import: %s", json_fname)

    if args.txt:
        import_mode |= ImportMode.TXT
        txt_fname = args.txt
        logger.debug("Provided TXT files for import: %s", txt_fname)

    contact_manager = ContactsManager(
        import_mode,
        csv_fname=csv_fname,
        json_fname=json_fname,
        txt_fname=txt_fname,
    )
    logger.info("Initialized contact manager")

    contacts = contact_manager.get_contacts()
    greetings = []

    for contact in contacts:
        try:
            greetings.append(
                {
                    "contact": contact,
                    "msg": generate_message(contact["name"]),
                }
            )

        except ValueError as e:
            logger.exception(
                "Received an exception when trying to create a greeting: %s", repr(e)
            )

    sorted_greetings = sorted(greetings, key=lambda d: d["contact"]["preferred_time"])
    previous_time = 0

    for greeting in sorted_greetings:
        try:
            if (
                previous_time < int(greeting["contact"]["preferred_time"])
                or previous_time != 0
            ):
                previous_time = int(greeting["contact"]["preferred_time"])
                logger.info(
                    "It's too early to send %s a greeting, sleeping for a while...",
                    greeting["contact"]["name"],
                )
                # if the contact's preferred time is higher than the current time, sleep
                # for a few seconds
                sleep(3)

            send_message(greeting["contact"]["email"], greeting["msg"])
        except ValueError as e:
            logger.exception(
                "Received an exception when trying to send a greeting: %s", repr(e)
            )


if __name__ == "__main__":
    main()
