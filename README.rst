The ZIP Code Finder for Taiwan
==============================

This package lets you find the ZIP code quickly by any Taiwan address.

The main features:

1. Fast. It builds ZIP code index by tokenizating the addresses and rules.
2. Gradual. It allows a partial address to match partial ZIP code.
3. Lightweight. It depends on nothing.

Usage
-----

Find the ZIP code gradually:

.. code-block:: python

    >>> import zipcodetw
    >>> zipcodetw.find('臺北市')
    '1'
    >>> zipcodetw.find('臺北市信義區')
    '110'
    >>> zipcodetw.find('臺北市信義區市府路')
    '110'
    >>> zipcodetw.find('臺北市信義區市府路1號')
    '11008'

Find all possible ZIP codes:

.. code-block:: python

    >>> zipcodetw.find_zipcodes('臺北市信義區市府路')
    set(['11060', '11001', '11008', '11073'])

Installation
------------

It is easy to install this package from PyPI:

.. code-block:: bash

    $ sudo pip install zipcodetw

Have fun! :)

Data
----

The ZIP code data are provided by Chunghwa Post. The CSV is available here: http://www.post.gov.tw/post/internet/down/index.html#1808
