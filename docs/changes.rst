*******
Changes
*******

This change log is used to track all major changes to *comics* after the first
versioned release.


v2.4.0 (UNRELEASED)
===================

- Dependencies with new minimum versions:

  - Django >= 1.7, < 1.8
  - django-tastypie >= 0.12, < 0.13

- Dependencies with new maximum versions:

  - Pillow >= 1.7, < 2.7

- Removed dependencies:

  - South

- Switched the database migrations from using South to the builtin tool in
  Django 1.7. Due to this, all old database migrations have been thrown away.
  If you're running an old version of *comics*, please upgrade to the latest
  v2.3.x release first to get your database entirely up to date, then upgrade
  to v2.4.x. There are no database changes between v2.3.x and v2.4.x.


v2.3.4 (UNRELEASED)
===================

**Crawlers**

- New: ``lunarbaboon``
- Update ``zits`` to fetch from better source.
- Update ``nerfnow`` after feed change.


v2.3.3 (2014-10-06)
===================

**Crawlers**

- New: ``nerdrage``
- Update lots of comic release schedules.
- Update: ``drmcninja`` after feed change.
- Update: ``harkavagrant`` after site change.
- Update: ``hijinksensue`` to fetch large images.
- Update: ``lookingforgroup`` to not fetch unrelated comics.
- Update: ``nedroid`` after feed change.
- Update: ``pennyarcade`` to work around User-Agent check.
- Update: ``pidjin`` to ignore repeated image.
- Update: ``redmeat`` after site change.
- Update: ``subnormality`` after page change.
- Update: ``wondermark`` after feed change.
- Inactive: ``marriedtothesea``
- Inactive: ``pelsogpoter``
- Inactive: ``threewordphrase``
- Inactive: ``toothpastefordinner``
- Inactive: ``virtualshackles``


v2.3.2 (2014-09-11)
===================

- Dependencies with new maximum versions:

  - django_compressor >= 1.1, < 1.5
  - Pillow >= 1.7, < 2.6

- Add crawler status page to the menu.

- Fix position of "Add to my comics" button.

- Make an attempt at fixing downloading of image URLs with non-ASCII chars in
  the URL.

**Crawlers**

- New: ``blasternation``
- New: ``cardboardcrack``
- New: ``commitstrip``
- New: ``lunche24``
- New: ``q2qcomics``
- Update: ``asofterworld`` after site change.
- Update: ``doghouse`` after feed change.
- Update: ``joyoftech`` after site change.
- Update: ``kiwiblitz`` after site change.
- Update: ``seemikedraw`` after site move.
- Update: ``thegamercat`` after feed change.
- Update: ``walkoflife`` is no longer published.


v2.3.1 (2014-06-11)
===================

- Display error message instead of crashing if a password reset link is reused.

**Crawlers**

- New: ``iamarg``
- Update: ``asofterworld`` after feed breakage.
- Update: ``crookedgremlins`` after feed removal.
- Update: ``darklegacy`` after site change.
- Update: ``hijinksensue`` after feed change.
- Update: ``lookingforgroup`` after feed change.
- Update: ``mutts`` after site change.
- Update: ``phd`` after feed change.
- Update: ``poledancingadventures`` after site change.
- Update: ``pcweenies`` after feed change.
- Update: ``playervsplayer`` after site change.
- Update: ``sinfest`` after site change.
- Update: ``stickydillybuns`` after delayed feed update.
- Update: ``yamac`` after site change.
- Inactive: ``antics``
- Inactive: ``boxerhockey``
- Inactive: ``dungeond``
- Inactive: ``eatthattoast``
- Inactive: ``gregcomic``
- Inactive: ``lunch``
- Inactive: ``pinkparts``
- Inactive: ``somethingofthatilk``
- Inactive: ``thechalkboardmanifesto``


v2.3.0 (2014-04-07)
===================

- Dependencies with new minimum versions:

  - Django >= 1.6, < 1.7
  - django-boostrap-form >= 3.1, < 3.2

- Dependencies with new maximum versions:

  - cssmin >= 0.1, < 0.3
  - cssselector >= 0.8, < 0.10
  - django-tastypie >= 0.9.13, < 0.12
  - Pillow >= 1.7, < 2.5

- Upgraded to Bootstrap 3, which gives way for a refreshed and more
  responsive/mobile friendly design.

- Upgraded to Font Awesome 4.

- Upgraded to JQuery 2. IE6/7/8 are no longer supported. IE9 is the oldest IE
  version you can expect to work with *comics*.

- Moved comics list from bottom of each page to its own page in the top menu.
  This makes it more available on mobile clients, as well as to new users that
  don't know where to find the list after they've subscribed to their first
  comic.

- Use Moment.js to show time since fetched timestamp in release meta data.
  This can't be done on the server side due to heavy caching.


v2.2.3 (2014-03-31)
===================

- Make ``num_releases_since/:id`` view return 404 instead of 500 for unknown
  release IDs.

**Crawlers**

- New: ``adam4d``
- New: ``poorlydrawnlines``
- Update: ``lookingforgroup`` after feed change.
- Update: ``pennyarcade`` after site change.
- Update: ``questionablecontent`` after site change.
- Update: ``satw`` to include description text.


v2.2.2 (2013-12-21)
===================

**Crawlers**

- Update many comic schedules
- Update: ``hijinksensue`` after feed change.
- Update: ``partiallyclips`` to save larger image.
- Update: ``scenesfromamultiverse`` after feed change.
- Update: ``toothpastefordinner`` after feed change.


v2.2.1 (2013-11-08)
===================

- **Security:** Disabled the GZip middleware to help prevent the BREACH attack.
  See https://www.djangoproject.com/weblog/2013/aug/06/breach-and-django/ for
  details.

- The feedback form no longer uses the logged in user's email address as the
  sender address as this can cause the mail to be rejected due to sender
  validation and similar anti spam measures. The user's email is still in the
  email signature and is now also in the mail's ``Reply-To`` header.

- The status page now sorts comics by the number of days since the last
  release, moving the comics most in need of maintenance to the top of the
  page.

**Crawlers**

- New: ``pinkparts``
- New: ``poledancingadventures``
- New: ``redmeat``
- New: ``seemikedraw``
- Update: ``amazingsuperpowers`` after feed change.
- Update: ``axecop`` after feed change.
- Update: ``bugcomic`` after site change.
- Update: ``chainsawsuit`` after feed change.
- Update: ``crookedgremlins`` after site change.
- Update: ``cyanideandhappiness`` schedule.
- Update: ``evilinc`` after site change.
- Update: ``fanboys`` after feed change.
- Update: ``gregcomic`` after site change.
- Update: ``gucomics`` after feed change.
- Update: ``harkavagrant`` after feed change.
- Update: ``heijibits`` after addition of User-Agent check.
- Update: ``hjinksensue`` after feed change.
- Update: ``joyoftech`` after feed change.
- Update: ``icanbarelydraw`` after addition of User-Agent check.
- Update: ``kalscartoon`` after addition of User-Agent check.
- Update: ``kiwiblitz`` after feed change.
- Update: ``lunch`` to use feed.
- Update: ``marriedtothesea`` after feed change.
- Update: ``menagea3`` after site change and delayed feed update.
- Update: ``mysticrevolution`` after site change.
- Update: ``nedroid`` after feed change.
- Update: ``optipess`` to add related text.
- Update: ``pidjin`` after site change.
- Update: ``questionablecontent`` after site change.
- Update: ``reallife`` after feed change.
- Update: ``sheldon`` after site change.
- Update: ``shortpacked`` after site change.
- Update: ``stickydillybuns`` to use site feed and include title.
- Update: ``thegamercat`` after addition of User-Agent check.
- Update: ``thegutters`` after feed change.
- Update: ``wulffmorgenthaler`` after site change.
- Inactive: ``picturesforsadchildren``
- Inactive: ``radiogaga``
- Inactive: ``reveland``


v2.2.0 (2013-07-07)
===================

- New dependencies, and dependencies with new minimum versions:

  - cssselect >= 0.8, < 0.9
  - Django >= 1.5, < 1.6
  - django-tastypie >= 0.9.13, < 0.10
  - lxml >= 3, < 4
  - defusedxml >= 0.4, < 0.5

- Dependencies with new maximum versions:

  - django_compressor >= 1.1, < 1.4
  - Pillow >= 1.7, < 2.2
  - South >= 0.7, < 2.0

- Fix crash in importing of old comic sets, which has been broken since v2.1.0.

**Crawlers**

- New: ``20px``
- New: ``completelyseriouscomics``
- New: ``hjalmar``
- New: ``kollektivet``
- New: ``tommyogtigern``
- New: ``truthfacts``
- New: ``wumovg``
- Update: ``amazingsuperpowers`` after feed change.
- Update: ``antics`` after feed change.
- Update: ``beyondthetree`` is no longer published.
- Update: ``chainsawsuit`` after feed change.
- Update: ``choppingblock`` is no longer published.
- Update: ``darylcagle`` after feed change.
- Update: ``dilbert`` after removal of feed.
- Update: ``dilbertvg`` after move to new site.
- Update: ``eatthattoast`` to not throw exception when the site is broken.
- Update: ``eon`` is no longer published.
- Update: ``evilinc`` to be more robust.
- Update: ``exiern`` to track new storyline.
- Update: ``extralife`` after feed change.
- Update: ``extraordinary`` after site change.
- Update: ``fagprat`` after site change.
- Update: ``geekandpoke`` after feed change.
- Update: ``gws`` after site change.
- Update: ``harkavagrant`` schedule.
- Update: ``havet`` is no longer published.
- Update: ``hejibits`` schedule.
- Update: ``heltnils`` is no longer published.
- Update: ``hipsterhitler`` is no longer published.
- Update: ``kiwiblitz`` schedule.
- Update: ``kukuburi`` is no longer published.
- Update: ``leasticoulddo`` after site change.
- Update: ``manalanextdoor`` is no longer published.
- Update: ``manlyguys`` after feed change.
- Update: ``orneryboy`` is no longer published.
- Update: ``overcompensating`` is no longer published.
- Update: ``perrybiblefellowship`` to be an active crawler again.
- Update: ``picturesforsadchildren`` is no longer published.
- Update: ``pidjin`` to ignore repeated non-comic image.
- Update: ``reallife`` after site change.
- Update: ``sheldon`` schedule.
- Update: ``slagoon`` after site change.
- Update: ``smbc`` after site change.
- Update: ``somethingofthatilk`` schedule.
- Update: ``subnormality`` to include title text.
- Update: ``thechalkboardmanifesto`` schedule.
- Update: ``thegamercat`` after feed change.
- Update: ``theidlestate`` is no longer published.
- Update: ``undeclaredmajor`` is no longer published.
- Update: ``utensokker`` is published again.
- Update: ``uvod`` after feed change.
- Update: ``veslemoy`` is no longer published.
- Update: ``whiteninja`` is no longer published.
- Update: ``wulffmorgenthaler`` to work after site change.
- Update: ``wulffmorgenthalerap`` is no longer active.
- Update: ``yehudamoon`` is no longer published.
- Update: ``zofiesverden`` is no longer published.


v2.1.1 (2013-02-26)
===================

**Crawlers**

- New: ``lunchtu``
- New: ``mutts``. Contributed by Anders Birkenes.
- New: ``pelsogpoter``. Contributed by Anders Birkenes.
- New: ``stickygillybuns``
- New: ``undeclaredmajor``
- New: ``yamac``
- Update: ``abstrusegoose`` after feed change.
- Update: ``bizarro`` after feed change.
- Update: ``joyoftech`` after site change.
- Update: ``lookingforgroup`` after feed change.
- Update: ``thegamercat`` to be more robust.


v2.1.0 (2012-10-15)
===================

- Added a :doc:`webservice` interface to the *comics* instance's data to
  enable the development of custom frontends to *comics* and apps for Android
  and iOS.

- Improved admin interface. A lot of fields on the comic, release, and image
  models are now read-only, as they are only intended to be changed by the
  ``comics_addcomics`` and ``comics_getreleases`` commands. The comics admin
  interface is mainly intended for browsing and deleting
  comics/releases/images, not changing.

- Proper time zone support for comics crawling. We now calculate the current
  date at the location a comic is published using time zone aware datetime
  objects for the current time, which are converted to the comic's local time
  zone using ``pytz``.

- Removed the setting ``COMICS_DEFAULT_TIME_ZONE``.

- Updated time zone data for all crawlers. A lot of releases will now be
  fetched an hour earlier during daylight savings time, which is now taken into
  consideration when crawling.


v2.0.1 (2012-10-06)
===================

- Add dependency on ``pytz``.
- Make conversion from publication date to epoch used by 11 crawlers aware of
  the time zone.
- Set sender of feedback emails to the email address of the logged in user.

**Crawlers**

- New: ``antics``
- New: ``beetlebailey``
- New: ``choppingblock``
- New: ``dungeond``
- New: ``dustin``
- New: ``exiern``
- New: ``pickles``
- Update: ``boxerhockey`` after site change.
- Update: ``exiern`` after site change.
- Update: ``gregcomic`` schedule.
- Update: ``havet`` with better time zone handling.
- Update: ``kiwiblitz`` after site change.
- Update: ``misfile`` after site change.
- Update: ``mysticrevolution`` to be more robust.
- Update: ``reveland`` with better time zone handling.
- Update: ``spikedmath`` to only fetch the correct images.
- Update: ``tehgladiators`` schedule.
- Update: ``thegamercat`` to fetch full size images.
- Update: ``virtualshackles`` schedule.
- Update: ``walkoflife`` with better time zone handling.
- Update: ``whattheduck`` schedule.
- Update: ``whiteninja`` schedule.
- Update: ``wulffmorgenthaler`` to fetch the previous day due to releases being
  delayed.
- Update: ``yehudamoon`` after site change.
- Update: ``zelda`` schedule.
- Update: ``zits`` after site change.


v2.0.0 (2012-06-11)
===================

Version 2 refreshes the entire *comics* web interface. The aggregation part
of *comics* is mostly unchanged since v1.1.

- Design: New design based on Twitter Bootstrap.

- User accounts:

  - Add user account registration flow, which includes email address
    verification, login, logout, password change, and password reset.

  - Add account management interface.

  - Add user information to footer of emails sent from the feedback page.

  - Require a user specific secret key to allow access to feeds. (Fixes:
    :issue:`25`)

  - Add support for requiring an invitation to register as a new user. Set the
    setting ``INVITE_MODE`` to ``True`` to require invitation before
    registration. (Fixes: :issue:`29`)

- "My comics":

  - Replace named comic sets with comic subscriptions associated with users,
    called "my comics". An importer for converting old comics sets to "my
    comics" is included. (Fixes: :issue:`26`, :issue:`27`)

  - Add buttons to all comic views for adding the comic to "my comics".

  - Extend comics list in the footer to include subscription management.
    (Fixes: :issue:`28`, :issue:`49`)

- Comics browsing:

  - Orders the "latest" view by fetched time instead of comic name. New content
    is always at the top. (Fixes: :issue:`13`)

  - Removes browsing of weeks or N days, with the exception of +1 days, which
    is kept as a "today" view.

  - Reimplemented lots of crusty old code using Django's class-based generic
    views.

  - Reimplement feeds using regular views instead of Django's feed abstraction
    to reduce the feed response time enough to not cause timeouts when using
    e.g. Netvibes to subscribe to feeds. (Fixes: :issue:`5`)

- Comics crawling:

  - Try to verify that image files are valid by loading them with PIL before
    saving them. (Fixes: :issue:`17`)

  - Use PIL instead of server provided MIME types to identify the image type.

  - Removed unused ``check_image_mime_type`` crawler setting.

  - Whitelist GIF, JPEG, and PNG files. All other file types are rejected.
    (Fixes: :issue:`16`)

  - Blacklisted the GoComics placeholder image.

- Development:

  - The WSGI file is now also used when using Django's ``runserver`` command
    while developing, making the development and deployment environments more
    alike.


v1.1 to v2.0 migration guide
----------------------------

- New dependencies:

  - django-registration >= 0.8, < 0.9

  - django-bootstrap-form >= 2.0, < 2.1

- Updated dependencies:

  - Django >= 1.4, < 1.5

  - django_compressor >= 1.1, < 1.2

- Settings:

  - Removed setting ``COMICS_SITE_TAGLINE``.

  - Replaced setting ``COMICS_MAX_DAYS_IN_PAGE`` with
    ``COMICS_MAX_RELEASES_PER_PAGE``.

  - Removed ``COMICS_MEDIA_ROOT`` and ``COMICS_MEDIA_URL``. As static files
    now are located under ``STATIC_ROOT`` and ``STATIC_URL``, the entire
    namespace under ``MEDIA_ROOT`` and ``MEDIA_URL`` are now available for
    downloaded media, e.g. crawled comics.

- Commands:

  - ``loadmeta`` is now called ``comics_addcomics``. It no longer defaults to
    adding all comics to your installation, but you must now specify ``-c all``
    to do so.

  - ``getcomics`` is now called ``comics_getreleases``

  Remember to update your cronjobs.

- Project layout:

  - Moved ``manage.py`` one level higher in the directory structure, to follow
    the new defaults in Django 1.4. Again, remember to update your cronjobs.

  - Moved file with WSGI application from ``wsgi/deploy.wsgi`` to
    ``comics/wsgi/__init__.py`` to follow the new default structure in Django
    1.4. Remember to update your web server configuration.

- As the comic sets functionality have been replaced, the app ``comics.sets``
  is no longer activated by default. If you're upgrading from comics v1.x and
  have existing sets in your database, you *should* activate the
  ``comics.sets`` app so that your users may import their old comic sets into
  their new user accounts. Add the following to your local settings file,
  ``comics/settings/local.py``::

      from comics.settings.base import INSTALLED_APPS
      INSTALLED_APPS += ('comics.sets',)

- Renamed :class:`MetaBase` to :class:`ComicDataBase`, and moved it to
  :mod:`comics.core.comic_data`. Remember to update any custom crawlers.

- Database changes:

  - The field :attr:`Comic.number_of_sets` have been removed as it is no longer
    used.  If you would want to rollback from 2.x to 1.x the data in this field
    can be regenerated, as it's only a denormalization of data available
    elsewhere.

  - The datetime field :attr:`Comic.added` has been added. It is automatically
    populated with a date in the far past upon database migration.

  - Added two new database indexes to the :class:`Release` model, which both
    help a lot towards making comics browsing faster. They will be
    automatically created on database migration.

  All of these changes can be automatically applied to your database. To do so,
  run::

      python manage.py syncdb --migrate


v1.1.6 (2012-06-10)
===================

**Bugfixes**

- :meth:`LxmlParser.text()` now returns an empty list if :attr:`allow_multiple`
  is :class:`True` and :attr:`default` is not specified. This is identical to
  how all other :class:`LxmlParser` selector methods already work.

**Crawlers**

- New: ``oatmeal``
- New: ``zelda``
- Update: ``abstrusegoose`` has a schedule.
- Update: ``apokalips`` is no longer published.
- Update: ``asofterworld`` after feed change.
- Update: ``atheistcartoons`` is no longer published.
- Update: ``axecop`` has a schedule.
- Update: ``basicinstructions`` has a new schedule.
- Update: ``bgobt`` is no longer published.
- Update: ``boasas`` is no longer published.
- Update: ``bunny`` is no longer published.
- Update: ``carpediem`` is no longer published.
- Update: ``countyoursheep`` is no longer published.
- Update: ``crfh`` after site change.
- Update: ``darklegacy`` does not follow a schedule.
- Update: ``devilbear`` does not follow a schedule.
- Update: ``dieselsweetiesweb`` to be more robust to missing elements in the
  feed.
- Update: ``goblins`` does not follow a schedule.
- Update: ``gunshow`` has a new release schedule.
- Update: ``hijinksensue`` after feed change.
- Update: ``icanbarelydraw`` has a new release schedule.
- Update: ``kiwiblitz`` does not follow a schedule.
- Update: ``littlegamers`` does not follow a schedule.
- Update: ``m`` is no longer published.
- Update: ``magpieluck`` is no longer published.
- Update: ``pcweenies`` does not follow a schedule.
- Update: ``picturesforsadchildren`` after feed change.
- Update: ``radiogaga`` has a new release schedule.
- Update: ``rhymeswithwitch`` is no longer published.
- Update: ``spaceavalanche`` after feed change.
- Update: ``stuffnoonetoldme`` is no longer published.
- Update: ``subnormality`` got a sensible history capability.
- Update: ``tehgladiators`` does not follow a schedule.
- Update: ``theidlestate`` does not follow a schedule.
- Update: ``utensokker`` is no longer published.
- Update: ``uvod`` got an updated homepage address.
- Update: ``virtualshackles`` does not follow a schedule.
- Update: ``walkoflife`` does not follow a schedule.


v1.1.5 (2012-05-09)
===================

The regular crawler updates and a small bug fix.

**Bugfixes**

- Handle aggregated images with MIME type ``image/pjpeg`` as JPEG images
  instead of rejecting them.

**Crawlers**

- New: ``chainsawsuit``
- New: ``goblins``
- New: ``subnormality``
- Update: ``applegeeks`` was discontinued a long time ago.
- Update: ``applegeekslite`` was discontinued a long time ago.
- Update: ``calamitesofnature`` has been discontinued.
- Update: ``duelinganalogs`` was broken due to feed changes.
- Update: ``fagprat`` has a new schedule.
- Update: ``fanboys`` was broken due to feed changes.
- Update: ``heltnils`` has a new schedule.
- Update: ``hijinksensure`` was broken due to feed changes.
- Update: ``playervsplayer`` was broken due to feed changes.
- Update: ``pondus`` was broken due to a site change.
- Update: ``savagechickens`` has a new schedule.
- Update: ``theidlestate`` after site redesign and addition of a feed.
- Update: ``veslemoy`` has a new schedule.


v1.1.4 (2012-04-07)
===================

The regular crawler updates and a performance improvement.

**Bugfixes**

- Store only the name of recently used sets in the session, instead of full
  set objects. After applying this fix, you should either delete all existing
  sessions::

      $ python manage.py shell
      >>> from django.contrib.sessions.models import Session
      >>> Session.objects.all().delete()

  Or migrate the content of your existing sessions::

      $ python manage.py cleanup
      $ python manage.py shell

      # Then run the following Python script in the Python shell:

      from django.contrib.sessions.backends.db import SessionStore
      from django.contrib.sessions.models import Session
      store = SessionStore()
      for session in Session.objects.all():
          data = session.get_decoded()
          set_names = []
          for set in data.get('recent_sets', []):
              if hasattr(set, 'name'):
                  set_names.append(set.name)
              else:
                  set_names.append(set)
          data['recent_sets'] = set_names
          session.session_data = store.encode(data)
          session.save()
          print '.',

**Crawlers**

- New: ``kellermannen``
- New: ``manalanextdoor``
- New: ``thegamercat``
- New: ``walkoflife``
- Update ``darylcagle`` after feed change.
- Update ``playervsplayer`` after feed change.


v1.1.3 (2012-01-29)
===================

This release adds 9 new crawlers and updates 46 existing crawlers.

**Crawlers**

- New: ``beyondthetree``
- New: ``dresdencodak``
- New: ``extraordinary``
- New: ``gunnerkrigg``
- New: ``icanbarelydraw``. Contributed by Jim Frode Hoff.
- New: ``manlyguys``. Contributed by Jim Frode Hoff.
- New: ``menagea3``
- New: ``sequentialarts``
- New: ``somethingofthatilk``. Contributed by Jim Frode Hoff.
- Update ``amazingsuperpowers`` with new release schedule.
- Update ``billy`` which is no longer published.
- Update ``bizarro`` with new release schedule.
- Update ``bizarrono`` which is no longer published.
- Update ``boasas`` after site change.
- Update ``bgobt`` with new release schedule.
- Update ``buttersafe`` with new release schedule.
- Update ``calvinandhobbes`` after site change.
- Update ``carpediem`` after site change.
- Update ``darylcagle`` after site change.
- Update ``devilbear`` with new release schedule.
- Update ``eatthattoast`` after site change.
- Update ``eon`` after site change.
- Update ``extralife`` to be more robust.
- Update ``fanboys`` after site change.
- Update ``gregcomic`` with new release schedule.
- Update ``gucomics`` after site change.
- Update ``heltnils`` after site change.
- Update ``hipsterhitler`` after site change.
- Update ``kalscartoon`` after site change.
- Update ``lefthandedtoons`` with new release schedule.
- Update ``loku`` which is no longer published.
- Update ``m`` with new release schedule.
- Update ``mortenm`` which is no longer published.
- Update ``mysticrevolution`` after site change.
- Update ``nemibt`` with new release schedule.
- Update ``nerfnow`` with new release schedule.
- Update ``optipess`` with new release schedule.
- Update ``orneryboy`` with new release schedule.
- Update ``pidjin`` after site change.
- Update ``pondusno`` which is no longer published.
- Update ``questionablecontent`` to be more robust.
- Update ``radiogaga`` after site change.
- Update ``reallife`` with new release schedule.
- Update ``reveland`` with new release schedule.
- Update ``romanticallyapocalyptic`` to be more robust.
- Update ``savagechickens`` with new release schedule.
- Update ``sheldon`` with new release schedule.
- Update ``somethingpositive`` after site change.
- Update ``stickycomics`` after site change.
- Update ``tehgladiators`` after site change.
- Update ``thedreamer`` with new release schedule.
- Update ``threewordphrase`` to be more robust.
- Update ``utensokker`` with new release schedule.
- Update ``wulffmorgenthalerap`` after site change.
- Update ``yehudamoon`` with new release schedule.


v1.1.2 (2011-09-18)
===================

A couple of bugfixes easing the transition from 1.0.x to 1.1.x by jwyllie83,
and some new crawlers.

**Bugfixes**

- Updated South requirement to v0.7, which is needed to support the last
  migration introduced by comics v1.1.0.

- If you use WSGI, you can now add a file ``wsgi/local.py`` based off of
  ``wsgi/local.py.template`` to set local settings for WSGI, like the use of
  ``virtualenv`` and debugging settings. This removes the need for changing Git
  tracked files, like ``deploy.wsgi`` for adding e.g. ``virtualenv`` support.

**Crawlers**

- New: ``buttersafe``
- New: ``doghouse``
- New: ``eatthattoast``
- New: ``hejibits``
- New: ``optipess``
- New: ``savagechickens``
- New: ``threewordphrase``
- New: ``timetrabble``
- Update ``pennyarcade`` after site change.


v1.1.1 (2011-08-22)
===================

Some fixes a week after the v1.1 feature release.

**Bugfixes**

- Fix missing whitespaces on about page after HTML minification.
- Add missing CSRF token to feedback form.

**Crawlers**

- Update ``asofterworld`` to work after feed change.


v1.1.0 (2011-08-15)
===================

- New/upgraded requirements:

  - Django 1.3
  - django_compressor
  - cssmin
  - jsmin

- Page speed improvements:

  - CSS and JavaScript is now merged and minified.
  - HTML is minified.
  - Optional Google Analytics code is upgraded to the asynchronous version.
  - All icons have been replaced with sprites to reduce number of elements that
    must be downloaded.

- Slightly refreshed graphical design.

- The "all comics" list at the bottom of the page have been changed from a
  cloud to lists in four columns.

- The optional comic meta data search functionality have been removed.

- Better handling of inactive comics:

  - Add ``active`` flag to comics.
  - Marked no longer published comics as inactive.
  - Inactive comics are no longer loaded by the ``loadmeta``  command unless
    explicitly specified by name or they have been previously loaded. In other
    words, inactive comics will not automatically be included in new
    installations.
  - Inactive comics are no longer included in the top 10 on the front page.
  - Inactive comics are now marked in the comics list on the bottom of all
    pages.
  - Inactive comics are now marked in the comics list page.
  - Inactive comics are now excluded from the set edit form, effectively
    removing them from the set on save.


v1.0.x to v1.1.x migration guide
--------------------------------

Ordered steps for syncronizing your v1.0.x installation with v1.1.0. You
should perform them in order.

**Using virtualenv**

If you choose to use ``virtualenv`` keeping all of comics' dependencies
sandboxed, be sure to activate the environment both in your cronjob and when
manually executing ``manage.py``::

    source <path_to_virtualenv>/bin/activate
    python manage.py getcomics

If you use WSGI, the WSGI file must be modified to support ``virtualenv``. See
the source code for how the bundled WSGI file solves this.

**New dependencies**

There are several new dependencies. All of them are listed in the file
``requirements.txt`` and may be installed using ``pip``, optionally inside a
``virtualenv``::

    pip install -r requirements.txt

To avoid compiling dependencies which are not pure Python and thus requires the
installation of various C libraries and Python's development packages, it may
be wise to use your distribution's package manger for some packages, like
``lxml`` and ``PIL``. E.g. on Ubuntu I would install the dependencies like
this::

    sudo apt-get install python-lxml python-imaging
    pip install -r requirements.txt

This way, ``lxml`` and ``PIL`` are installed from APT, and ``pip`` installs the
remaining pure Python dependencies.

**Settings changes**

Database settings now use the new `Django 1.2 format
<https://docs.djangoproject.com/en/dev/releases/1.2/#specifying-databases>`_.
See ``comics/settings/base.py`` for the new default setting and use it as an
example for porting your ``comics/settings/local.py`` settings file.

**Database migration**

A new database field has been added. To migrate your database to work with
v1.1.0, run::

    python manage.py migrate

.. warning ::

    You need South v0.7 or later to perform the database migration.

    comics v1.1.0's ``requirements.txt`` file only require South v0.6 or later.
    This is a bug, and the migration will not work if you're using South
    v0.6.x.

**Static files  collection**

We now use Django's new static files system. After installing you need to
"collect" your static files. See :ref:`collecting-static-files` for how to do
this.


v1.0.8 (2011-08-10)
===================

Just new and updated crawlers.

**Crawlers**

- New: ``mysticrevolution``
- New: ``theidlestate``
- Update ``havet`` to work after feed removal.
- Update ``reveland`` to work after feed removal.
- Update ``thechalkboardmanifesto`` to work after feed change.
- Update ``utensokker`` to work after feed removal.
- Update ``whattheduck`` schedule.


v1.0.7 (2011-07-13)
===================

Just new and updated crawlers.

**Crawlers**

- New: ``fagprat``
- New: ``gregcomic``
- New: ``satw``
- New: ``shortpacked``
- New: ``stickycomics``
- New: ``tehgladiators``
- Update ``betty`` which has moved from comics.com to gocomics.com.
- Update ``bizarro`` which moved to a new site.
- Update ``brandondraws`` which is no longer published.
- Update ``countyoursheep`` after URL changes.
- Update ``darylcagle`` after change from GIF to JPEG.
- Update ``faktafraverden`` which is no longer published.
- Update ``fminus`` which has moved from comics.com to gocomics.com.
- Update ``getfuzzy`` which has moved from comics.com to gocomics.com.
- Update ``lookingforgroup`` after feed change.
- Update ``m`` as it moved from start.no to dagbladet.no.
- Update ``nemibt`` to work after site change.
- Update ``nerfnow`` which crashed when it did not find an image URL.
- Update ``peanuts`` which has moved from comics.com to gocomics.com.
- Update ``pearlsbeforeswine`` which has moved from comics.com to gocomics.com.
- Update ``pondusbt`` after URL changes.
- Update ``rockybt`` to work after site change.
- Update ``romanticallyapocalyptic`` to use web page instead of feed.
- Update ``roseisrose`` which has moved from comics.com to gocomics.com.
- Update ``treadingground`` to not crash if URL is not found.
- Update ``threadingground`` which is no longer published.
- Update ``yehudamoon`` which was broken by addition of new images.
- Update ``zits`` with new feed URL.
- Update generic GoComics.com crawler to also support larger Sunday issues.


v1.0.6 (2011-02-19)
===================

The 1.0.6 release includes two bugfixes, five new crawlers, and many updated
crawlers. Also, most crawler schedules have been updated to make the status
page more useful.

**Bugfixes**

- :class:`comics.aggregator.lxmlparser.LxmlParser` methods now returns an empty
  list if ``allow_multiple`` is :class:`True` and no value is given for
  ``default``. This ensures that using the return value in for loops will not
  fail if no matches are found.

- :meth:`comics.aggregator.crawler.CrawlerBase.get_crawler_release` does no
  longer create empty releases if the ``do_crawl`` method returns false values,
  like empty lists. It previously only stopped processing if ``do_crawl``
  returned :class:`None`.

- Remove ``safe`` filter from title text, and explicitly use ``escape``, even
  though they should be implicitly escaped. Thanks to XKCD #859.

**Crawlers**

- A lot of comic release schedule updates.
- New: ``nerfnow``
- New: ``romanticallyapocalyptic``
- New: ``schlockmercenary``
- New: ``spaceavalanche``
- New: ``treadingground``
- Update ``butternutsquash`` which is no longer published.
- Update ``charliehorse`` which is no longer published.
- Update ``garfield`` to include Sunday editions.
- Update ``hipsterhitler`` to work after feed change.
- Update ``idiotcomics`` which is no longer published.
- Update ``inktank`` which is no longer published.
- Update ``intelsinsides`` which is no longer published.
- Update ``kiwiblitz`` to work after feed change.
- Update ``lifewithrippy`` which is no longer published.
- Update ``pcweenies`` to work after feed change.
- Update ``petpeevy`` which is no longer published.
- Update ``smbc`` to work after feed change.
- Update ``superpoop`` which is no longer published.
- Update ``thegutters`` to use feed instead of broken page parser.
- Update ``threepanelsoul`` to work after feed change.
- Update ``userfriendly`` to support reruns.
- Update ``wulffmorgenthaler`` to work after site change.


v1.0.5 (2010-12-29)
===================

A couple of bugfixes, and new and updated crawlers.

**Bugfixes**

- Do not throw :exc:`ParserError` in :mod:`comics.aggregator.lxmlparser` when
  the XML document is a all-space string.
- Catch :exc:`socket.error` in :mod:`comics.aggregator.downloader`, like we
  already do in :mod:`comics.aggregator.crawler`.

**Crawlers**

- New: ``brandondraws``
- New: ``crookedgremlins``
- New: ``faktafraverden``
- New: ``lunchdb``
- New: ``orneryboy``
- New: ``reveland``
- Update ``foxtrot`` crawler to work after site change.
- Update ``gws`` to work again, and add text parsing.
- Update ``havet`` meta data.
- Update ``lookingforgroup`` to ignore non-comic releases and fetch multiple
  pages released on the same day.
- Update ``magpieluck`` to handle titles without a dash.
- Update ``questionablecontent`` to not check if the page contains the expected
  date, as that make us lose some releases.
- Update ``utensokker`` to use RSS feed.


v1.0.4 (2010-10-23)
===================

Yet another minor release bringing a bug fix, four new and five updated
crawlers.

**Bugfixes**

- Catch :exc:`socket.error` in :meth:`CrawlerBase.get_crawler_release()`.

**Crawlers**

- New: ``hipsterhitler``
- New: ``marriedtothesea``
- New: ``stuffnoonetoldme``
- New: ``utensokker``
- Update ``boxerhockey`` to use feed instead of site.
- Update ``bugcomic`` to not fail if URL is not empty, and to work after source
  site changes.
- Update ``extralife`` to work after source site changes.
- Update ``gunshow`` to work after source site changes.
- Update ``questionablecontent`` to use site instead of feed, since it lacks
  some releases.


v1.0.3 (2010-07-26)
===================

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


v1.0.2 (2010-04-11)
===================

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


v1.0.1 (2010-02-23)
===================

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


v1.0.0 (2010-01-27)
===================

A week has gone, and here is the 1.0.0 final release. Enjoy :-)

**Crawlers**

- Update ``uvod`` crawler to use new feed.


v1.0.0.rc2 (2010-01-19)
=======================

Second release candidate for 1.0.0. Again, I will bump to 1.0.0 in a week if no
new issues arises.

**Bugfixes**

- Make ``core/0006`` migration work on the sqlite3 backend.


v1.0.0.rc1 (2010-01-17)
=======================

First release, so no list of changes. Will bump to 1.0.0 in a week if no issues
arise. Please report any problems at http://github.com/jodal/comics/issues.

Development on *comics* as a Python/Django project started in February 2007, so
this release has been almost three years in the making. Far too long, and I
promise it won't be three years until the next release.
