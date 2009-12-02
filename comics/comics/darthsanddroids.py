from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Darths & Droids'
    language = 'en'
    url = 'http://darthsanddroids.net/'
    start_date = '2007-09-14'
    history_capable_days = 14
    time_zone = -8
    rights = 'The Comic Irregulars'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://darthsanddroids.net/rss.xml')
        for entry in feed.for_date(pub_date):
            if entry.title.startswith('Episode'):
                url = entry.summary.src('img')
                title = entry.title
                return CrawlerResult(url, title)
