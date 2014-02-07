#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import _zipcodetw

setup(

    name = 'zipcodetw',
    version = _zipcodetw.__version__,
    description = 'Find Taiwan ZIP code by address fuzzily.',
    long_description = open('README.rst').read(),

    author = 'Mosky',
    url = 'https://github.com/moskytw/zipcodetw',
    author_email = 'mosky.tw@gmail.com',
    license = 'MIT',
    platforms = 'any',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    py_modules = ['_zipcodetw'],
    packages = find_packages(),
    package_data = {'zipcodetw': ['*.csv']}

)

