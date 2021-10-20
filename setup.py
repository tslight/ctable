# Copyright (c) 2021, Toby Slight. All rights reserved.
# ISC License (ISCL) - see LICENSE file for details.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ctable",
    version="0.0.1",
    author="Toby Slight",
    author_email="tslight@pm.me",
    description="Curses Tables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tslight/ctable",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'ctable = ctable.__main__:main',
        ],
    }
)
