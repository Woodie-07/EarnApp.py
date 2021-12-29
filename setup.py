from setuptools import find_packages, setup
setup(
    name='earnapp',
    packages=find_packages(),
    version='0.0.2',
    description='A python library to interact with the EarnApp API',
    author='Woodie',
    url='https://github.com/Woodie-07/earnapp.py',
    install_requires=['requests'],
)