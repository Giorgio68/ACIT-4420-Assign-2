# pylint: disable

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ACIT4420 Assignment 2",
    version="1.0.0",
    author="Giorgio Salvemini",
    author_email="s351995@oslomet.no",
    description=("The produced module for Assignment 2 in the subject ACIT4420"),
    url="https://github.com/Giorgio68/ACIT-4420-Assign-2",
    packages=["morning_greetings"],
    long_description=read("README.md"),
    test_suite="morning_greetings.tests",
    # install_requires=['peppercorn'],
)
