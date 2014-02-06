.. image:: https://pypip.in/v/zipcodetw/badge.png
   :target: https://pypi.python.org/pypi/zipcodetw

.. image:: https://pypip.in/d/zipcodetw/badge.png
   :target: https://pypi.python.org/pypi/zipcodetw

The ZIP Code Finder for Taiwan
==============================

This package lets you find ZIP code by address in Taiwan.

The main features:

1. Fast. It builds ZIP code index by tokenization.
2. Gradual. It returns partial ZIP code rather than noting when address is not
   detailed enoguh.
3. Lightweight. It depends on nothing.

Usage
-----

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

Installation
------------

It is available on PyPI:

.. code-block:: bash

    $ sudo pip install zipcodetw

Just install it and have fun. :)

Data
----

The ZIP code directory we use is provided by Chunghwa Post, and is available
from: http://www.post.gov.tw/post/internet/down/index.html#1808

Changelog
---------

v0.3
~~~~

1. It also normalizes Chinese numerals; and
2. builds 3x size of index for middle tokens now!
3. But initiation time increases to 1.3x.
4. ``zipcodetw.find`` is 1.05x faster.

v0.2
~~~~

1. ``zipcodetw.find`` is 8x faster now!
2. It has a better tokenizing logic; and
3. a better matching logic for sub-number now.
4. ``zipcodetw.find_zipcodes`` was removed.
5. Internal API was changed a lot.
6. The tests are better now.
