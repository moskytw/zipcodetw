#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
from setuptools.command.install import install

class zipcodetw_install(install):

    def run(self):
        import zipcodetw.builder
        print('Building ZIP code index ... ')
        sys.stdout.flush()
        zipcodetw.builder.build()
        install.run(self)

from setuptools import setup, find_packages

setup(

    name = 'zipcodetw',
    version = '0.6.6',
    description = 'Find Taiwan ZIP code by address fuzzily.',
    long_description = open('README.rst', encoding='UTF-8').read(),

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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    packages = find_packages(),
    install_requires = ['six', 'unicodecsv'],
    setup_requires = ['six', 'unicodecsv'],
    package_data = {'zipcodetw': ['*.csv', '*.db']},

    cmdclass = {'install': zipcodetw_install},

)
