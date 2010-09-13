*******
Changes
*******

This change log is used to track all major changes to *comics* after the first
versioned release.


In development
==============

**Bugfixes**

- Catch :exc:`socket.error` in :meth:`CrawlerBase.get_crawler_release()`.

**Crawlers**

- New: ``stuffnoonetoldme``
- Update ``gunshow`` to work after source site changes.


1.0.3 (2010-07-26)
==================

Another minor release bringing 17 new and 11 updated crawlers.

**Bugfixes**

- Make crawlers handle :exc:`httplib.BadStatusLine` exception raised when HTTP
  responses are empty.
- Make crawlers convert :class:`lxml.etree._ElementUnicodeResult` to unicode
  objects before saving to the database, to avoid ``DatabaseError: can't
  adapt`` errors.
- Handle MIME types like ``image/jpeg, image/jpeg`` returned by
  :class:`mimetools.Message.gettype`.
- Use :attr:`Crawler.headers` for image requests, and not just page requests.

**Crawlers**

- New: ``apokalips``
- New: ``axecop`` (fixes GH-8)
- New: ``boxerhockey``
- New: ``bugcomic`` (fixes GH-11)
- New: ``carpediem``
- New: ``crfh``
- New: ``darylcagle``
- New: ``havet`` (fixes GH-7)
- New: ``heltnils``
- New: ``intelsinsides`` (fixes GH-9)
- New: ``misfile`` (fixes GH-3)
- New: ``notinventedhere`` (fixes GH-4)
- New: ``pondusno``
- New: ``radiogaga``
- New: ``scenesfromamultiverse`` (fixes GH-10)
- New: ``sheldon``
- New: ``thegutters``
- Update ``8bittheater`` which is no longer published.
- Update ``brinkerhoff`` which is no longer published.
- Update ``ctrlaltdelete`` to work after source site changes.
- Update ``ctrlaltdeletesillies`` to work after source site changes.
- Update ``dieselsweetiesweb`` to work after source site changes.
- Update ``eon`` with new source site.
- Update ``lunch`` with new source site.
- Update ``sometingpositive`` to get all releases.
- Update ``supereffective`` to work after source site changes.
- Update ``vgcats`` to work after source site changes.
- Update ``yafgc`` to work after source site changes.


1.0.2 (2010-04-11)
==================

A minor release to get crawler updates out there. Two new cool but partly
immature features are included, as they do not affect existing features or
change database schema.

**Features**

- Add status page which for each comic shows when releases are fetched compared
  to the comic's release schedule. Contributed by Thomas Adamcik.
- Add support for search in comic's title and text fields, using Haystack.
  Contributed by Thomas Adamcik.

**Crawlers**

- New: ``atheistcartoons``
- New: ``petpeevy``
- Update ``evilinc`` to work again.
- Update ``uvod`` to fetch comment too.
- Update ``gunshow`` to fetch multiple images per release.
- Update ``questionablecontent`` to work again.
- Update ``basicinstructions`` to ignore QR Code.
- Update ``partiallyclips`` with new feed URL.
- Update ``somethingpositive`` with new image URL.
- Update ``spikedmath`` to fetch multiple images per release.


1.0.1 (2010-02-23)
==================

This release features 17 new crawlers and three updated crawlers, most by
*comic*'s new contributor Jim Wyllie. Let's get more of those!

**Features**

- Add links to official sites via redirect page.
- Add :class:`comics.aggregator.crawler.GoComicsComCrawlerBase` for fast
  gocomics.com crawler creation.
- Add ``headers`` argument to :class:`comics.aggregator.lxmlparser.LxmlParser`
  for adding HTTP headers to requests it makes.
- Add time since last release to ``release-list`` and ``comic-list``.

**Crawlers**

- New: ``babyblues``
- New: ``calamitiesofnature``
- New: ``charliehorse``
- New: ``fminus``
- New: ``forbetterorforworse``
- New: ``girlgenius``
- New: ``hijinksensue``
- New: ``joelovescrappymovies``
- New: ``magpieluck``
- New: ``nonsequitur``
- New: ``overcompensating``
- New: ``pluggers``
- New: ``tankmcnamara``
- New: ``theboondocks``
- New: ``thedreamer``
- New: ``wondermark``
- New: ``yehudamoon``
- Update ``playervsplayer`` to not miss comics on days with blog posts.
- Update ``questionablecontent`` to include text below image.
- Update ``kalscartoon`` after target site change.
- Update ``butternutsquash`` after target site change.


1.0.0 (2010-01-27)
==================

A week has gone, and here is the 1.0.0 final release. Enjoy :-)

**Crawlers**

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
