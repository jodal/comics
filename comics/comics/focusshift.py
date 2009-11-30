import re

from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Focus Shift'
    language = 'en'
    url = 'http://www.osnews.com/comics/'
    start_date = '2008-01-27'
    history_capable_date = '2008-01-27'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Thom Holwerda'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        pass # XXX Comic no longer published
