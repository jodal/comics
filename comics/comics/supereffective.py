import datetime as dt

from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Super Effective'
    language = 'en'
    url = 'http://www.vgcats.com/super/'
    start_date = '2008-04-23'
    history_capable_date = '2008-04-23'
    time_zone = -5
    rights = 'Scott Ramsoomair'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.vgcats.com/super/images/%(date)s.gif' % {
            'date': self.pub_date.strftime('%y%m%d'),
        }
