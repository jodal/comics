from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = 'Count Your Sheep'
    language = 'en'
    url = 'http://www.countyoursheep.com/'
    start_date = '2003-06-11'
    history_capable_date = '2003-06-11'
    schedule = 'Mo,Tu,We,Th,Fr'
    rights = 'Adrian "Adis" Ramos'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        page_url = 'http://www.countyoursheep.com/d/%(date)s.html' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
        page = LxmlParser(page_url)
        self.url = page.src('img[src^="http://www.countyoursheep.com/comics/"]')
