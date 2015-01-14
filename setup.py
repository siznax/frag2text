#!/usr/bin/env python

import os

import frag2text

from setuptools import setup

def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='frag2text',
    version=frag2text.__version__,
    description='Select and reverse-Markdown (html2text) web page fragments.',
    long_description=(read('README.md')),
    url='https://github.com/siznax/frag2text/',
    license='MIT',
    author='Steve @siznax',
    author_email='steve@siznax.net',
    py_modules=['frag2text'],
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
    
