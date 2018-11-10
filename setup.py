from os import path

from setuptools import setup, find_packages

# Gets the long description from the README file.
_here = path.abspath(path.dirname(__file__))
with open(path.join(_here, 'README.md'), encoding='utf-8') as f:
    _long_description = f.read()

setup(
    name='Meme-Machinery-VKHack2018',
    version='0.0.1',

    description='Simple meme generator project for VK Hackathon 2018',
    long_description=_long_description,
    long_description_content_type='text/markdown',

    url='git@github.com:stasbel/Meme-Machinery-VKHack2018.git',

    author='Stanislav Belyaev',
    author_email='stasbelyaev96@gmail.com',

    packages=find_packages(exclude=['contrib', 'docs', 'tests'])
)
