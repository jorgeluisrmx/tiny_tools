#!/usr/bin/env python
#-*- coding:utf-8 -*-

from distutils.core import setup
from setuptools import find_packages

setup(
    name='CyclingLog',
    version='1.0',
    author='jorgeluisrmx',
    author_email='jorgeluisrmx@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cylog = cyclinglog:main'
        ]},
    url='',
    license='LICENSE.txt',
    description='Cycling log manager and data analyzer',
    long_description=open('README.md').read(),
    install_requires=[
        'appdirs',
        'python-telegram-bot',
        'fysom',
        'googlemaps',
        'gpxpy'
    ]
)
