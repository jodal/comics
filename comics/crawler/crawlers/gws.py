from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Girls With Slingshots'
    language = 'en'
    url = 'http://www.girlswithslingshot.com/'
    start_date = '2004-09-30'
    history_capable_days = 1
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5
    rights = 'Danielle Corsetto'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://www.daniellecorsetto.com/gws.html'
        self.parse_web_page()

        for img in self.web_page.imgs:
            if 'src' in img and img['src'].startswith('images/gws/GWS'):
                self.url = self.join_web_url(img['src'])
                return
