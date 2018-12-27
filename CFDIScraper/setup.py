#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='CFDIScraper',
    version='1.2',
    author='jorgeluisrmx',
    author_email='jorgeluisrmx@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cfdi = cfdiscraper:ep_cfdi',
            'zipcfdi = cfdiscraper:ep_zip_cfdi'
        ]},
    scripts=[ ],
    url='',
    license='LICENSE.txt',
    description='extractor de datos de conjuntos de archivos xml-cfdi comprimidos en zip',
    long_description=open('README.txt').read(),
    install_requires=[ ],
)
