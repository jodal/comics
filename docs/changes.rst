*******
Changes
*******

This change log is used to track all major changes to *comics* after the first
versioned release.


Unreleased
==========

**Features**

- New crawler: ``babyblues``
- New crawler: ``calamitiesofnature``
- New crawler: ``charliehorse``
- New crawler: ``fminus``
- New crawler: ``forbetterorforworse``
- New crawler: ``girlgenius``
- New crawler: ``hijinksensue``
- New crawler: ``joelovescrappymovies``
- New crawler: ``magpieluck``
- New crawler: ``nonsequitur``
- New crawler: ``overcompensating``
- New crawler: ``pluggers``
- New crawler: ``tankmcnamara``
- New crawler: ``theboondocks``
- New crawler: ``thedreamer``
- New crawler: ``wondermark``
- New crawler: ``yehudamoon``
- Add links to official sites via redirect page.
- Add ``GoComicsComCrawlerBase`` for fast gocomics.com crawler creation.
- Add ``headers`` argument to LxmlParser for HTTP requests it makes.

**Bugfixes**

- Update crawler ``playervsplayer`` to not miss comics on days with blog posts.
- Update crawler ``questionablecontent`` to include text below image.


1.0.0 (2010-01-27)
==================

A week has gone, and here is the 1.0.0 final release. Enjoy :-)

**Features**

- Update ``uvod`` crawler to use new feed.


1.0.0.rc2 (2010-01-19)
======================

Second release candidate for 1.0.0. Again, I will bump to 1.0.0 in a week if no
new issues arises.

**Bugfixes**

- Make ``core/0006`` migration work on the sqlite3 backend.


1.0.0.rc1 (2010-01-17)
======================

First release, so no list of changes. Will bump to 1.0.0 in a week if no issues
arise. Please report any problems at http://github.com/jodal/comics/issues.

Development on *comics* as a Python/Django project started in February 2007, so
this release has been almost three years in the making. Far too long, and I
promise it won't be three years until the next release.
