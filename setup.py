#!/usr/bin/env python
# # coding: utf-8

from setuptools import setup
from unittest_utils import __version__

setup(
    name='unittest_utils',
    description='Timeout helper',
    long_description='A library to allow repeat a function until timeout is finished',
    version=__version__,
    author='IT Attractor',
    author_email='info@it-attractor.com',
    url='https://github.com/ITAttractor/ddt',
    py_modules=['unittest_utils'],
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
)

