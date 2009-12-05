Todo
====

A mostly unordered list of things to fix. Patches accepted.


Improvements
------------

- comics.comics.pennyarcade:
  Move web page string decoding to comics.aggregator.lxmlparser.
- comics.aggregator.crawler._decode_feed_data():
  Move feed string decoding to comics.aggregator.feedparser/lxmlparser.
- comics.aggregator.crawler._get_date_to_crawl():
  Use comics time zone to crawl the correct current date.
- comics.aggregator.command:
  Use comic week schedule to crawl less often on non-schedule days.
- comics.core.utils.navigation:
  Unit test and refactor.


New features
------------

- Support multiple strips per comic per day, which requires:
    - Change of naming scheme for image files from date to checksum.
    - Optionally support for returning multiple CrawlerResults from one crawl().
