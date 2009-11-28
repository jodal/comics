from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = 'Gun Show'
    language = 'en'
    url = 'http://www.gunshowcomic.com/'
    start_date = '2008-09-04'
    history_capable_date = '2008-09-04'
    schedule = 'Mo,Tu,We,Th,Fr'
    rights = '"Lord KC Green"'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://www.gunshowcomic.com/d/%(date)s.html' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
        page = LxmlParser(self.web_url)
        self.url = page.src('img[src^="http://www.gunshowcomic.com/comics/"]')
