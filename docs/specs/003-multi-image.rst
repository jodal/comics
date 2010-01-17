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

1. [done, 2010-01-03] Change naming scheme for image files from date to
   checksum.
2. [done, 2010-01-04] Rename ``Strip`` to ``Image``.
3. [done, 2010-01-05] Replace the ``Release.image`` foreign key with a
   many-to-many relation to ``Image``.
4. [done, 2010-01-05] Update web view and feed view to support multiple images
   per release.
5. [done, 2010-01-17] Update aggregator to support multiple images per release.
6. Update docs on how to create crawlers.
