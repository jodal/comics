from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Diesel Sweeties (web)'
    language = 'en'
    url = 'http://www.dieselsweeties.com/'
    start_date = '2000-01-01'
    rights = 'Richard Stevens'

class Crawler(CrawlerBase):
    history_capable_date = '2000-01-01'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.dieselsweeties.com/ds-unifeed.xml')
        for entry in feed.for_date(pub_date):
            if not entry.summary:
                continue
            url = entry.summary.src('img[src*="/strips/"]')
            title = entry.title
            text = entry.summary.alt('img[src*="/strips/"]')
            return CrawlerImage(url, title, text)
