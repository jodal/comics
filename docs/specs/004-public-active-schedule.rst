.. _spec-public-active-schedule:

Spec-004: Add new database fields for public, active and schedule
=================================================================

*Spec created:*
    2010-03-03
*Spec implemented:*
    Partly, 2011-08-14


Goals
-----

- Add ``COMICS_PUBLIC`` setting to indicate if the installations is public
  or private. Default value should be should be ``True``. The proposed
  ``public`` field handling needs to respect this setting.

  Alternatively this setting can be avoided with ``loadmeta`` ignoring private
  comics by default (ie. add --include-private or only load private ones when
  explicitly specified).

- Add ``public`` field to Comic model that indicates if comic can be showed on
  public installations. All comics should have default value ``True`` and info
  loaded through ``loadmeta``.

  A design decision needs to be made with respect to if public installs should
  crawl "private" comics, the options are:

  a) Private comics are not loaded by ``loadmeta``.
  b) Load all comics, but hide private comics unless logged in.

- [done, 2011-08-14] Add ``active`` field to Comic model that can be used to
  indicate that a comic is no longer crawled. All comics should have default
  value ``True`` and info loaded through ``loadmeta``. The status page should
  ignore inactive comics.

- Add ``schedule`` field Comic model to track comic's schedule. This
  information will thus be moved from the crawler to the comic instance in the
  DB and loaded with ``loadmeta``. Comics without a schedule should have
  ``None`` as schedule.  This change has been proposed in response to better
  use of the new status page.


Implementation plan
-------------------

1. Add new setting.
2. Add new fields using south.
3. Update base Meta object.
4. Move schedule from crawler to meta in all existing crawlers.
5. Update status page to use "new" schedule.
6. Remove old ``get_comic_schedule`` from utils.
7. Update crawler and/or view code to respect public flag.
8. [done, 2011-08-14] Update crawler and/or view code to respect active flag.
9. Update docs if required.
