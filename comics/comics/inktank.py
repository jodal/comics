from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'InkTank'
    language = 'en'
    url = 'http://www.inktank.com/'
    start_date = '2008-04-01'
    rights = 'Barry T. Smith'

class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'Mo,We,Fr'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/inktank/HstZ')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics-rss/"]')
            title = entry.title
            return CrawlerResult(url, title)
