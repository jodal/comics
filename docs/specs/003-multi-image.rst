.. _spec-multi-image:

Spec-003: Multiple images per comic release
===========================================

*Spec created:*
    2009-12-14
*Spec implemented:*
    N/A


Goals
-----

- Some comic releases consists of multiple images. The goal is to change
  *comics*' data model to support this.


Implementation plan
-------------------

1. [done, 2009-01-03] Change naming scheme for image files from date to
   checksum.
2. Rename ``Strip`` to ``Image``.
3. Replace the ``Release.strip`` foreign key with a many-to-many relation to
   ``Image``.
4. Consider removing the foreign key ``Release.comic`` and instead infer it
   from the ``Image`` relation.
5. Update aggregator to support multiple ``CrawlerResult`` from one
   ``crawl()``.
6. Update web view and feed view accordingly.
