Daily Comics (aka comics)
=========================

What is comics?
---------------

A Django application and library for aggregating web comics. Originally
developed for running http://comics.jodal.no/.


Is it legal?
------------

The code is legal. Copying and distributing some of the comics may not be.
Anyway nobody is making any money here, and the intention is having fun
developing software and reading comics.


Credits
-------

comics was created by Stein Magnus Jodal (stein.magnus@jodal.no), with comments
and input from numerous users.


License
-------

comics is licensed under the GNU General Public Licence version 2. See COPYING
for the full license.


Dependencies
------------

The deps are listed as Debian/Ubuntu package names:

- python (>=2.5, at least hashlib is new in 2.5)
- python-django (>=1.0), and the following sub-dependencies
	- python-psycopg or python-psycopg2
	- postgresql-X.Y (developed with 8.3)
	- cmemcache (from source, or alternatively python-memcache)
- python-feedparser
- python-beautifulsoup (Future dep. I want to replace SGMLParser with it.)


Additional dependencies for development
---------------------------------------

- python-pmock (for mocking in unit tests)
- python-coverage (for checking test coverage)
- debug_toolbar (for debugging, from
  http://code.google.com/p/django-debug-toolbar/)


Usage
-----

To run unit tests:

    ./manage.py test --settings=comics.settings_testing

To run unit tests with statement coverage:

    ./manage.py test --settings=comics.settings_coverage

To fetch new comic strips:

    ./manage.py crawlcomics

To import comics from an old disk archive:

    ./manage.py importcomics

Add ``--help'' to get further instructions.



TODO
----

A mostly unordered list of things to fix. Patches accepted.

- comics.crawler.crawlers.*:
  - Use comic week schedule to crawl less often on non-schedule days.
  - Use comics time zone to crawl the correct current date.
- comics.crawler.utils.webparser: Replace with BeautifulSoup.
- comics.common.utils.navigation: Unit test and refactor to a tree of OO
  classes instead of long complicated functions.

New features:
- Support multiple strips per comic per day. Some places were this is not
  supported, it is commented in the source.
- Replace "Top 10" default views with a stream of the most recently fetched
  comics. Consider not having alternative time frame views, but using regular
  pagination.


Further documentation
---------------------

Use the force, read the source.
