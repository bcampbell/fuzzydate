=========
fuzzydate
=========

fuzzydate is a python date/time parsing library.

* tolerant of surrounding cruft (eg "Posted on jan 1st, 2010 at 8pm")

* handles common timezone abbreviations (BST, CET etc...)

* good at publication dates on web pages (eg news articles, blog posts)


Example interactive usage::

    >>> import fuzzydate
    >>> test_dt = 'Tuesday October 14 2008 00.01 BST'
    >>> fz = fuzzydate.parse_datetime(test_dt)

fz is a fuzzydate object where missing fields can be None (eg there are no seconds in this example)

    >>> print fz
    2008-10-14 0:1:None BST

convert it to a python datetime:

    >>> fz.datetime()
    datetime.datetime(2008, 10, 13, 23, 1)

parse_date() and parse_time() also return a span which indicates which part of the string was matched:

    >>> fz,span = fuzzydate.parse_date(test_dt)
    >>> span
    (0, 23)
    >>> fz,span = fuzzydate.parse_time(test_dt)
    >>> span
    (24, 33)

Why not dateutil?
* TODO


