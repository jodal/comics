***********************
Development environment
***********************

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
formatted in the same way. To format code, use `ruff
<https://docs.astral.sh/ruff/>`_::

    ruff format .


Linting
=======

All code should be lint free, and PRs will only be accepted if they pass
linting. To check the code for code quality issues, use `ruff
<https://docs.astral.sh/ruff/>`_::

    ruff check .


Run it all
==========

To locally run all the same tests as GitHub Actions runs on each pull
request, use `tox <https://tox.readthedocs.io/>`_::

    tox
