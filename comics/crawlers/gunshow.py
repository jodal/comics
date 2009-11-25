from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

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
        self.parse_web_page()

        for img in self.web_page.imgs:
            if 'src' in img and img['src'].startswith('/comics/'):
                self.url = self.join_web_url(img['src'])
                return
