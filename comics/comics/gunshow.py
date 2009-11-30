from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Gun Show'
    language = 'en'
    url = 'http://www.gunshowcomic.com/'
    start_date = '2008-09-04'
    history_capable_date = '2008-09-04'
    schedule = 'Mo,Tu,We,Th,Fr'
    rights = '"Lord KC Green"'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        page_url = 'http://www.gunshowcomic.com/d/%(date)s.html' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
        page = self.parse_page(page_url)
        self.url = page.src('img[src^="http://www.gunshowcomic.com/comics/"]')
