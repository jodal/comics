from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = '8-Bit Theater'
    language = 'en'
    url = 'http://www.nuklearpower.com/'
    start_date = '2001-03-02'
    history_capable_date = '2001-03-02'
    schedule = 'Tu,Th,Sa'
    time_zone = -6
    rights = 'Brian Clevinger'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        page_url = 'http://www.nuklearpower.com/%(year)s/%(month)d/%(day)s/episode/' % {
            'year': self.pub_date.year, 'month': self.pub_date.month, 'day': self.pub_date.day
        }

        page = LxmlParser(page_url)
        self.url = page.src('img[src^="http://www.nuklearpower.com/comics/"]')
        self.title = page.alt('img[src^="http://www.nuklearpower.com/comics/"]')
