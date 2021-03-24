# &#x1F5DE; Comics

_Comics is a webcomics aggregator._

[![CI](https://img.shields.io/github/workflow/status/jodal/comics/CI)](https://github.com/jodal/comics/actions?workflow=CI)
[![Docs](https://img.shields.io/readthedocs/comics)](https://comics.readthedocs.io/)
[![Coverage](https://img.shields.io/codecov/c/gh/jodal/comics)](https://codecov.io/gh/jodal/comics)

---

Comics is a webcomics aggregator. Out of the box it can crawl and archive
about two hundred comics every day. The comics are made available through an
easy to use web interface were users can build personalized collections of
their favorite comics, and then read them on the site or using a feed reader.

Adding a new comic to your installation requires only the addition of a single
Python file with some metadata and a few lines of code. To make crawler
development easy, Comics comes with both documentation and powerful APIs for
crawling web sites and feeds.

## Installation and usage

Comics runs on Python and Django. For instructions on how to install and use it, see [the documentation](https://comics.readthedocs.io/).

## Development status

The Comics project is almost as old as Django itself, with the code base
originating back to 2007. Currently, it is a bit stagnated, still running on
Django 1.11.

However, as of 2021, the project isn't entirely dead: the project maintainer
is still running his own instance with a number of regular users. There are
no immediate plans for any new features, but there is a
[roadmap](https://github.com/jodal/comics/projects/1) for getting Comics
up and running on Python 3 and the latest dependency releases, with a modern
and maintainable deployment setup.

## License

Comics is copyright 2009-2021 Stein Magnus Jodal and contributors.
Comics is licensed under the
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.en.html).
