from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Ctrl+Alt+Del'
    language = 'en'
    url = 'http://www.ctrlaltdel-online.com/'
    start_date = '2002-10-23'
    history_capable_date = '2002-10-23'
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Tim Buckley'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        self.url = 'http://www.cad-comic.com/comics/%(date)s.jpg' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
