from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

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
        self.web_url = 'http://www.countyoursheep.com/d/%(date)s.html' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
        self.parse_web_page()

        for image in self.web_page.imgs:
            if 'src' in image and image['src'].startswith('/comics/'):
                self.url = self.join_web_url(image['src'])
                return
