Spec: Crawler meta data in Python code
======================================

*Spec created:*
    2009-06-13
*Spec implemented:*
    2009-07-18

Goals
-----

- Remove the need for patching common/fixtures/initial_data.json when adding
  new comic crawlers.
- Everything needed for adding a new comic in one file.
- Automatic creation of a new Comic instance when adding a crawler.
- No adding of Comic instances before the matching crawler is in place.


Implementation plan
-------------------

1. Add a ComicMeta class in each crawler module containing the information
   previously added as fixtures.
2. Add a management command 'loadcomicmeta' which reads the ComicMeta classes
   and adds new Comic instances to the database.
   - Let the user specify which crawlers to add with '-c comicslug'.
3. Add ComicMeta to all existing crawlers.
4. Remove common/fixtures/initial_data.json.
5. As a bonus, add support for merging ComicMeta changes into the database.
