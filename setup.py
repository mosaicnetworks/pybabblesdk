import os

from setuptools import setup, find_packages


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='pybabblesdk',
    version='0.1.1',
    description='An SDK for developing babble clients in python.',
    long_description=read('README.md'),
    packages=find_packages(exclude=['tests', 'examples']),
    keywords='babble',
    author='Mosaic Networks',
    author_email='kevin@babble.io',
    maintainer='Kevin Jones',
    maintainer_email='kevin@babble.io',
    url='http://github.com/babbleio/pybabblesdk', install_requires=['six']
)
