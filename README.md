# ACIT4420 Assignment 2

## Installation

Installation is relatively straight-forward: once the repository is cloned, simply run

```bash
python -m pip install .
```

to install the package.

## Tests

Unit tests can be run by calling
```python setup.py test```

## Importing contacts

Contacts can be given in different formats, such as a python list, stored in a CSV, JSON or text file. The file names can be provided as both a single file or a list of files, and as either a string or `pathlib.Path` object. A separator can also be specified for CSV and text files if so desired.

Before any contacts can be provided for import, an import mode has to be selected: this is done by importing the `ImportMode` Enum class, and selecting one of four possible modes, `LIST`, `CSV`, `JSON`, and `TXT`. If an import mode is not selected, any files or lists passed will simply be ignored.

The simplest way to add new contacts is using a list. These should contain a dictionary in the format:

```Python
{
    "name": <name>,
    "email": <email>,
    "preferred_time": <time>
}
```

When creating an external list of contacts, whether in CSV format or as a normal text file, the order to be followed is: `name`, `email`, and `preferred_time`. If JSON is preferred, a valid file must be created that includes the `name`, `email` and `preferred_time` values (essentially as the dictionary shown above); a `jsonl` file can also be passed, provided it has the correct extension and is valid.

Regardless of how contacts are stored, validation is done for both the email and preferred time: the email address *MUST* be valid, and the preferred sending time *MUST* be in the format `HHmm`, else a `ValueError` will be raised.

Examples for how to create a contact list can also be seen in the `contacts` folder.

## Running the program

This package can be executed in two different ways: the first is executing the module directly, using
```python -m morning_greetings <args>```
The user can provide their own files as arguments: CSV files can be provided using the `--csv` option; JSON files with the `--json` option; and text files with the `--txt` option. Multiple files of the same type can be passed (e.g.: ```python -m morning_greetings --json file1 --json file2```)

The second method is using the `main.py` script provided:
```python main.py <args>```
This works the same way as when executing the package directly, by passing files to it using arguments.

The `main.py` script also provides a starting point for users to build their own program around this package, if so desired.

### Message generation

Message generator is relatively straight-forward: a name is passed to the `generate_message` function (from the `message_generator` module), and it returns a randomly chosen greeting from a list. The name has to be a string of at least one character, else the function will raise a `ValueError`.

### Message sending

Sending messages is done by the `send_message` function from the `message_sender` module. Both the email and message body must be provided, and the email has to be a valid address.

### Logging

Logging happens automatically during execution.

The program is configured to both print all log `INFO` and above messages to console, and write *all* log messages (including `DEBUG` messages) to `morning_greetings.log`. This file has a maximum size of 3MB, before it is rotated and a new file is created. A maximum of three log files can exist simultaneously, and will be stored in the user's current directory (i.e. where the program is called).

## Caveats

While all modules from `morning_greeting` are able to be used independently, they do depend on the logging module, as it is used throughout the program's execution.
