from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Superpoop'
    language = 'en'
    url = 'http://www.superpoop.com/'
    start_date = '2008-01-01'
    rights = 'Drew'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.superpoop.com/rss/rss.php')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src$=".jpg"]')
            title = entry.title
            return CrawlerResult(url, title)
