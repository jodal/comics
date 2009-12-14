Spec: Multiple images per release
=================================

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

1. Rename ``Strip`` to ``Image``.
2. Move ``title`` and ``text`` from ``Image`` to ``Release``.
3. Replace the ``Release.strip`` foreign key with a many-to-many relation to
   ``Image``.
4. Update aggregator, web view and feed view accordingly.
