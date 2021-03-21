***********
Development
***********

Comics development is coordinated through `GitHub
<http://github.com/jodal/comics/>`_.


Testing
=======

Comics got some tests, but far from full test coverage. If you write new or
improved tests for Comics' functionality it will be greatly appreciated

You can run the tests with `pytest <https://docs.pytest.org/>`_::

    pytest

To check test coverage, run with ``--cov``::

    pytest --cov


Code formatting
===============

All code is autoformatted, and PRs will only be accepted if they are
formatted in the same way. To format code, use `Black
<https://black.readthedocs.io/>`_::

    black .


Linting
=======

All code should be lint free, and PRs will only be accepted if they pass
linting. To check the code for code quality issues, use `flake8
<https://flake8.pycqa.org/>`_::

    flake8


Run it all
==========

To locally run all the same tests as GitHub Actions runs on each pull
request, use `tox <https://tox.readthedocs.io/>`_::

    tox
