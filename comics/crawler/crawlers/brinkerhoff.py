from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Brinkerhoff'
    language = 'en'
    url = 'http://www.brinkcomic.com/'
    start_date = '2006-01-02'
    history_capable_date = '2006-01-02'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5
    rights = 'Gabe Strine'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.brinkcomic.com/comics/%(date)s.gif' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }

    def _get_headers(self):
        return {
            'Referer': 'http://www.brinkcomic.com/d/%(date)s/' % {
                'date': self.pub_date.strftime('%Y%m%d'),
            }
        }
