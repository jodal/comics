# encoding: utf-8

from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Butternutsquash'
    language = 'en'
    url = 'http://www.butternutsquash.net/'
    start_date = '2003-04-16'
    history_capable_date = '2003-04-16'
    rights = 'Ramón Pérez & Rob Coughler'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.butternutsquash.net/comics/%(date)s.jpg' % {
            'date': self.pub_date.strftime('%Y-%m-%d'),
        }
