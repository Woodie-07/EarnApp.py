from setuptools import find_packages, setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='earnapp',
    packages=find_packages(),
    version='0.0.6',
    description='A python library to interact with the EarnApp API',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Woodie',
    author_email="woodie@woodie.cf",
    url='https://github.com/Woodie-07/earnapp.py',
    install_requires=['requests'],
)