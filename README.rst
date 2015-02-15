.. image:: https://pypip.in/v/zipcodetw/badge.png?v=0.5.7
   :target: https://pypi.python.org/pypi/zipcodetw

.. image:: https://pypip.in/d/zipcodetw/badge.png?v=0.5.7
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
    u'1'
    >>> zipcodetw.find('臺北市信義區')
    u'110'
    >>> zipcodetw.find('臺北市信義區市府路')
    u'110'
    >>> zipcodetw.find('臺北市信義區市府路1號')
    u'11008'

After v0.3, you even can find ZIP code like:

.. code-block:: python

    >>> zipcodetw.find('松山區')
    u'105'
    >>> zipcodetw.find('秀山街')
    u''
    >>> zipcodetw.find('台北市秀山街')
    u'10042'

Installation
------------

It is available on PyPI:

.. code-block:: bash

    $ sudo pip install zipcodetw

Just install it and have fun. :)

Build Index Manually
--------------------

If you install it by ``pip`` or ``python setup.py install``, a ZIP code index
will be built automatically. But if you want to use it from source code, you
have to build an index manually:

.. code-block:: bash

    $ python -m zipcodetw.builder

Data
----

The ZIP code directory is provided by Chunghwa Post, and is available from:
http://www.post.gov.tw/post/internet/Download/all_list.jsp?ID=2201#dl_txt_s_A0206

Changelog
---------

v0.6
~~~~

1. Updated the data to 2014/12.

v0.5.7
~~~~~~

1. Fixed a rarely issue that causes IndexError.

v0.5.6
~~~~~~

1. Reverted removing insignificant tokens introduced in v0.5.4.
2. It now handles insignificant tokens; and
3. redundant units in the finding logic (``directory.find``).
4. Allowed number token ends without unit.
5. Now ``address.tokens`` is a list.

v0.5.5
~~~~~~

1. Fixed a gradual matching issue causing some wrong results.

v0.5.4
~~~~~~

1. Removed the token whose unit is insignificant automatically.

v0.5.3
~~~~~~

1. Fixed and simplified the matching logic for address tail.
2. Refined the index building logic.

v0.5.2
~~~~~~

1. Fixed the issue while it was running in multi-threaded environment.
2. Added a new argument, ``keep_alive``, for the ``Directory`` class.

v0.5.1
~~~~~~

1. Refined the code slightly.

v0.5
~~~~

1. It now builds a ZIP code index when you install it; so
2. the package size is 12.5x smaller.
3. The internal API is better now.

v0.4
~~~~

1. It now shipped with an index compiled in SQLite; so
2. initiation time is ~680x faster, i.e. ~30ms each import; and
3. ``zipcodetw.find`` is ~1.9x slower, i.e. ~2ms each call; and
4. has bigger package size.
5. All code was moved into ``zipcodetw`` package.
6. ``zipcodetw.find`` now returns unicode instead of string.

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
