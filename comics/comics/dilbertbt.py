from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Dilbert (bt.no)'
    language = 'no'
    url = 'http://www.bt.no/tegneserier/dilbert/'
    start_date = '1989-04-16'
    history_capable_date = '2005-10-28'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Scott Adams'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        pass # XXX Comic no longer published
