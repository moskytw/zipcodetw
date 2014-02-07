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
3. Stand-alone. It depends on nothing.

Usage
-----

Find ZIP code gradually:

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

After v0.3, you can find ZIP code fuzzier:

.. code-block:: bash

    >>> zipcodetw.find('松山區')
    '105'
    >>> zipcodetw.find('秀山街')
    ''
    >>> zipcodetw.find('台北市秀山街')
    '10042'

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

v0.4
~~~~

1. It uses SQLite instead of memory to store index; so
2. initiation time is ~680x faster, i.e. ~30ms each import; and
3. ``zipcodetw.find`` is ~1.9x slower, i.e. ~2ms each call; and
4. has bigger package size.
5. All code was moved into ``zipcodetw`` package.

v0.3
~~~~

1. It builds full index for middle tokens; and
2. also normalizes Chinese numerals now!
3. ``zipcodetw.find`` is ~1.06x faster.
4. But initiation time increases to ~1.7x.

v0.2
~~~~

1. ``zipcodetw.find`` is 8x faster now!
2. It has a better tokenizing logic; and
3. a better matching logic for sub-number now.
4. ``zipcodetw.find_zipcodes`` was removed.
5. Internal API was changed a lot.
6. The tests are better now.
