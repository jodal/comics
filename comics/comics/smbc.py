from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Saturday Morning Breakfast Cereal'
    language = 'en'
    url = 'http://www.smbc-comics.com/'
    start_date = '2002-09-05'
    rights = 'Zach Weiner'

class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.smbc-comics.com/rss.php')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            return CrawlerImage(url)
