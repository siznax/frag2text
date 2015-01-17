#!/usr/bin/env python

import os

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='frag2text',
    version='0.0.1',
    description='Select and reverse-Markdown (html2text) web page fragments.',
    long_description=readme,
    url='https://github.com/siznax/frag2text/',
    license='MIT',
    author='Steve @siznax',
    author_email='steve@siznax.net',
    py_modules=['frag2text'],
    packages=find_packages(exclude=['tests']),
    install_requires=['cssselect', 'html2text', 'html5lib', 'lxml', 'requests'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3'
    ],
)
