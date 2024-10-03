# ACIT4420 Assignment 2

## Installation

Installation is relatively straight-forward: simply run
```pip install .```
to install the package.

## Tests

Unit tests can be run by calling
```python setup.py test```

## Importing contacts

Contacts can be given in different formats, such as a python list, stored in a CSV, JSON or text file. The file names can be provided as both a single file or a list of files, and as either a string or `pathlib.Path` object.
A separator can also be specified for CSV and text files if so desired.

## Running the program

This package can be executed in two different ways: the first is executing the module directly, using
```python -m morning_greetings <args>```
The user can provide their own files as arguments: CSV files can be provided using the `--csv` option; JSON files with the `--json` option; and text files with the `--txt` option. Multiple files of the same type can be passed (e.g.: ```python -m morning_greetings --json file1 --json file2```)

The second method is using the `main.py` script provided:
```python main.py <args>```
This works the same way as when executing the package directly, by passing files to it using arguments.
