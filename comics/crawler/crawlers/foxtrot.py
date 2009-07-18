from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'FoxTrot'
    language = 'en'
    url = 'http://www.foxtrot.com/'
    start_date = '1988-04-10'
    history_capable_date = '2006-12-27'
    schedule = 'Su'
    time_zone = -5
    rights = 'Bill Amend'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://images.ucomics.com/comics/ft/%(year)s/ft%(date)s.gif' % {
            'year': self.pub_date.strftime('%Y'),
            'date': self.pub_date.strftime('%y%m%d'),
        }
