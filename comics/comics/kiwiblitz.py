from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Kiwiblitz'
    language = 'en'
    url = 'http://www.kiwiblitz.com/'
    start_date = '2009-04-18'
    rights = 'Mary Cagle'

class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'Tu,Th'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.kiwiblitz.com/feed/')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('img[src*="/comics/"]')
            title = page.alt('img[src*="/comics/"]')
            return CrawlerImage(url, title)
