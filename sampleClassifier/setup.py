# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sampleClassifier',
    version='0.0.1',
    description='Sample classifier for training',
    long_description=readme,
    author='Max Isenholt',
    author_email='misenholt@gmail.com',
    url='https://github.com/misenholt/sampleClassifier',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

