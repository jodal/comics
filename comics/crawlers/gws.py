from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = 'Girls With Slingshots'
    language = 'en'
    url = 'http://www.girlswithslingshots.com/'
    start_date = '2004-09-30'
    history_capable_days = 1
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5
    rights = 'Danielle Corsetto'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://www.daniellecorsetto.com/gws.html'
        page = LxmlParser(self.web_url)
        self.url = page.src(
            'img[src^="http://www.daniellecorsetto.com/images/gws/GWS"]')
