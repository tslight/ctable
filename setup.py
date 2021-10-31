# Copyright (c) 2021, Toby Slight. All rights reserved.
# ISC License (ISCL) - see LICENSE file for details.

from setuptools import setup, find_packages
import subprocess


def get_commit_hash():
    """Talk to git and find out the tag/hash of our latest commit"""
    try:
        p = subprocess.Popen(
            ["git", "describe", "--tags", "--dirty", "--always"], stdout=subprocess.PIPE
        )
    except EnvironmentError:
        print("Couldn't run git to get a version number for setup.py")
        return
    ver = p.communicate()[0]
    return ver.strip()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ctable",
    version=get_commit_hash(),
    author="Toby Slight",
    author_email="tslight@pm.me",
    description="Curses Tables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tslight/ctable",
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ),
    entry_points={
        "console_scripts": [
            "ctable = ctable.__main__:main",
        ],
    },
)
