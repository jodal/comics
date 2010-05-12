.. _spec-public-active-schedule:

Spec-005: Unit Test and Refactoring of Navigation
=================================================================

*Spec created:*
    2010-05-02
*Spec implemented:*
    N/A


This spec is still under development as we more fully understand the final goal
for implementation.

Impetus
-------

Currently, the navigation loading code is a pretty large hunk that's quite
confusing.  It also has some odd behavior in certain instances (not realizing
what day it is exactly, not pulling recent history properly).   This spec is to
keep track of the refactoring project to clean up this code, preferably with
backward compatibility.

Unit Tests
----------

To assist in refactoring the code, we need to fully develop unit tests to test
time functionality so it doesn't slip through regression.  When I figure out
exactly what should be covered in these tests, I'll put some specific items
here.

Refactoring
-----------

Once unit tests are done, the code has to be refactored into smaller, more
managable chunks.

- Write modules to handle Comics date representation and populating with
  directives rather than free-form primitives.

- Write a facade to perform typical operations to populate a date with
  commonly-requested URIs.

- Maintain backward compatibility with existing date APIs, either through
  direct usage or extension.
