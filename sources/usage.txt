Usage
=====

To run unit tests::

    python manage.py test --settings=comics.settings.testing

To run unit tests with statement coverage::

    python manage.py test --settings=comics.settings.coverage

To load meta data for new or existing comics::

    python manage.py loadmeta

To fetch new comic strips::

    python manage.py getcomics

Add ``--help`` to any of the commands to get more options.
