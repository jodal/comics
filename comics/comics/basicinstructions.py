from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Basic Instructions'
    language = 'en'
    url = 'http://www.basicinstructions.net/'
    start_date = '2006-07-01'
    rights = 'Scott Meyer'

class Crawler(CrawlerBase):
    history_capable_days = 100
    schedule = 'Mo,We,Fr'
    time_zone = -7

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://basicinstructions.net/basic-instructions/rss.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/storage/"][src*=".gif"]')
            title = entry.title
            return CrawlerImage(url, title)
