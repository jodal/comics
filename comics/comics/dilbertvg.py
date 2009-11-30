from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Dilbert (vg.no)'
    language = 'no'
    url = 'http://www.vg.no/dilbert/'
    start_date = '1989-04-16'
    history_capable_days = 1
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Scott Adams'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        self.url = 'http://www.vg.no/grafikk/dilbert/dilbert-%(date)s.gif' % {
            'date': self.pub_date.strftime('%Y-%m-%d'),
        }
