"""
EarnApp.py - A Python library to interact with the EarnApp API
Copyright (C) 2022  Woodie

This file is part of EarnApp.py.

EarnApp.py is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

EarnApp.py is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with EarnApp.py. If not, see <https://www.gnu.org/licenses/>.
"""

from setuptools import find_packages, setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='earnapp',
    packages=find_packages(),
    version='0.1.6',
    description='A python library to interact with the EarnApp API',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Woodie',
    author_email="woodie@woodie.cf",
    url='https://github.com/Woodie-07/earnapp.py',
    install_requires=['requests'],
)
