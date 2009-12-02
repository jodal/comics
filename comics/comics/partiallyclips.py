from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'PartiallyClips'
    language = 'en'
    url = 'http://www.partiallyclips.com/'
    start_date = '2002-01-01'
    history_capable_days = 10
    schedule = 'Tu'
    time_zone = -5
    rights = 'Robert T. Balder'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.partiallyclips.com/includes/rss.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title.split(' - ')[0]
            return CrawlerResult(url, title)
