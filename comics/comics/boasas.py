from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Boy on a Stick and Slither'
    language = 'en'
    url = 'http://www.boasas.com/'
    start_date = '1998-01-01'
    rights = 'Steven L. Cloud'

class Crawler(CrawlerBase):
    history_capable_days = 365
    schedule = None
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.boasas.com/rss')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('.high_res img')
            title = entry.title
            return CrawlerImage(url, title)
